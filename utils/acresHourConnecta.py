import re


def hour_for_connecta(dados):
    data = re.search('(\\d{2}\\/\\d{2}\\/\\d{4})', dados['data']).group(0)
    hora = re.search('(\\d{2}\\:\\d{2})', dados['data']).group(0)

    date_hour = data + " " + hora

    hour_first_part = hora[0:2]
    hour_last_part = hora[3:]
    if int(hour_first_part) == 0:
        sum_hour = '01'

    elif int(hora[0]) == 0 and int(hora[1]) != 0:
        adding = int(hora[1])+1
        if adding <= 9:
            sum_hour = "0"+str(adding)
        else:
            sum_hour = str(adding)

    elif int(hour_first_part) >= 23 and int(data[0:2]) < 31:
        sum_hour = "00"
        data_formated = int(data[0:2])+1
        if int(data[0:2]) >= 9:
            data = str(data_formated)+data[2:]
        else:
            data = "0"+str(data_formated)+data[2:]

    elif int(data[0:2]) == 31 and int(data[3:5]) < 12 and int(hour_first_part) >= 23:
        sum_date = int(data[3:5])+1
        data = "01/"+str(sum_date)+data[5:]
        sum_hour = "00"

    elif int(data[0:2]) == 31 and int(data[3:5]) == 12 and int(hour_first_part) >= 23:
        sum_date = int(data[6:])+1
        data = "01/"+data[3:6]+str(sum_date)
        sum_hour = "00"

    else:
        sum_hour = int(hour_first_part)+1
    date_hour_acres = data+" "+str(sum_hour)+":"+str(hour_last_part)

    return {"date_hour": date_hour, "date_hour_acres": date_hour_acres}
