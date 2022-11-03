from datetime import date
import re

def hour_for_connecta(dados):
    data = re.search('(\\d{2}\\/\\d{2}\\/\\d{4})', dados['data']).group(0)
    hora = re.search('(\\d{2}\\:\\d{2})', dados['data']).group(0)
     
    date_hour = data +" "+ hora
    
    hour_first_part = hora[0:1]
    hour_last_part = hora[3:]
    if hour_first_part == 0:
        acres = '0.1'
        sum_hour = int(hour_first_part)+float(acres)
    else:
        sum_hour = int(hour_first_part)+1
        
    hour_acres = hour_first_part+str(sum_hour)
    date_hour_acres = data+" "+str(hour_acres)+":"+str(hour_last_part)
    return {"date_hour":date_hour, "date_hour_acres": date_hour_acres}