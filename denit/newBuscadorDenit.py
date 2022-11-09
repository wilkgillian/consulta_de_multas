import os
from playwright.async_api import Page, BrowserContext
from dotenv import load_dotenv
from termcolor import colored
from denit.extractorDenit import extractor_denit
load_dotenv()

async def buscador_denit(planilha, page: Page, path, context: BrowserContext):
    orgao = 'Denit'
    for index, row in planilha.iterrows():
        await page.goto(os.environ['DENI'])
        placa = row['PLACA']
        renavam = row['RENAVAN']
        await page.locator('#placa').fill(str(placa))
        print(index, placa, renavam)
        await page.locator('#renavam').fill(str(renavam))
        await page.locator('button', has_text='Continuar').click()
        try:
            page.set_default_timeout(3000)
            await extractor_denit(page, context, placa, path, orgao)
        except:
            print(colored("Sem débitos no denit", 'green'))

pass
