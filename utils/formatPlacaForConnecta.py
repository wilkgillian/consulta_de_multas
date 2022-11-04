def formatPlacaForConnecta(placa):
    placa_first= placa[0:3]
    placa_last=placa[3:]
    
    placa_replaced = "("+placa_first+"-"+placa_last+")"
    return placa_replaced
