import os
import re
import time
from playwright.async_api import Page
from dotenv import load_dotenv

from extractor_connecta import extractor_connecta

load_dotenv()

async def connecta_actions(page: Page, hours, placa) -> None:
    await page.goto(
                os.environ['CONNECTA'])
    await page.locator(
        "input[name='usuario']").fill(os.environ['USER_NAME'])
    await page.locator(
        "input[name='senha']").fill(os.environ['PASSWORD'])
    time.sleep(1)
    await page.locator(
        "button[name='Submit']").click()
    await page.locator(
                            "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/a").hover()
    await page.locator(
        "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/ul/li[1]/a").hover()
    await page.locator(
        "a[href='controlerelatoriodeslocamento']").click()
    await page.locator(
        "//*[@id='formfiltro']/fieldset/span[1]/button").click()
    await page.locator(
        "//div[4]/div/div/input").fill(placa)
    time.sleep(1)
    await page.locator("//div[4]/ul/li[6]/label/span", has_text=re.compile(placa)).click()
    await page.keyboard.press("Tab")
    await page.locator("#dtI").click()
    await page.locator("#dtI").press("Control+KeyA")
    await page.locator("#dtI").press("Delete")
    await page.locator("#dtI").type(hours["date_hour"], delay=10)
    await page.locator("#dtI").click()
    await page.locator("#dtF").press("Control+KeyA")
    await page.locator("#dtF").press("Delete")
    await page.locator("#dtF").type(hours["date_hour_acres"], delay=10)
    await page.locator(
                                    "//*[@id='formfiltro']/fieldset/div/button[2]").click()
    
    url = await page.inner_html(
                                            "//body/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr")
    
    infrator = await extractor_connecta(url)
    return infrator