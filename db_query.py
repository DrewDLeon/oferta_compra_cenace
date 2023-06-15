#Requerimos utilizar como fechas el between del mes anterior, para esto usaremos la siguiente funcion
from datetime import date, timedelta
import calendar


twenty_eight_days_ago = date.today() - timedelta(days=28)

yesterday = date.today() - timedelta(days=1)

print(f'28 days ago: {twenty_eight_days_ago}\n')
print(f'yesterday: {yesterday}')

query = f'''
                SELECT tcl.cliente, tcl.zona_carga, tcl.elemento, tcl.rpu, tlm.fechayhora, HOUR(fechayhora) as Hora, tlm.tipo, tlm.kwhe as kW, tlm.utc
                FROM tbl_clientes tcl
                INNER JOIN tbl_lecturas_medimem tlm ON tcl.id_cliente = tlm.id_cliente
                WHERE (tlm.fecha >= '{twenty_eight_days_ago}' and tlm.fecha <= '{yesterday}') AND tcl.cliente != 'Metsa'
                ORDER BY zona_carga, cliente, rpu, fechayhora
                '''


fecha = date.today() + timedelta(days=4) 
fechaNumber = fecha.weekday()
MonthNumber = fecha.month
dia = fecha.day
mes = calendar.month_name[MonthNumber]
fecha = fecha.strftime('%d/%m/%Y')
print("OFERTA DE COMPRA DIA: ",fecha)
print('Dia de la semana: ' ,fechaNumber)
print('Mes',mes)
print('Dia: ',dia)