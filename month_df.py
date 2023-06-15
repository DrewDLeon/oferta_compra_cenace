from datetime import datetime, date, timedelta
import calendar
import pandas as pd

fecha = date.today() - timedelta(days=75) #43 days from March 1st
print(f'Fecha Inicial {fecha}')

MonthNumber = fecha.month
dia = fecha.day
mes = calendar.month_name[MonthNumber]
print(f'Info_Oferta_{dia}-{mes}.xlsx')
df = pd.read_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/Info_Oferta_{dia}-{mes}.xlsx')
df['fecha'] = fecha
final_df = df

for i in range(28):
    if i >= 1:
        MonthNumber = fecha.month
        dia = fecha.day
        mes = calendar.month_name[MonthNumber]
        print(f'Info_Oferta_{dia}-{mes}.xlsx')
        df1 = pd.read_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/Info_Oferta_{dia}-{mes}.xlsx')
        df1['fecha'] = fecha
        final_df = pd.concat([final_df, df1], ignore_index=True)
        fecha = fecha + timedelta(days=1)
    else:
        fecha = fecha + timedelta(days=1)

final_df.to_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/Info_Oferta_{mes}.xlsx')