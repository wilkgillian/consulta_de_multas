from datetime import datetime
from openpyxl import Workbook, load_workbook
import pandas as pd

dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")

path = "consultas/Consulta dia 01-11-2022.xlsx"
planilha = load_workbook(path)

async def excel_generator(placa, multa, local_data, condutor):
    # planilha: Workbook
    try:
        page_docs = planilha['Documentos']
    except:
        planilha.create_sheet("Documentos")
        page_docs = planilha['Documentos']
        page_docs.append(
            [placa, multa, local_data, condutor])
        planilha.save(
                        filename="consultas/Consulta dia "+formatData+".xlsx")
    pass