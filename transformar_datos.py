import pandas as pd
df = pd.read_csv('goodreads_library_export.csv')


# Limpiar y convertir todas las columnas a minúsculas y reemplazar espacios por guiones bajos automáticamente
df.columns = df.columns.str.lower().str.replace(' ', '_')


print(f"Filas originales: {len(df)}")

# Descartar las columnas que no queremos
columnas_a_borrar = ['Bookshelves with positions', 
                     'Bookshelves',
                     'My Review', 
                     'Spoiler', 
                     'Private Notes', 
                     'Owned Copies', 
                     'Author l-f', 
                     'Additional Authors']
df_limpio= df.drop(columns=columnas_a_borrar, errors='ignore')

# Vista previa de las columnas restanets
print ('Columnas restantes después de la limpieza:')
print(df_limpio.columns.tolist())

# --------------------------------------------------------------------------
# Creamos la columna Formato y ponemos que todos los libros son Ebook
df_limpio['formato'] = 'Ebook'
# escribirmos los libros que hemos leído en físico para identificar cuáles son ebook y cuáles físicos
libros_físicos = [
    'mile',
    'Jugando fuerte',
    'Caught up',
    'Siguiendo el juego',
    'Volviendo a empezar',
    'Zarco',
    'Lagos',
    '(Clan Z, #3)',
    'Oscar',
    'Beni',
    'The Love Hypothesis',
    'Brain',
    'Love, Theoretically',
    'No es amor',
    'Si es perfeccto no es amor',
    'God of Malice',
    'God of Pain',
    'God of War',
    'God of Wrath'
    'God of Ruin',
    'God of Fury',
    'Twisted games',
    'Flawless',
    'Heartless',
    'Powerless',
    'Alfa',
    '(Bride, #1)',
    'Deep end',
    'Lupara bianca',
    'Naturaleza de escorpión',
    'Hooked',
    'Scarred',
    'Wretched',
    'Heartless Hunter',
    'Book lovers',
    'Funny Story',
    'Gente que conocemos en vacaciones',
    'Todo lo que quiero eres tú',
    'razones',
    'Cien',
    '(Quererte, #1)',
    '(Quererte, #2)',
    'Beautiful fiend',
    'The Lies We Steal',
    'La novia gitana',
    'La red púrpura',
    'league',
    'Wild love',
    'court'
]

# Si el título contiene alguna de estas palabras, cambia a Físico
for libro in libros_físicos:
    df_limpio.loc[df_limpio['title'].str.contains(libro, case=False, na=False),'formato'] = 'Físico'

# Comprobar cuántos han quedado de cada formato

print(df_limpio['formato'].value_counts())

# Imprimimos directamente los títulos filtrados sin bucles de por medio
print(df_limpio[df_limpio['formato'] == 'Físico']['title'])

# 2. Eliminar el libro 'Mate' si está duplicado con 'Alfa'
# Buscamos el índice de la fila donde el título sea 'Mate'
indices_mate = df_limpio[df_limpio['title'].str.contains('Mate', case=False, na=False)].index
# 2. Usamos drop para eliminar esas filas del DataFrame
df_limpio = df_limpio.drop(indices_mate)

# 2. Eliminar el libro 'Right Move' que es el mismo que 'Jugando fuerte'
# Buscamos el índice de la fila donde el título sea 'Mate'
indices_rightmove = df_limpio[df_limpio['title'].str.contains('Right Move', case=False, na=False)].index
# 2. Usamos drop para eliminar esas filas del DataFrame
df_limpio = df_limpio.drop(indices_rightmove)


#----------------------------------------------------------------------------
# Dividir columna título en 3 columnas: título, nombre saga, y núm saga
# ----------------------------------------------------------------------------

# 1 Extraer los textos de los paréntesis y dejarlos como dos columnas auxiliares sin alterar el texto. 
df_limpio['parentesis_1'] = df_limpio['title'].str.extract(r'\(([^)]+)\)', expand=False)
todos_p = df_limpio['title'].str.findall(r'\(([^)]+)\)')
df_limpio['parentesis_2'] = todos_p.apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None)

