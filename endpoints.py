from flask import Flask, json, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)

CORS(app)


try:
    con = psycopg2.connect(
        dbname = "Practica1_MIA",
        user = "root",
        password = "password",
        host = "localhost"
    )

    cur = con.cursor()

    print(con.status)


    @app.route("/")
    def inicio():
        return "<h1>Practica 1 MIA</h1>"

    @app.route("/consulta1", methods=['GET'])
    def consulta1():
        cur.execute("""select count(*) from "Master_Pelicula", "Pelicula"
                    where "Pelicula"."Nombre"='SUGAR WONKA' AND 
                    "Pelicula"."Id"="Master_Pelicula"."IdPelicula"
                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/consulta2", methods=['GET'])
    def consulta2():
        cur.execute("""
                select "Cliente"."Nombre", "Cliente"."Apellido"
                from "Cliente"
                where (select count(*) from "MasterAlquiler"
                        where "MasterAlquiler"."id_cliente" = "Cliente"."id") >= 40
                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/consulta3", methods=['GET'])
    def consulta3():
        cur.execute("""
                select "NombreActor", "ApellidoActor" from "Actor"
                where "ApellidoActor" Like '%son%'
                order by "NombreActor"

                
                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/consulta4", methods=['GET'])
    def consulta4():
        cur.execute("""
                    select "DetallePelicula"."Nombre_Actor","DetallePelicula"."Apellido_Actor","Pelicula"."Lanzamiento" from "DetallePelicula", "Master_Pelicula", "Pelicula"
                        where "DetallePelicula"."IdMaster" = "Master_Pelicula"."Id"
                        and "Pelicula"."Id" = "Master_Pelicula"."IdPelicula"
                        and "Pelicula"."DescripcionPelicula" like '%Crocodile%' and "Pelicula"."DescripcionPelicula" like '%Shark%'
                        order by "DetallePelicula"."Apellido_Actor" asc

                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/consulta5", methods=['GET'])
    def consulta5():
        cur.execute("""
                    select Min("A"."Sip"), "A"."Pais", max("A"."Ad") as "Cantidad", Max("A"."Ad")/Sum("A"."Ad")*100 "Porcentaje" from(
                        select distinct "Pais", "Cl"."Nombre" "Sip",
                        (select count(*) as "Columna" from "MasterAlquiler", "Cliente"
                        where "MasterAlquiler"."id_cliente" = "Cliente"."id"
                        and "Cl"."id" = "Cliente"."id") "Ad"
                        from "Direccion", "Cliente" "Cl"
                        where "Cl"."IdDireccion"="Direccion"."Id"
                    ) as "A"
                    where "A"."Ad" > 0
                    group by "A"."Pais"
                    order by "Cantidad"

                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/consulta6", methods=['GET'])
    def consulta6():
        cur.execute("""
                        select "AA"."Pais", "AA"."ConteoCiudad" "Ciudad" ,count("AA"."ConteoCiudad") "ConteoCiudad",
                        (cast((

                            select count("CC"."Pais") from(
                                select "Pais",
                                (select count(*) from "Cliente"
                                    where "Cliente"."IdDireccion" = "Direccion"."Id"
                                    )
                                from "Direccion"
                                where "Direccion"."Pais"="AA"."Pais"
                            ) as "CC"
                            
                            
                        ) as decimal )/cast(( 

                                select count("MM"."Ciudad") from(
                                select distinct "Ciudad"
                                from "Direccion"
                                where "Direccion"."Pais"="AA"."Pais"
                                ) as "MM"

                        ) as decimal))/
                        cast((
                                select count("PP"."Pais") from(
                                select "Pais",
                                (select count(*) from "Cliente"
                                    where "Cliente"."IdDireccion" = "Direccion"."Id"
                                    )
                                from "Direccion"
                                where "Direccion"."Pais"="AA"."Pais"
                                ) as "PP"	
                            
                        )as decimal)*100 "Porcentaje por ciudad (%)" from(
                            select distinct "Pais",
                                (select distinct "Ciudad" from "Direccion" "A"
                                    where "Direccion"."Ciudad" = "A"."Ciudad") "ConteoCiudad",
                                (select count(*) from "Cliente" "Cl" 
                                    where "Cl"."IdDireccion"="Direccion"."Id"
                                    and "Cliente"."id" = "Cl"."id" 
                                ) "B"
                            from "Direccion", "Cliente"
                            where "Cliente"."IdDireccion" = "Direccion"."Id"
                        )as "AA"
                        where "AA"."ConteoCiudad" <> '-'
                        group by "AA"."Pais", "AA"."ConteoCiudad"

                """)

        rows = cur.fetchall()

        arreglo = []

        for i in rows:
            arregloAux = []
            for j in i:
                arregloAux.append(str(j))
            arreglo.append(arregloAux)
        

        return jsonify(arreglo)

    @app.route("/consulta7", methods=['GET'])
    def consulta7():
        cur.execute("""
                select "AA"."Pais", "AA"."ConteoCiudad" "Ciudad" ,count("AA"."ConteoCiudad") "ConteoCiudad", 
                (
                    "AA"."B"/
                cast((		select count("MM"."Ciudad") from(
                        select distinct "Ciudad"
                        from "Direccion"
                        where "Direccion"."Pais"="AA"."Pais"
                        ) as "MM") as decimal)
                ) "Promedio"

                from(
                    select distinct "Pais",
                        (select distinct "Ciudad" from "Direccion" "A"
                            where "Direccion"."Ciudad" = "A"."Ciudad") "ConteoCiudad",
                        (select count(*) from "Cliente" "Cl", "MasterAlquiler" "Ma"
                            where "Cl"."IdDireccion"="Direccion"."Id"
                            and "Cliente"."id" = "Cl"."id" 
                            and "Ma"."id_cliente" = "Cliente"."id"
                        ) "B"
                    from "Direccion", "Cliente"
                    where "Cliente"."IdDireccion" = "Direccion"."Id"
                )as "AA"
                where "AA"."ConteoCiudad" <> '-' and "AA"."B" > 0
                group by "AA"."Pais", "AA"."ConteoCiudad","AA"."B"
                """)

        rows = cur.fetchall()

        arreglo = []

        for i in rows:
            arregloAux = []
            for j in i:
                arregloAux.append(str(j))
            arreglo.append(arregloAux)
        

        return jsonify(arreglo)

    @app.route("/consulta8", methods=['GET'])
    def consulta8():
        cur.execute("""
                select "AA"."Pais",count("AA"."B") "Alquiler" from(
                    select distinct "Pais",
                        (select distinct "Ciudad" from "Direccion" "A"
                            where "Direccion"."Ciudad" = "A"."Ciudad") "ConteoCiudad",
                        (select count(*) from "Cliente" "Cl", "MasterAlquiler" "Ma"
                            where "Cl"."IdDireccion"="Direccion"."Id"
                            and "Cliente"."id" = "Cl"."id" 
                            and "Ma"."id_cliente" = "Cliente"."id"
                            and "Ma"."IdMaster_peli" = (select "Id" from "Master_Pelicula"
                                where "Master_Pelicula"."IdPelicula" =  "Pelicula"."Id"
                                    and "Ma"."IdMaster_peli" = "Id")
                        ) "B"
                    from "Direccion", "Cliente", "Pelicula"
                    where "Cliente"."IdDireccion" = "Direccion"."Id"
                    and "Pelicula"."Categoria" ='Sports'

                ) as "AA"
                group by "AA"."Pais"


                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/consulta9", methods=['GET'])
    def consulta9():
        cur.execute("""
                select "NN"."Ciudad",max("NN"."B") 
                from(
                    select "Ciudad", "Pais",		
                        (select count(*) from "Cliente" "Cl", "MasterAlquiler" 
                                where "Cl"."IdDireccion"="Direccion"."Id"
                                and "Cliente"."id" = "Cl"."id" 
                                and "Cliente"."id" = "MasterAlquiler"."id_cliente"
                            ) "B"
                        from "Direccion", "Cliente"
                        where "Cliente"."IdDireccion" = "Direccion"."Id"
                        and "Direccion"."Pais" = 'United States'
                        and "Direccion"."Ciudad" <> 'Dayton'

                ) as "NN"
                where "NN"."B" > 26
                group by "NN"."Ciudad"

                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/consulta10", methods=['GET'])
    def consulta10():
        
        cur.execute("""
                    select "Dir"."Ciudad", "Dir"."Pais" from(
                        select "Ciudad", "Pais",		
                            (select count(*) from "Cliente" "Cl", "MasterAlquiler" 
                                    where "Cl"."IdDireccion"="Direccion"."Id"
                                    and "Cliente"."id" = "Cl"."id" 
                                    and "Cliente"."id" = "MasterAlquiler"."id_cliente"
                                ) "B",
                            (select count(*) from "Cliente" "Cl", "MasterAlquiler", "Pelicula"
                                    where "Cl"."IdDireccion"="Direccion"."Id"
                                    and "Cliente"."id" = "Cl"."id" 
                                    and "Cliente"."id" = "MasterAlquiler"."id_cliente"
                                    and "Pelicula"."Id" = (select "IdPelicula" from "Master_Pelicula"
                                                where "Master_Pelicula"."Id" ="MasterAlquiler"."IdMaster_peli")

                            and 
                            (select count(*) from "Pelicula" "Peli"
                                where "Peli"."Categoria"='Horror') >(select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Family')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Games')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Animation')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Classics')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Documentary')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Sports')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='New')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Children')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='-')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Music')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Travel')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Foreign')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Drama')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Action')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Comedy')
                            and (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Horror') > (select count(*) from "Pelicula" "Peli" where
                                    "Peli"."Categoria"='Sci-Fi')
                            ) "Horror"
                            from "Direccion", "Cliente"
                            where "Cliente"."IdDireccion" = "Direccion"."Id"

                        )as "Dir"
                    where "Dir"."Horror" > 0
                    group by "Dir"."Ciudad", "Dir"."Pais"
		
                """)

        rows = cur.fetchall()

        return jsonify(rows)

    @app.route("/eliminarTemporal", methods=['GET'])
    def eliminarTemporal():

        cur.execute("""truncate table "Temporal" cascade""")
        
        return "Temporal Eliminado con exito"

    @app.route("/eliminarModelo", methods=['GET'])
    def eliminarModelo():

        cur.execute("""
            truncate table "Direccion"  cascade;
            truncate table "Pelicula"   cascade;
            truncate table "Actor"      cascade;
            """)
        
        ##rows = cur.fetchall()

        return "Modelo Eliminado"


    @app.route("/cargarTemporal", methods=['GET'])
    def cargarTemporal():

        cur.execute("""copy public."Temporal" from '/home/mefm/Descargas/ArchivoDeEntradaPractica.csv' delimiter ';' csv header""")
        
        ##        rows = cur.fetchall()

        return "Temporal Cargado"
    
    @app.route("/cargarModelo", methods=['GET'])
    def modelo():
        cur.execute(""" 
        
                    /*DIRECCIONES*/

            /*Direccion Cliente*/

            insert into "Direccion" ("CodigoPostal", "Pais", "direccion", "Ciudad")
            select distinct "CodigoPostal", "PaisCliente", "DireccionCliente", "CiudadCliente"
            from "Temporal";

            /*Direccion Tienda*/

            insert into "Direccion" ("CodigoPostal", "Pais", "direccion", "Ciudad")
            select distinct "CodigoPostalTienda", "PaisTienda", "DireccionTienda", "CiudadTienda"
            from "Temporal";


            /*Direccion Empleado*/

            insert into "Direccion" ("CodigoPostal", "Pais", "direccion", "Ciudad")
            select distinct "CodigoPostalEmpleado", "PaisEmpleado", "DireccionEmpleado", "CiudadEmpleado"
            from "Temporal";




            /*CLIENTES*/
            insert into "Cliente" ("Nombre","Apellido","email","FechaRegistro","Activo","TiendaFav","IdDireccion")
            select distinct "nombreCliente","ApellidoCliente","CorreoCliente", "FechaCreacion","Activo","TiendaPreferida", (select "Id" from 
                                                                "Direccion" where "Direccion"."CodigoPostal"="CodigoPostal" AND "Direccion"."direccion" = "DireccionCliente" limit 1)
            from "Temporal";


            /*TIENDA*/
            insert into "Tienda" ("NombreTienda", "IdDireccion")
            select distinct "NombreTienda", (select "Id" from "Direccion" where "Direccion"."CodigoPostal"="CodigoPostalTienda" AND "Direccion"."direccion"="DireccionTienda" limit 1)
            from "Temporal";


            /*EMPLEADO*/


            insert into "Empleado" ("Nombre","Apellido","Activo","Usuario","Contrasenia","Tienda","Puesto","IdDireccion", "IdTienda")
            select distinct "NombreEmpleado","ApellidoEmpleado","EmpleadoActivo","UsuarioEmpleado","ContraseniaEmpleado"
            ,"TiendaEmpleado", CASE WHEN CONCAT("NombreEmpleado", "ApellidoEmpleado")=Concat("EncargadoNombre","EncargadoApellido") then 'Encargado' ELSE 'Empleado' end,
            (select "Id" from "Direccion" where "Direccion"."CodigoPostal"="CodigoPostalEmpleado" AND "Direccion"."direccion"="DireccionEmpleado" limit 1),
            (select "Id" from "Tienda" where "Tienda"."IdDireccion"=(select "Id" from "Direccion" where "Direccion"."CodigoPostal"="CodigoPostalTienda" AND "Direccion"."direccion"="DireccionTienda" limit 1))
            from "Temporal";




            /*PELICULA*/

            insert into "Pelicula" ("Nombre","Categoria","Lanzamiento", "DescripcionPelicula")
            select distinct "NombrePelicula", "CategoriaPelicula","AnioLanzamiento","DescripcionPelicula"
            from "Temporal";

            /*MASTER PELI*/
            insert into "Master_Pelicula" ("IdTienda", "IdPelicula")
            select distinct 
            (select "Id" from "Tienda" where "Tienda"."IdDireccion"=(select "Id" from "Direccion" where "Direccion"."CodigoPostal"="CodigoPostalTienda" AND "Direccion"."direccion"="DireccionTienda" limit 1)), 
            (select "Id" from "Pelicula" where "Pelicula"."Nombre"="NombrePelicula")
            from "Temporal";

            /*DETALLE PELICULA*/



            insert into "DetallePelicula"  ("DiasRenta","CostoRenta","CostoDaño","Duracion","Nombre_Actor","Apellido_Actor","Idioma","IdMaster")
            select distinct "DiasRenta","CostoRenta","CostoDanio","Duracion","NombreActor","ApellidoActor","LenguajePelicula",
            (select distinct "Id" from "Master_Pelicula"
            where "Master_Pelicula"."IdPelicula"=(select "Pelicula"."Id" from "Pelicula","Tienda" where 
                "Pelicula"."Nombre"="NombrePelicula"
                and "Pelicula"."DescripcionPelicula"="DescripcionPelicula"
                and "Pelicula"."Categoria"="CategoriaPelicula"
                and "Pelicula"."Lanzamiento"="AnioLanzamiento" limit 1)limit 1)
            from "Temporal";

            /*truncate table "Master_Pelicula" cascade*/

            /*MASTER ALQUILER*/
            insert into "MasterAlquiler" ("id_cliente","IdMaster_peli")
            select distinct
            (select  "id" from "Cliente" where "Cliente"."Nombre"="nombreCliente" AND "Cliente"."Apellido"="ApellidoCliente"), 
            (select  "Id" from "Master_Pelicula" 
            where "Master_Pelicula"."IdPelicula"=
            (select "Id" from "Pelicula" where "Pelicula"."Nombre"="NombrePelicula") limit 1)

            
            from "Temporal";




            /*DETALLE ALQUILER (FACTURA?) AJJA*/
            insert into "DetalleAlquiler" ("Fecha_Renta","Fecha_Retorno","MontoPagar","FechaPagar","IdAlquiler")
            select distinct "Fecha_Renta", "Fecha_Retorno", "MontoPagar","FechaPago",
            (select distinct "Id" from "MasterAlquiler" where 
            "MasterAlquiler"."IdMaster_peli"=
            (select distinct "Pelicula"."Id" from "Pelicula","Tienda" where 
                "Pelicula"."Nombre"="NombrePelicula"
                and "Pelicula"."DescripcionPelicula"="DescripcionPelicula"
                and "Pelicula"."Categoria"="CategoriaPelicula"
                and "Pelicula"."Lanzamiento"="AnioLanzamiento" limit 1)limit 1)

            from "Temporal";






            /*ACTOR*/
            insert into "Actor" ("NombreActor", "ApellidoActor")
            select distinct "NombreActor", "ApellidoActor"
            from "Temporal";


            /*ACTOR REPARTO*/
            insert into "ActorReparto" ("IdActor", "IdDetallePelicula")
            select distinct 
            (select "Id" from "Actor" where "Actor"."NombreActor"="NombreActor" AND "Actor"."ApellidoActor"="ApellidoActor" limit 1),
            (select "Id" from "DetallePelicula" where "DetallePelicula"."Idioma"="LenguajePelicula"
            AND "DetallePelicula"."Duracion"="Duracion" AND "DetallePelicula"."Nombre_Actor"="NombreActor" AND "DetallePelicula"."Apellido_Actor"="ApellidoActor" limit 1)
            from "Temporal";

        
            """)
        ##rows = cur.fetchall()
        return "<h2>Modelo cargado con exito</h2>"

    if __name__ == "__main__":  
        app.run(host='0.0.0.0')
except:
    print("Error de no se que cosa")




