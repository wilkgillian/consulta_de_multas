import asyncio
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from termcolor import colored
from playwright.async_api import async_playwright
from denit.newBuscadorDenit import buscador_denit
from detran.buscadorDetran import buscador_detran


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

        # try:
        #     await buscador_detran(page=page, context=context, planilha_formatada=planilha_formatada, path=path)
        # except:
        #     print(colored("Falha ao executar a busca no detran", 'red'))
        try:
            await buscador_denit(page=page, planilha=planilha_formatada, path=path, context=context)
        except:
            print(colored("Falha ao executar busca no denit", 'red'))
        await browser.close()
        print("Busca finalizada...")

asyncio.run(main())
