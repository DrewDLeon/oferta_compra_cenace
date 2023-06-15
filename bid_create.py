import requests
from db_query import fecha, dia, mes
from dotenv import load_dotenv
import json
import pandas as pd
import os
load_dotenv()

SOLARIO_KEY = "C044"

df1 = pd.read_excel(f'/Users/andrew/Documents/Solario/Oferta de Compra/Docs/Info_Oferta_{dia}-{mes}.xlsx')

userNameToken = os.environ.get('CENACE_MAIL')
passwordToken = os.environ.get('CENACE_PASSWORD')
huellaDigital = os.environ.get('CENACE_HD')

fechaInicial = fecha
fechaFinal = fecha
clvSistema = 'SIN'

URL_BID = "https://ws01.cenace.gob.mx:8082/mxswmem/EnviarOfertaCompraEnergiaService.asmx"
URL_BID_PRUEBAS = "https://ws01.cenace.gob.mx:9082/mxswmement/EnviarOfertaCompraEnergiaService.asmx" # Para pruebas
headers = {
    'Content-Type': 'application/soap+xml; charset=utf-8',
    'Host': 'ws01.cenace.gob.mx',
    'Content-Length': 'length',
}

bid_list = []
for i in df1.index: #Tamaño del dataframe
  if df1['Hora'][i] == 23:
    elemento = df1['elemento'][i]
    bid_step = {
        "demandaFijaMw":df1['Oferta(MWh)'][i], # df1['Oferta(MWh)'][i]
        "hora":int(df1['Hora'][i])+1,
        "idSubInt":1,
        "oiMw01":0,
        "oiPrecio01":0,
        "oiMw02":0,
        "oiPrecio02":0,
        "oiMw03":0,
        "oiPrecio03":0,
    }
    bid_list.append(bid_step)

    bid_dict = {"ofertaEconomica":bid_list}
    bid_OE = json.dumps(bid_dict, indent=2)
    payload = f"""<?xml version='1.0' encoding='utf-8'?>
    <soap12:Envelope xmlns:xsi='"http://www.w3.org/2001/XMLSchema-instance"' xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
      <soap12:Header>
        <Authentication xmlns="http://xmlns.cenace.com/">
          <userNameToken>{userNameToken}</userNameToken>
          <passwordToken>{passwordToken}</passwordToken>
          <hd>{huellaDigital}</hd>
        </Authentication>
      </soap12:Header>
      <soap12:Body>
        <enviarOfertaCompraEnergia xmlns="http://xmlns.cenace.com/">
          <clvParticipante>{SOLARIO_KEY}</clvParticipante>
          <fechaInicial>{fechaInicial}</fechaInicial>
          <fechaFinal>{fechaInicial}</fechaFinal>
          <clvCarga>{elemento}</clvCarga>
          <clvSistema>{clvSistema}</clvSistema>
          <jsonOE>{bid_OE}</jsonOE>
        </enviarOfertaCompraEnergia>
      </soap12:Body>
    </soap12:Envelope>
    """
    print(payload)
    response = requests.request('POST', URL_BID, headers=headers, data=payload)
    print(response.text)

    # RESETEAMOS PARA EL SIGUIENTE ELEMENTO
    bid_list = []
  else:
    bid_step = {
        "demandaFijaMw":df1['Oferta(MWh)'][i], # df1['Oferta(MWh)'][i]
        "hora":int(df1['Hora'][i])+1,
        "idSubInt":1,
        "oiMw01":0,
        "oiPrecio01":0,
        "oiMw02":0,
        "oiPrecio02":0,
        "oiMw03":0,
        "oiPrecio03":0,
    }
    bid_list.append(bid_step)