# 2 Creamos la columna Edicion
es_edicion_1 = df_limpio['parentesis_1'].str.contains(r'Spanish|Edition|Version|latino', case=False, na=False)
df_limpio['edicion'] = df_limpio['parentesis_2']
df_limpio.loc[es_edicion_1, 'edicion'] = df_limpio['parentesis_1']
df_limpio['edicion'] = df_limpio['edicion'].fillna('None')

# 3 Nombre_Saga y Orden_Saga
# Creamos una columna auxiliar con el contenido del primer paréntesis que NO sea edición
# Si el primer paréntesis era una edición, dejamos un valor vacío (None)
primer_parentesis_saga = df_limpio['parentesis_1'].copy()
primer_parentesis_saga[es_edicion_1] = None

# Columna Nombre_Saga: Quitamos todo lo que venga después de coma, #, nº para quedarnos solo con el nombre de la saga
df_limpio['nombre_saga'] = primer_parentesis_saga.str.replace(r',.*|#.*|n°.*', '', regex=True).str.strip()
# Los huecos vacíos o sin saga son libros únicos
df_limpio['nombre_saga'] = df_limpio['nombre_saga'].fillna('Libro único')

# Columna Orden_Saga: Extraemos el número de saga si existe, sino dejamos 0.Primeor buscamos # o nº si existe
df_limpio['orden_saga'] = primer_parentesis_saga.str.extract(r'(?:#|n°)\s*(\d+)', expand=False)
# y si no tiene número de saga, dejamos 0
df_limpio['orden_saga'] = df_limpio['orden_saga'].fillna(0)

# 4 Limpiar columna titulo original
df_limpio['title'] = df_limpio['title'].str.replace(r'\s*\([^)]*\)', '', regex=True).str.strip()
# Comprobación
print('Resultado final:')
print(df_limpio[['title', 'nombre_saga', 'orden_saga', 'edicion']].head(10))

# COMPROBAR LAS 2 PRIMERAS FILAS TRAS LAS TRANSFORMACIONES
print('Primeras filas tras las transformaciones:')
print(df_limpio.head(2))
print('Listado de columnas:', list(df_limpio.columns))

# Eliminar  columnas parentesis 1 y parentesis 2
df_limpio = df_limpio.drop(columns=['parentesis_1',
                                    'parentesis_2'])
print('Listado de columnas:', list(df_limpio.columns))


# -------------------------------------------------------------------------------------------
# COLUMNAS GÉNERO Y SUBGÉNERO
# -------------------------------------------------------------------------------------------

def clasificar_generos(row):
    saga = row['nombre_saga']
    autor = row['author']
    titulo = row['title']

