import asyncio
import os
import re
import time
from turtle import delay
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from buscadorConnecta import connecta_actions

from extractor_detran import extractor_infracoes_em_autuacao
from utils.acresHourConnecta import hour_for_connecta
from excelGenerator import excel_generator

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
        except:
            have_debits = False
        
        if have_debits == True:
            url = await page2.inner_html(
                            '//*[@id="div_servicos_Autuacoes"]/table/tbody/tr[2]/td[2]')
            
            debito = extractor_infracoes_em_autuacao(url)
            hours = hour_for_connecta(debito)
            connecta = await context.new_page()
            placa = "(QCW-4251)"
            print(debito['local'], debito['data'])
            condutor = await connecta_actions(connecta, hours=hours, placa=placa)
            await excel_generator(placa=placa, multa=debito['local'], local_data=debito['data'], condutor=condutor)
            # await connecta.keyboard.press("Tab")
            # await connecta.locator("#dtI").click()
            # await connecta.locator("#dtI").press("Control+KeyA")
            # await connecta.locator("#dtI").press("Delete")
            # await connecta.locator("#dtI").type(hours["date_hour"], delay=100)
            # await connecta.locator("#dtI").click()
            # await connecta.locator("#dtF").press("Control+KeyA")
            # await connecta.locator("#dtF").press("Delete")
            # await connecta.locator("#dtF").type(hours["date_hour_acres"], delay=100)
            # await connecta.locator("#dtI").dblclick()
            # await connecta.keyboard.press("Control+a")
            # await connecta.locator("#dtI").fill(hours["date_hour"], no_wait_after=True, force=True)
            # await connecta.locator("#dtI").fill("")
            # await connecta.keyboard.press("Control+a")
            # await connecta.keyboard.insert_text(hours["date_hour"])
            # time.sleep(1)
            # await connecta.keyboard.press("Enter")
            # await connecta.locator("#dtF").dblclick()
            # await connecta.keyboard.press("Control+a")
            # await connecta.locator("#dtF").fill(hours["date_hour_acres"], no_wait_after=True, force=True)
            # await connecta.locator("#dtF").fill("")
            # await connecta.keyboard.press("Control+a")
            # await connecta.keyboard.insert_text(hours["date_hour_acres"])
            time.sleep(1)
            await connecta.keyboard.press("Enter")
            await connecta.keyboard.press("Tab")
        time.sleep(10)
        await browser.close()

asyncio.run(main())