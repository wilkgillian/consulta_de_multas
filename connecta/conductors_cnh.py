import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import BrowserContext, Page

from connecta.extractors_connecta import extractor_condutores
from utils.excelGenerator import excel_generator_condutores

load_dotenv()


async def conductors_cnh(page: Page, path: str):
    await page.goto(os.environ['CONNECTA'])
    await page.locator(
        "input[name='usuario']").fill(os.environ['USER_NAME'])
    await page.locator(
        "input[name='senha']").fill(os.environ['PASSWORD'])
    await page.locator(
        "button[name='Submit']").click()
    await page.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/a").hover()
    await page.locator(
        "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/ul/li[2]/a").click()
    url = await page.inner_html(
        '//*[@id="box-table-b"]/tbody/tr[16]/th/form')
    soup = BeautifulSoup(url, 'html.parser')
    next_page = soup.find('a').get('href')

    url_to_extract = page.inner_html('//*[@id="box-table-b"]/tbody')

    while next_page is not None:
        try:
            page.set_default_timeout(2000)
            await extractor_condutores(url=url_to_extract, path=path)
            page.locator(
                "//*[@id='box-table-b']/tbody/tr[16]/th/form/a", has_text="Próxima").click()
        except:
            next_page = None
    await page.close()
    pass
