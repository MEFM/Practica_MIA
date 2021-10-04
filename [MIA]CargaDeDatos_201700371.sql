select * from "Cliente";


select * from "Temporal";

/*CARGA MASIVA*/
copy public."Temporal" from '/home/mefm/Descargas/ArchivoDeEntradaPractica.csv' delimiter ';' csv header;

select count(*) from "Temporal";

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

select * from "Cliente" where "email"='-';
select "email" from "Cliente" group by "email" having count(*) > 1;

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
(select "Id" from "Master_Pelicula" where "Master_Pelicula"."IdTienda"=(select "Id" from "Pelicula" where "Pelicula"."Nombre"="NombrePelicula") limit 1)
from "Temporal";


/*MASTER ALQUILER*/
insert into "MasterAlquiler" ("id_cliente","IdMaster_peli")
select distinct
(select "id" from "Cliente" where "Cliente"."Nombre"="nombreCliente" AND "Cliente"."Apellido"="ApellidoCliente"), 
(select "Id" from "Master_Pelicula" where "Master_Pelicula"."IdTienda"=(select "Id" from "Pelicula" where "Pelicula"."Nombre"="NombrePelicula") limit 1)
from "Temporal";

/*DETALLE ALQUILER (FACTURA?) AJJA*/
insert into "DetalleAlquiler" ("Fecha_Renta","Fecha_Retorno","MontoPagar","FechaPagar","IdAlquiler")
select distinct "Fecha_Renta", "Fecha_Retorno", "MontoPagar","FechaPago",
(select "Id" from "MasterAlquiler" where 
"MasterAlquiler"."IdMaster_peli"=(select "Id" from "Master_Pelicula" where "Master_Pelicula"."IdTienda"=(select "Id" from "Pelicula" where "Pelicula"."Nombre"="NombrePelicula") limit 1))

from "Temporal";


select * from "Cliente";

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





