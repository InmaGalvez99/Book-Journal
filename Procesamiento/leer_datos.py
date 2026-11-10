import pandas as pd
# cargar archivo csv
df = pd.read_csv('goodreads_library_export.csv')

# mostrar la primera fila para ver como viene estructurado
print(df.head(1))

# mostrar el nombre de todas las columnas disponibles
print(df.columns)

# mostrar datos de la columna binding
print(df['Binding'].unique())

# -------------------------------------------------------------------------------------
# Migrar de python a SQL para crear una bbdd raw
# -------------------------------------------------------------------------------------

import pandas as pd
from sqlalchemy import create_engine
import urllib   

# 1. Cargar el archivo CSV exportado de Goodreads desde tu carpeta data
# Asegúrate de que el nombre del archivo y la ruta coinciden con los tuyos
df = pd.read_csv('goodreads_library_export.csv')
print("¡CSV cargado correctamente! Filas y columnas:", df.shape)

# 2. Configurar la conexión a SQL Server (usando el servidor que ya usaste en librytics)
server = 'INMAPC\SQLEXPRESS'  # Ej: 'localhost' o 'NOMBRE_DE_TU_PC\\SQLEXPRESS'
database = 'Book_Journal_RAW'

# Creamos la cadena de conexión de forma segura con urllib
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# 3. Volcar los datos en bruto a la tabla 'goodreads_raw' en tu nueva base de datos
df.to_sql('goodreads_raw', con=engine, if_exists='replace', index=False)

print("¡Copia de seguridad en bruto (RAW) guardada con éxito en SQL Server!")