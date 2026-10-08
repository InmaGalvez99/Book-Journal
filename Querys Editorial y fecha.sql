/* Ver la fecha de publicación original*/

select
	title as Titulo,
	original_publication_year as Fech_Publicacion_Origen
from FactLibros

/* buscar libros por título y autor concreto*/

select 
	title as Titulo,
	author as Autor
from FactLibros
join DimAutores on DimAutores.autor_id = FactLibros.autor_id
where author like '%Kristen Ciccarelli%'

/* listado de generos y subgeneros*/

select
	genero as Genero,
	subgenero as Subgenero
from DimGeneros

/* Buscar editorial ID 3*/

select 
	title as Titulo,
	DimPublisher.publisher_id as ID_Editorial,
	publisher as Editorial
from FactLibros
join DimPublisher on DimPublisher.publisher_id = FactLibros.publisher_id
where DimPublisher.publisher_id is null