# 1. REGLAS PARA SAGA: barre de un plumazo los libros de la misma saga

    if saga == 'Clan Z':
        return ('Romance', 'Mafia Romance')
    elif saga == 'No es amor':
        return ('Romance', 'Romance Contemporáneo')
    elif saga == 'Bride':
        return ('Fantasía', 'Romance Paranormal')
    elif saga == 'Legacy of Gods':
        return ('Romance', 'Dark Romance')
    elif saga == 'Chestnut Springs':
        return ('Romance', 'Romance Contemporáneo')
    elif saga == 'Rose Hill':
        return ('Romance', 'Romance Contemporáneo')
    elif saga == 'D.C Stars':
        return ('Romance', 'Sport Romance')
    elif saga == 'Dark Forces':
        return ('Romance', 'Romance Militar')
    elif saga == 'Never Afert':
        return ('Romance', 'Dark Romance')
    elif saga == 'Twisted':
        return ('Romance', 'Dark Romance')
    elif saga == 'North Shore':
        return ('Romance', 'Dark Romance')
    elif saga == 'Silver Pines Ranch':
        return ('Romance', 'Cowboy Romance')
    elif saga == 'Sky Ridge Hotshots':
        return ('Romance', 'Romance Contemporáneo')
    elif saga == 'The Soldiers of Bedlam':
        return ('Romance', 'Dark Romance')
    elif saga == 'Sinners of Saint':
        return ('Romance', 'Dark Romance')
    elif saga == 'Society of Villains':
        return ('Romance', 'Mafia Romance')
    elif saga == 'Vipers':
        return ('Romance', 'Dark Romance')
    elif saga == 'Deception Trilogy':
        return ('Romance', 'Mafia Romance')
    elif saga == 'Throne Duet':
        return ('Romance', 'Mafia Romance')
    elif saga == 'Límites Prohibidos':
        return ('Romance', 'Dark Romance')
    elif saga == 'Bestias peligrosas':
        return ('Romance', 'Mafia Romance')
    elif saga == 'Entre Mafias':
        return ('Romance', 'Mafia Romance')
    elif saga == 'Cupido':
        return ('Romance', 'Cowboy Romance')
    elif saga == 'Arpias':
        return ('Romance', 'Dark Romance')
    elif saga == 'Maple Hills':
        return ('Romance', 'Sport Romance')
    elif saga == 'Rubí de sangre':
        return ('Fantasía', 'Fantasía Romántica')
    elif saga == 'Kings of Sin':
        return ('Romance', 'Romance Contemporáneo')
    elif saga == 'Pecados':
        return ('Romance', 'Romance Contemporáneo')
    elif saga == 'Dirty Air':
        return ('Romance', 'Sport Romance')
    elif saga == 'Dreamland Billionaires':
        return ('Romance', 'Romance Contemporáneo')
    elif saga == 'Gold Rush Runch':
        return ('Romance',  'Cowboy Romance')
    elif saga == 'Royal Elite':
        return ('Romance','Dark Romance')
    elif saga == 'Speed':
        return ('Romance', 'Dark Romance')
    elif saga == 'Villain':
        return ('Romance', 'Dark Romance')
    
    

# 2. REGLAS POR TITULO: si el título es de un libro independiente 
    elif 'Naturaleza de Escorpión' in str(titulo): # usamos 'in' por si el título varía un poco
        return ('Romance', 'Dark Romance')
    elif 'Love Hypothesis' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'love, Theoretically' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'Love on the Brain' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'Deep End' in str(titulo):
        return ('Romance', 'Sport Romance')
    elif 'Lupara Bianca' in str(titulo):
        return ('Romance', 'Mafia Romance')
    elif 'Déjame atrás' in str(titulo):
        return ('Romance', 'Romance Militar')
    elif 'Maldita fortuna' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'Petricor' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'In Stormy Weather' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'Ira' in str(titulo):
        return ('Romance', 'Dark Romance')
    elif 'Descifrando a Cox' in str(titulo):
        return ('Romance', 'Dark Romance')
    elif 'Icebraker' in str(titulo):
        return ('Romance', 'Sport Romance')
    elif 'Cuando caiga la nieve' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'El error vive arriba' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'Fever Dream' in str(titulo):
        return ('Romance', 'Cowboy Romance')
    elif 'Striker' in str(titulo):
        return ('Romance', 'Sport Romance')
    elif 'Defender' in str(titulo):
        return ('Romance', 'Sport Romance')
    elif 'Mariposa' in str(titulo):
        return ('Romance', 'Romance Militar')
    elif 'El camino a Rhodes' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'De Lukov, con amor' in str(titulo):
        return ('Romance', 'Sport Romance')
    elif 'Bourbon & Lies' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'La luz de todos nuestros otoños' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'Fuera de juego' in str(titulo):
       return ('Romance', 'Sport Romance')
    elif 'Si fuera amor' in str(titulo):
        return ('Romance', 'Sport Romance')
    elif 'Muñeca Rusa' in str(titulo):
        return ('Romance', 'Mafia Romance')
    elif 'Criaturas despiadadas' in str(titulo):
        return ('Romance', 'Mafia Romance')
    elif 'La voz de Archer'in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'Turno de noche' in str(titulo):
        return ('Romance', 'Sport Romance')
    elif 'Hate mail' in str(titulo):
        return ('Romance', 'Romance Contemporáneo')
    elif 'End game' in str(titulo):
        return ('Romance', 'Sport Romance')
    

    

