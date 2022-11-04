import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
from playwright.async_api import async_playwright
from buscadorConnecta import connecta_actions

from extractor_detran import extractor_infracoes_em_autuacao
from utils.acresHourConnecta import hour_for_connecta
from excelGenerator import excel_generator
from utils.formatPlacaForConnecta import formatPlacaForConnecta

load_dotenv()

dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")

path = "consultas/Consulta dia "+formatData+".xlsx"
planilha = pd.read_excel("base_de_dados/Controle - Frota.xlsx",
                         "Vencimento Documentação", skiprows=1, usecols=['PLACA', 'RENAVAN'])
orgao = "Detran"
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
        await page.goto(os.environ["DET"])
        try:
            await page.locator(".closer").click()
        except:
            print("No have answer")
        for index, row in planilha_formatada.iterrows():
            placa = row['PLACA']
            renavan = row['RENAVAN']

            await page.locator("#input_placa").fill(str(placa))
            await page.locator("#input_renavam").fill(str(renavan))

            async with context.expect_event("page") as event_info:
                await page.locator("//*[@id='formVeiculo']/div[4]/input[2]").click()
            page2 = await event_info.value
            print(placa, renavan)
            try:
                await page2.locator("#cmbTipoDebito").select_option("Integral")
                url = await page2.inner_html('//*[@id="div_servicos_Autuacoes"]/table/tbody/tr[2]/td[2]')
                debito = extractor_infracoes_em_autuacao(url)
                hours = hour_for_connecta(debito)
                connecta = await context.new_page()
                print(debito['local'], debito['data'])
                condutor = await connecta_actions(page=connecta, hours=hours, placa=formatPlacaForConnecta(str(placa)))
                await excel_generator(placa=str(placa), multa=debito['local'], local_data=debito['data'], condutor=condutor, path=path, orgao=orgao)
            except:
                print("Débito não encontrado")

            await page2.close()
        await browser.close()

asyncio.run(main())
