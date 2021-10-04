/*Tienda*/
select count(*) from "Tienda"

/*Peliculas*/
select count(*) from "Pelicula"

/*Direccion*/
select count(*) from "Direccion"

/*Ciudad*/
select count("AA"."Ciudad") from(
select distinct "Ciudad" from "Direccion"
) as "AA"


/*Pais*/
select count("AA"."Ciudad") from(
select distinct "Pais" from "Direccion"
) as "AA"

/*Actores*/

select count(*) from "Actor"


/*Categoria*/
select count("AA"."Categoria") from(
select distinct "Categoria" from "Pelicula"
) as "AA"

/*Renta*/

select count(*) from "MasterAlquiler"