# 3. MÁS AUTORES O SAGAS (Aquí irás añadiendo tus siguientes reglas poco a poco)
    # elif autor == 'Nombre de Autora':
    #     return ('Fantasía', 'Fantasía Romántica')
    elif autor == 'Sarah J. Maas':
        return ('Fantasía', 'Fantasía Romántica')
    elif autor == 'Carmen Mola':
        return ('Thriller', 'Thriller Policíaco')
    elif autor == 'Emily Henry':
        return ('Romance', 'Romance Contemporáneo')
    elif autor == 'Violeta Reed':
        return ('Romance', 'Romance Contemporáneo')
    elif autor == 'Liz Tomforde':
        return ('Romance', 'Sport Romance')
    elif autor == 'Monty Jay':
        return ('Romance', 'Dark Romance')
    elif autor == 'Elle Kennedy':
        return ('Romance', 'Sport Romance')
    elif autor == 'Danielle Lori':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Walker Rose':
        return ('Romance', 'Romance Contemporáneo')
    elif autor == 'Lyla Sage':
        return ('Romance', 'Cowboy Romance')
    elif autor == 'Jessica Peterson':
        return ('Romance', 'Cowboy Romance')
    elif autor == 'Bailey Hannah':
        return ('Romance', 'Cowboy Romance')
    elif autor == 'Elliot Rose':
        return ('Romance', 'Cowboy Romance')
    elif autor == 'H.M. Wolfe':
        return ('Fantasía', 'Fantasía Romántica')
    elif autor == 'Kristen Ciccarelli':
        return ('Fantasía', 'Fantasía Romántica')
    elif autor == 'Emilia Rossi':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Neva Altaj':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Mila García García':
        return ('Romance', 'Dark Romance')
    elif autor == 'Ana Serca':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Becca Devereux':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Grace Reilly':
        return ('Romance', 'Sport Romance')
    elif autor == 'Runyx':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Somme Sketcher':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Navessa Allen':
        return ('Romance', 'Dark Romance')
    elif autor == 'Adriana Criado':
        return ('Romance', 'Cowboy Romance')
    elif autor == 'Bailey Hannah':
        return ('Romance', 'Cowboy Romance')
    elif autor == 'Emily Rath':
        return ('Romance', 'Sport Romance')
    elif autor == 'Moruena Estríngana':
        return ('Romance', 'Sport Romance')
    elif autor == 'Stephanie Archer':
        return ('Romance', 'Sport Romance')
    elif autor == 'Lucy Score':
        return ('Romance', 'Romance Contemporáneo')
    elif autor == 'Eva Winners':
        return ('Romance', 'Mafia Romance')
    elif autor == 'Peyton Corinne':
        return ('Romance', 'Sport Romance')
    elif autor == 'Brynne Weaver':
        return ('Romance', 'Dark Romance')
    elif autor == 'Elena Armas':
        return ('Romance', 'Romance Contemporáneo')
    elif autor == 'Lynn Painter':
        return ('Romance', 'Sport Romance')
    elif autor == 'Alexandra Moody':
        return ('Romance', 'Sport Romance')
    elif autor == 'Lisina Coney':
        return ('Romance', 'Romance Contemporáneo')
    elif autor == 'Sierra Simone':
        return ('Romance', 'Dark Romance')
    elif autor =='Vi Keeland':
        return ('Romance', 'Romance Contemporáneo')
    elif autor == 'Leigh Rivers':
        return ('Romance', 'Dark Romance')
    elif autor == 'Nira Strauss':
        return ('Romance', 'Sport Romance')
    elif autor == 'Becka Mack':
        return ('Romance', 'Sport Romance')
    elif autor == 'Bal Khabra':
        return ('Romance', 'Sport Romance')
    elif autor == 'Kandi Steiner':
        return ('Romance', 'Sport Romance')
 
    


# 4. LIBROS SIN CLASIFICAR
    else:
        return ('Por clasificar', 'Por clasificar')

