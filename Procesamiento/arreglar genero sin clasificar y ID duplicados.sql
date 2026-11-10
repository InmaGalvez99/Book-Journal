/* Buscar libros con genero sin clasificar */

select
	title,
	genero,
	subgenero
from FactLibros
join DimGeneros on DimGeneros.genero_id = FactLibros.genero_id
where genero like 'Por clasificar'

/* Buscar autor */
select 
	title,
	author,
	genero,
	subgenero,
	nombre_saga,
	orden_saga
from FactLibros
join DimGeneros on DimGeneros.genero_id = FactLibros.genero_id
join DimSagas on DimSagas.saga_id = FactLibros.saga_id
join DimAutores on DimAutores.autor_id = FactLibros.autor_id
where author like 'RuNyx'


/* Buscar titulo, genero y subgenero */
select 
	title,
	author,
	genero,
	subgenero,
	nombre_saga,
	orden_saga
from FactLibros
join DimGeneros on DimGeneros.genero_id = FactLibros.genero_id
join DimSagas on DimSagas.saga_id = FactLibros.saga_id
join DimAutores on DimAutores.autor_id = FactLibros.autor_id
where title like 'El emperador'


/* ver sagas */

select
	title,
	nombre_saga,
	DimSagas.saga_id
from FactLibros
join DimSagas on DimSagas.saga_id = FactLibros.saga_id
where nombre_saga like '%Almas Letales%'
