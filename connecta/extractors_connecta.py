import re
from bs4 import BeautifulSoup


async def extractor_connecta(url):
    newSoup = BeautifulSoup(url, 'html.parser')
    nome = newSoup.find_all(
        'td', attrs={'style': 'text-align: center'}, string=re.compile(r"[A-Z]"))
    contador = 0
    while contador < len(nome):
        infrator = nome[contador].text
        if re.search(r"[a-z]", infrator) == None and re.search("CEP", infrator) == None:
            nomeInfrator = infrator
        contador += 1
    return nomeInfrator
