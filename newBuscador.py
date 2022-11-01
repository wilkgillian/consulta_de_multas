import asyncio
import os
import time
import re
from dotenv import load_dotenv
from playwright.async_api import async_playwright

from extractor_detran import extractor_infracoes_em_autuacao
from utils.convertHourConnecta import acres_hour_for_connecta

load_dotenv()

async def main():
    async with async_playwright() as p:
        chromium = p.chromium
        browser = await chromium.launch(timeout=10000, headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(os.environ["DET"])
        
        try:
            await page.locator(".closer").click()
        except:
            print("No have answer")
        
        await page.locator("#input_placa").fill("QCW4251")
        await page.locator("#input_renavam").fill("01221078949")
        
        async with context.expect_event("page") as event_info:
            await page.locator("//*[@id='formVeiculo']/div[4]/input[2]").click()
        page2 = await event_info.value
        
        try: 
            await page2.locator("#cmbTipoDebito").select_option("Integral")
            have_debits = True
            print("Achei")
        except:
            have_debits = False
            print("Not have select")
        
        # print(page2.frame_locator)
        if have_debits == True:
            url = await page2.inner_html(
                            '//*[@id="div_servicos_Autuacoes"]/table/tbody/tr[2]/td[2]')
            # soup = BeautifulSoup(url, 'html.parser')
            # debitos = soup.find_all(
            #                 'td', attrs={'class': False, 'width': False, 'colspan': False})
            debito = extractor_infracoes_em_autuacao(url)
            print(debito['local'], debito['data'])
            data = re.search('(\\d{2}\\/\\d{2}\\/\\d{4})', debito['data']).group(0)
            hora = re.search('(\\d{2}\\:\\d{2})', debito['data']).group(0)
            acres_hour_for_connecta(hora)
            print(hora)
            # print("Debitos localizados --->> ", debitos)
        time.sleep(10)
        await browser.close()

asyncio.run(main())