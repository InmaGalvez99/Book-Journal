/* Top 10 de los libros con mayor puntuación */

select top 10
	title as Titulo,
	author as Autor,
	my_rating as Puntuacion
from FactLibros
inner join DimAutores on DimAutores.autor_id = FactLibros.autor_id
order by my_rating desc 


/* Top 5 de libros leídos con la menos puntuación */

select top 5
	title as Titulo,
	author as Autor,
	my_rating as Puntuacion
from FactLibros
inner join DimAutores on DimAutores.autor_id = FactLibros.autor_id
where exclusive_shelf = 'read'
order by my_rating asc


/* Saber la puntuación de una saga concreta ordenada por el orden de la saga */

select
	title as Titulo,
	nombre_saga as Saga,
	orden_saga as Orden,
	my_rating as Puntuacion
from FactLibros
join DimSagas on DimSagas.saga_id = FactLibros.saga_id
where nombre_saga like '%Legacy of gods%'
order by orden_saga asc


/* Buscar todos los libros de una autora, tanto leídos como no leídos */

select 
	title as Titulo,
	author as Autor,
	exclusive_shelf as Estado
from FactLibros
join DimAutores on DimAutores.autor_id = FactLibros.autor_id
where author like '%Ali Hazelwood%'
order by exclusive_shelf desc


/* Calcular el total de libros leídos y no leídos */

select 
	exclusive_shelf as Estado,
	count(book_id) as Total_libros
from FactLibros
group by exclusive_shelf
order by Total_libros desc


/* autores favoritos: nota media + total de libros leídos agrupados por autor y ordenados por los libros leídos de cada autor 
de mayor a menos y su nota media */

select 
	author as Autor,
	count(book_id) as Libros_leidos,
	round(avg(my_rating),2) as Nota_media
from FactLibros
join DimAutores on DimAutores.autor_id = FactLibros.autor_id
where exclusive_shelf = 'read' and my_rating is not null
group by author
order by Libros_leidos desc, Nota_media desc


/* buscar repetición libro La hipótesis del amor de Ali Hazelwood por fecha. En este caso, hubo relectura por eso 2 fechas distintas.
Pero en Goodreads se registró 2 edicines distintas: la inglesa y la española. */

select
	title as Titulo,
	author as Autor,
	book_id as Libro_ID,
	date_read as Fecha_lectura
from FactLibros
join DimAutores on DimAutores.autor_id = FactLibros.autor_id
where author like '%Ali Hazelwood%' 
	and title like '%hypothesis%' or title like '%hipótesis%'
