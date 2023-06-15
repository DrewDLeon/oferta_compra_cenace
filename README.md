# Oferta de Compra de Energia CENACE
Script de Python que genera y envia una oferta de compra de energia al Centro Nacional de Control de Energia


El CENACE tal cual como el Manual Tecnico de Uso, tambien incluido en este repositorio lo demanda, requiere de informacion confidencial del participante del mercado, informacion que en este caso fue usada en un .ENV file.
Asi mismo, el CENACE recomienda que se oferte el promedio de consumo de los ultimos 28 dias.

Lo que realizan estos es scripts es:
- DB_Params, establecer los parametros para poder conectar a la BD (se usaron variables de entorno)

- db_query, se establece el query a ejecutar, en el cual se define que dia se desea ofertar, asi como los 28 dias de los cuales se tomara en cuenta para poder establecer una oferta.

- df_start, en este se inicializa un dataframe con ese periodo de 28 dias de consumos

- df_process, aqui se procesa con pandas, para poder obtener este promedio terminando en un archivo con el cual se va a ofertar al CENACE

- bid_create, aqui se crea el formato XML y JSON que el Servicio Web del CENACE requiere para poder mandar esta oferta, y se manda la oferta de acuerdo al promedio establecido.


## NO INCLUIDOS
Mail.py, aqui se manda un correo con lo ofertado, fue retirado por ser innecesario para este repositorio
Db_insert, se inserta a la BD la informacion ofertada, para poder tener un registro historico, tambien se retiro por ser innecesario para el proposito del repositorio.



Elaborado por Andres De Leon Castilleja
