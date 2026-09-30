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

# 1. Por seguridad, asegurarnos de que 'Alexei' se queda como Ebook por si se coló por coincidencia
df_limpio.loc[df_limpio['Title'].str.contains('Alexei', case=False, na=False), 'Formato'] = 'Ebook'

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