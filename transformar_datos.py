import pandas as pd
df = pd.read_csv('goodreads_library_export.csv')
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
df_limpio['Formato'] = 'Ebook'
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
    'God of Wrath',
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
    df_limpio.loc[df_limpio['Title'].str.contains(libro, case=False, na=False),'Formato'] = 'Físico'

# Comprobar cuántos han quedado de cada formato

print(df_limpio['Formato'].value_counts())

# Imprimimos directamente los títulos filtrados sin bucles de por medio
print(df_limpio[df_limpio['Formato'] == 'Físico']['Title'])

# 2. Eliminar el libro 'Mate' si está duplicado con 'Alfa'
# Buscamos el índice de la fila donde el título sea 'Mate'
indices_mate = df_limpio[df_limpio['Title'].str.contains('Mate', case=False, na=False)].index
# 2. Usamos drop para eliminar esas filas del DataFrame
df_limpio = df_limpio.drop(indices_mate)

# 2. Eliminar el libro 'Right Move' que es el mismo que 'Jugando fuerte'
# Buscamos el índice de la fila donde el título sea 'Mate'
indices_rightmove = df_limpio[df_limpio['Title'].str.contains('Right Move', case=False, na=False)].index
# 2. Usamos drop para eliminar esas filas del DataFrame
df_limpio = df_limpio.drop(indices_rightmove)


#----------------------------------------------------------------------------
# Dividir columna título en 3 columnas: título, nombre saga, y núm saga
# ----------------------------------------------------------------------------

# 1 Extraer los textos de los paréntesis y dejarlos como dos columnas auxiliares sin alterar el texto. 
df_limpio['parentesis_1'] = df_limpio['Title'].str.extract(r'\(([^)]+)\)', expand=False)
todos_p = df_limpio['Title'].str.findall(r'\(([^)]+)\)')
df_limpio['parentesis_2'] = todos_p.apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None)

# 2 Creamos la columna Edicion
es_edicion_1 = df_limpio['parentesis_1'].str.contains(r'Spanish|Edition|Version|latino', case=False, na=False)
df_limpio['Edicion'] = df_limpio['parentesis_2']
df_limpio.loc[es_edicion_1, 'Edicion'] = df_limpio['parentesis_1']
df_limpio['Edicion'] = df_limpio['Edicion'].fillna('None')

# 3 Nombre_Saga y Orden_Saga
# Creamos una columna auxiliar con el contenido del primer paréntesis que NO sea edición
# Si el primer paréntesis era una edición, dejamos un valor vacío (None)
primer_parentesis_saga = df_limpio['parentesis_1'].copy()
primer_parentesis_saga[es_edicion_1] = None

# Columna Nombre_Saga: Quitamos todo lo que venga después de coma, #, nº para quedarnos solo con el nombre de la saga
df_limpio['Nombre_Saga'] = primer_parentesis_saga.str.replace(r',.*|#.*|n°.*', '', regex=True).str.strip()
# Los huecos vacíos o sin saga son libros únicos
df_limpio['Nombre_Saga'] = df_limpio['Nombre_Saga'].fillna('Libro único')

# Columna Orden_Saga: Extraemos el número de saga si existe, sino dejamos 0.Primeor buscamos # o nº si existe
df_limpio['Orden_Saga'] = primer_parentesis_saga.str.extract(r'(?:#|n°)\s*(\d+)', expand=False)
# y si no tiene número de saga, dejamos 0
df_limpio['Orden_Saga'] = df_limpio['Orden_Saga'].fillna(0)

# 4 Limpiar columna titulo original
df_limpio['Title'] = df_limpio['Title'].str.replace(r'\s*\([^)]*\)', '', regex=True).str.strip()
# Comprobación
print('Resultado final:')
print(df_limpio[['Title', 'Nombre_Saga', 'Orden_Saga', 'Edicion']].head(10))

# COMPROBAR LAS 2 PRIMERAS FILAS TRAS LAS TRANSFORMACIONES
print('Primeras filas tras las transformaciones:')
print(df_limpio.head(2))
print('Listado de columnas:', list(df_limpio.columns))

# Eliminar  columnas parentesis 1 y parentesis 2
df_limpio = df_limpio.drop(columns=['parentesis_1',
                                    'parentesis_2',
                                    'Date Added', 
                                    'Binding',
                                    'Year Published'])
print('Listado de columnas:', list(df_limpio.columns))