import os
from playwright.async_api import Page, BrowserContext
from termcolor import colored
from connecta.buscadorConnecta import connecta_actions

from detran.extractors_detran import extractor_infracoes_em_autuacao, extractor_licenciamento, extractor_penalidades
from utils.acresHourConnecta import hour_for_connecta
from utils.excelGenerator import excel_generator_licenciamento, excel_generator_multas
from utils.formatPlacaForConnecta import formatPlacaForConnecta


async def buscador_detran(page: Page, context: BrowserContext, planilha_formatada, path):
    orgao = 'Detran'
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
        print(index, placa, renavan)
        try:
            page2.set_default_timeout(1000)
            await page2.locator("#cmbTipoDebito").select_option("Integral")
            urlLicenciamento = await page2.inner_html('//*[@id="Integral"]/table/tbody')
            licenciamento = await extractor_licenciamento(urlLicenciamento)
            await excel_generator_licenciamento(placa=str(placa), licenciamento=licenciamento['licenciamento'], data_vencimento=licenciamento['vencimento_licenciamento'], path=path)

        except:
            print(colored('Sem licenciamento pendente', 'green'))
        try:
            page2.set_default_timeout(1000)
            url = await page2.inner_html('//*[@id="div_servicos_Autuacoes"]/table/tbody/tr[2]/td[2]')
            debito = extractor_infracoes_em_autuacao(url)
            hours = hour_for_connecta(debito)
            connecta = await context.new_page()
            print(colored(debito['local']+debito['data'], 'red'))
            condutor = await connecta_actions(page=connecta, hours=hours, placa=formatPlacaForConnecta(str(placa)))
            await excel_generator_multas(placa=str(placa), multa=str(debito['local']).upper(), local_data=str(debito['data']).upper(), condutor=str(condutor).upper(), path=path, orgao=orgao.upper())
        except:
            print(
                colored("Infrações em autuação não encontradas", 'green'))
        try:
            page2.set_default_timeout(1000)
            url = await page2.inner_html('//*[@id="div_servicos_Multas"]/table/tbody/tr[2]/td[2]')
            debito = extractor_penalidades(url)
            hours = hour_for_connecta(debito)
            connecta = await context.new_page()
            print(colored(debito['local']+debito['data'], 'red'))
            condutor = await connecta_actions(page=connecta, hours=hours, placa=formatPlacaForConnecta(str(placa)))
            await excel_generator_multas(placa=str(placa).upper(), multa=str(debito['local']).upper(), local_data=str(debito['data']).upper(), condutor=str(condutor).upper(), path=path, orgao=orgao.upper())
        except:
            print(colored("Penalidades não encontradas", 'green'))

        await page2.close()
pass
