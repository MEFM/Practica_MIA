
/*CONSULTA 1*/

select count(*) from "Master_Pelicula", "Pelicula"
where "Pelicula"."Nombre"='SUGAR WONKA' AND 
"Pelicula"."Id"="Master_Pelicula"."IdPelicula";


/*CONSULTA 2*/

select "Cliente"."Nombre", "Cliente"."Apellido"
from "Cliente"
where (select count(*) from "MasterAlquiler"
	   	where "MasterAlquiler"."id_cliente" = "Cliente"."id") >= 40


/*CONSULTA 3*/

select "NombreActor", "ApellidoActor" from "Actor"
where "ApellidoActor" Like '%son%'
order by "NombreActor";

/*CONSULTA 4*/


select "DetallePelicula"."Nombre_Actor","DetallePelicula"."Apellido_Actor","Pelicula"."Lanzamiento" from "DetallePelicula", "Master_Pelicula", "Pelicula"
where "DetallePelicula"."IdMaster" = "Master_Pelicula"."Id"
and "Pelicula"."Id" = "Master_Pelicula"."IdPelicula"
and "Pelicula"."DescripcionPelicula" like '%Crocodile%' and "Pelicula"."DescripcionPelicula" like '%Shark%'
order by "DetallePelicula"."Apellido_Actor" asc;


/*CONSULTA 5*/


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
order by "Cantidad";


/*CONSULTA 6*/

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



/*CONSULTA 7*/


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



/*CONSULTA 8*/

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




/*CONSULTA 9*/

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


/*CONSULTA 10*/
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
		
		
		
		
