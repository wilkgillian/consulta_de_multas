import asyncio
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from termcolor import colored
from playwright.async_api import async_playwright
from connecta.condutores_habilitados import condutores
from denit.newBuscadorDenit import buscador_denit

from detran.buscadorDetran import buscador_detran
from utils.sendNotification import post_message_to_teams


load_dotenv()

dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")

path = "consultas/Consulta dia "+formatData+".xlsx"
planilha = pd.read_excel("base_de_dados/Controle - Frota.xlsx",
                         "Vencimento Documentação", skiprows=1, usecols=['PLACA', 'RENAVAN'])
try:
    planilha_formatada = pd.read_excel(path)
except:
    planilha.to_excel(path, index=False)
    planilha_formatada = pd.read_excel(path)


async def main():
    async with async_playwright() as p:
        chromium = p.chromium
        browser = await chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print(colored("<<<< Iniciando busca no detran >>>>",
                  'yellow', attrs=['reverse']))
            await buscador_detran(page=page, context=context, planilha_formatada=planilha_formatada, path=path)
            busca_detran = 'Concluída'
        except:
            print(colored("Falha ao executar a busca no detran", 'red'))
            busca_detran = 'Falhou'
        try:
            print(colored("<<<< Iniciando busca no denit >>>>",
                  'yellow', attrs=['reverse']))
            await buscador_denit(page=page, planilha=planilha_formatada, path=path, context=context)
            busca_denit = 'Concluída'
        except:
            print(colored("Falha ao executar busca no denit", 'red'))
            busca_denit = 'Falhou'
        try:
            print(colored("<<<< Iniciando busca dos condutores habilitados >>>>",
                  'yellow', attrs=['reverse']))
            await condutores(page=page, path=path)
            busca_cnh = 'Concluída'
        except:
            print(colored("Falha ao executar busca dos condutores",
                  "red", attrs=['reverse']))
            busca_cnh = 'Falhou'
        await browser.close()
        try:
            post_message_to_teams(message='[MENSAGEM DO ROBÔ 🤖]\n\nConsulta do dia '+str(
                formatData)+':\n\nBusca no detran -> '+busca_detran+'\n\nBusca no denit -> '+busca_denit+'\n\nBusca dos condutores -> '+busca_cnh+'')
            print(colored('Mensagem enviada', 'green', attrs=['reverse']))
        except:
            print(colored('Falha ao enviar notificação',
                  'red', attrs=['reverse']))
        print(colored("Busca finalizada...", 'blue', attrs=['reverse']))

asyncio.run(main())
