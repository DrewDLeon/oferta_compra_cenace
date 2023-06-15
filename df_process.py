from df_start import df
import pandas as pd
import numpy as np
from mail import send_mail
from db_query import yesterday, twenty_eight_days_ago, fechaNumber, mes, dia

start_date = twenty_eight_days_ago.strftime("%Y-%m-%d")
end_date = yesterday.strftime("%Y-%m-%d")

# Creamos los campos para el DataFrame = 'Dia', 'Hora', 'Minuto', 'Fecha'
print('Creando campos...')
df['Dia'] = df['fechayhora'].dt.day
df['Minuto'] = df['fechayhora'].dt.minute
df['fecha'] = df['fechayhora'].dt.date

# Acomodamos o agrupamos el DataFrame en orden a los campos escritos
print('Acomodando DataFrame...')
df.sort_values(by=['zona_carga','elemento', 'rpu', 'fechayhora', 'tipo'],ascending=[True, True, True,True, False], inplace=True)

#Debug print df
print('DataFrame:')
print(df.head(20))

# Agrupamos los datos por Nombre de Tienda, Fecha, Hora y Minuto, y aplicamos una funcion para mantener las lecturas Reales si existen, o mantener las Estimadas de ser caso contrario
print('Filtrando DataFrame...')

# Acomodamos o agrupamos el DataFrame en orden a los campos escritos
df = df.sort_values(by=['zona_carga', 'elemento', 'rpu', 'fechayhora', 'Hora', 'Minuto'])

def get_utc_value(df):
    if -6 in df['utc'].unique():
        return -6
    elif -5 in df['utc'].unique():
        return -5
    else:
        return -7


df = df.groupby(['zona_carga', 'rpu', 'fechayhora'], group_keys=False).apply(lambda x: x.loc[x['utc'] == get_utc_value(x)])

# df.to_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/ConsumoUTC{dia}{mes}.xlsx')

# reset the index before applying the lambda function
df = df.reset_index()

# Agrupamos los datos por Nombre de Tienda, Fecha, Hora y Minuto, y aplicamos una funcion para mantener las lecturas Reales si existen, o mantener las Estimadas de ser caso contrario
df_filtered = df.groupby(['rpu','fecha','Hora','Minuto'], group_keys=False).apply(lambda x: x[x['tipo'] == 'Real'] if any(x['tipo'] == 'Real') else x[x['tipo'] == 'Estimada'])

df_filtered.to_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/ConsumoFiltrado{dia}{mes}.xlsx')

# Filtramos o acomodamos los datos por el orden descrito:
print('Acomodando DataFrame Filtrado...')
df_filtered.sort_values(['zona_carga','elemento', 'rpu', 'fecha', 'Hora'], inplace=True)
df_filtered.reset_index(drop=True, inplace=True)

# Cambiamos el tipo de dato para estar seguros que podemos operarlos \
print('Cambiando tipo de datos...')
df_filtered['kW'] = df_filtered['kW'].astype(float)
df_filtered['zona_carga'] = df_filtered['zona_carga'].astype(str)
df_filtered['elemento'] = df_filtered['elemento'].astype(str)

#Debug print df filtered
print('DataFrame Filtrado:')
print(df_filtered.head(20))


"""SUMAMOS CONSUMO POR RPU"""
consumo_df = df_filtered.groupby(['elemento','zona_carga','cliente','rpu', 'fecha','Hora'], as_index=False)['kW'].sum()

consumo_df.rename(columns = {'kW':'Consumo(kWh)'}, inplace=True)

# Creamos una columna con el dia de la semana
consumo_df['fecha'] = pd.to_datetime(consumo_df['fecha'])
consumo_df['Weekday'] = consumo_df['fecha'].dt.day_name()

consumo_df['Weekday_Number'] = consumo_df['fecha'].dt.day_of_week

# Creamos la columna que contenga Dia - #Dia
consumo_df['Day_Name'] = consumo_df['Weekday'].map(str) + consumo_df['Hora'].map(str)

# Transformamos el consumo a Megas
consumo_df['Consumo(MWh)'] = ( consumo_df['Consumo(kWh)'] / 1000 )
consumo_df.pop('Consumo(kWh)')