# aplicamos la función a cada fila del DataFrame y creamos las nuevas columnas
df_limpio[['genero', 'subgenero']] = df_limpio.apply(clasificar_generos, axis=1, result_type='expand')

# Comprobación de las nuevas columnas
resultado_autor = df_limpio[df_limpio['author'] == 'Neva Altaj']
print('Resultado del autor Neva Altaj:')
print(resultado_autor[['title', 'nombre_saga', 'genero', 'subgenero']].head(3))

resultado_libro = df_limpio[df_limpio['title'].str.contains('Maldita Fortuna', case=False, na=False)]
print('Resultado del libro Maldita Fortuna:')
print(resultado_libro[['title', 'author', 'genero', 'subgenero']])

# Comprobar los libros por clasificar

pendientes = df_limpio [df_limpio['genero']=='Por Clasificar']
print(f"¡Te quedan {len(pendientes)} libros por clasificar!")
print(pendientes[['title', 'author', 'nombre_saga']].head(15))


# CORREGIR LIBROS SIN EDITORIAL

# 1. Rellenar los huecos vacíos heredando la editorial de los libros de la misma saga
df_limpio['publisher'] = df_limpio.groupby('nombre_saga')['publisher'].bfill().ffill()

# 2. Para los libros que no tienen saga o siguen sin editorial, poner un texto limpio
df_limpio['publisher'] = df_limpio['publisher'].fillna('Autopublicado')


# ----------------------------------------------------------------------------------------
# CARGA DE DATOS BBDD SQL SERVER
# ----------------------------------------------------------------------------------------


import pandas as pd
from sqlalchemy import create_engine
import urllib

# 1. CREAR LAS DIMENSIONES A PARTIR DE TU `df_limpio` YA EXISTENTE
dim_autores = df_limpio[['author']].drop_duplicates().reset_index(drop=True)
dim_autores['autor_id'] = dim_autores.index + 1

dim_publisher = df_limpio[['publisher']].drop_duplicates().reset_index(drop=True)
dim_publisher['publisher_id'] = dim_publisher.index + 1

dim_generos = df_limpio[['genero', 'subgenero']].drop_duplicates().reset_index(drop=True)
dim_generos['genero_id'] = dim_generos.index + 1

dim_sagas = df_limpio[['nombre_saga']].drop_duplicates().reset_index(drop=True)
dim_sagas['saga_id'] = dim_sagas.index + 1

# 2. CONSTRUIR LA TABLA DE HECHOS (Fact_Libros)
fact_libros = df_limpio.merge(dim_autores, on='author', how='left')
fact_libros = fact_libros.merge(dim_publisher, on='publisher', how='left')
fact_libros = fact_libros.merge(dim_generos, on=['genero', 'subgenero'], how='left')
fact_libros = fact_libros.merge(dim_sagas, on='nombre_saga', how='left')


columnas_fact = [
    'book_id', 'title', 'isbn', 'isbn13', 'my_rating', 'number_of_pages',
    'original_publication_year', 'date_read', 'exclusive_shelf', 'read_count',
    'formato', 'edicion', 'orden_saga',
    'autor_id', 'publisher_id', 'genero_id', 'saga_id'
]
fact_libros = fact_libros[columnas_fact]


# 3. CONFIGURACIÓN DE LA CONEXIÓN A SQL SERVER (con la 'r' para evitar el warning)
server = r'INMAPC\SQLEXPRESS'
database_name = 'DB_BookJournal'

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database_name};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")




# 4. CARGA DE LAS TABLAS A SQL SERVER
dim_autores.to_sql('DimAutores', con=engine, if_exists='replace', index=False)
dim_publisher.to_sql('DimPublisher', con=engine, if_exists='replace', index=False)
dim_generos.to_sql('DimGeneros', con=engine, if_exists='replace', index=False)
dim_sagas.to_sql('DimSagas', con=engine, if_exists='replace', index=False)
fact_libros.to_sql('FactLibros', con=engine, if_exists='replace', index=False)

print("¡Modelo en estrella creado y volcado a SQL Server con éxito! ")