import pandas as pd
import pprint
import pyodbc
import mysql.connector as mysql
from db_query import query
from db_params import params
# Para Facturas dejar BLANK
database = params('SolarioDB')

# Creamos la conexion
db = mysql.connect(
user = database.user,
password = database.password,
database = database.database,
host = database.host,
port = database.port
)

# y su Cursor
dataCursor = db.cursor()
print('--------------------Base de datos conectada!--------------------\n')


# Ejecutamos la consulta de SQL
db_query = pd.read_sql_query(
    query, db
)

# Creamos Dataframe de Pandas
df = pd.DataFrame(db_query)
print('--------------------DataFrame Creado!--------------------\n')

db.close()
dataCursor.close()