consumo_df.to_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/ConsumoHorarioxCarga{dia}{mes}.xlsx')

print(consumo_df.head(30))

# Aplicamos un sort para poder tener los datos acomodados por zona de carga, carga, day (dia de la semana)
consumo_df.sort_values(['zona_carga','elemento','cliente','fecha','Hora'], inplace=True)
consumo_df.reset_index(drop=True, inplace=True)

consumo_df = consumo_df.groupby(['zona_carga','elemento','cliente','fecha','Hora'], as_index=False)['Consumo(MWh)'].sum() #Caso LC sumamos el consumo de las tiendas HORA DIA
# Creamos una columna con el dia de la semana
consumo_df['fecha'] = pd.to_datetime(consumo_df['fecha'])
consumo_df['Weekday'] = consumo_df['fecha'].dt.day_name()

consumo_df['Weekday_Number'] = consumo_df['fecha'].dt.day_of_week

# Creamos la columna que contenga Dia - #Dia
consumo_df['Day_Name'] = consumo_df['Weekday'].map(str) + consumo_df['Hora'].map(str)

"""------------------------------------------------------------------------------------------------------------------------------------"""

consumo_df = consumo_df.groupby(['zona_carga','elemento','fecha','Hora'], as_index=False)['Consumo(MWh)'].sum()
# Creamos una columna con el dia de la semana
consumo_df['fecha'] = pd.to_datetime(consumo_df['fecha'])
consumo_df['Weekday'] = consumo_df['fecha'].dt.day_name()

consumo_df['Weekday_Number'] = consumo_df['fecha'].dt.day_of_week

# Creamos la columna que contenga Dia - #Dia
consumo_df['Day_Name'] = consumo_df['Weekday'].map(str) + consumo_df['Hora'].map(str)

print('---------------------Reporte---------------------')
print(consumo_df.head(30))

consumo_df.to_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/ConsumoDiari-Elemento_Cliente-[{dia}{mes}].xlsx')

# Sacamos el promedio por dia-hora (Day)
df1 = (consumo_df.groupby(['zona_carga','elemento','Weekday_Number', 'Hora'], as_index=False)['Consumo(MWh)'].mean())

""""""
# Aplicamos un sort para poder tener los datos acomodados por zona de carga, carga, day (dia de la semana)
df1.sort_values(['zona_carga','elemento','Weekday_Number','Hora'], inplace=True)
df1.reset_index(drop=True, inplace=True)

df1.rename(columns = {'Consumo(MWh)':'Oferta(MWh)'}, inplace=True)

df1 = df1[df1['Weekday_Number'] == fechaNumber]
df1.reset_index(drop=True, inplace=True)

# SE REQUIERE MULTIPLICAR POR 1.25 CIERTAS ZONAS PARA REDUCIR SU OFERTA
# df1['Oferta(MWh)'] = np.where(df1['zona_carga'] == 'MONTERREY', df1['Oferta(MWh)'] * 1.25, df1['Oferta(MWh)'])
# df1['Oferta(MWh)'] = np.where(df1['zona_carga'] == 'SALTILLO', df1['Oferta(MWh)'] * 1.25, df1['Oferta(MWh)'])

# # Centro sur subir su oferta 1.25
# df1['Oferta(MWh)'] = np.where(df1['zona_carga'] == 'CENTRO SUR', df1['Oferta(MWh)'] * 1.25, df1['Oferta(MWh)'])

df1['Oferta(MWh)'] = np.where(df1['zona_carga'] == 'QUERÉTARO', df1['Oferta(MWh)'] + 0.150, df1['Oferta(MWh)'])
df1['Oferta(MWh)'] = np.where((df1['zona_carga'] == 'MONTERREY'), df1['Oferta(MWh)'] + 0.183, df1['Oferta(MWh)'])

print(df1.head(30))

# Guardamos el archivo en formato XSLX
""""""
df1.to_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/Info_Oferta_{dia}-{mes}.xlsx')

print('---------------------Consumos Generados---------------------')

dfJ = df1.groupby(['zona_carga', 'elemento'], as_index = False)['Oferta(MWh)'].sum()

dfJ.to_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/Ofertas_{dia}-{mes}.xlsx')

send_mail()
