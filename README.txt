#### Lista de comando e libs ####

1 - Instalar Anaconda 3  (baixar no site: "https://www.anaconda.com/")

2 - No prompt do anaconda:
                                         --
                                        |$ pip install --upgrade pyautogui 
                                        |$ pip install --upgrade beautifulsoup4
                                        |$ pip install --upgrade pandas
    Bibliotecas a serem instaladas ---> |$ pip install --upgrade openpyxl
                                        |$ pip install --upgrade opencv-python
                                        |$ pip install --upgrade pip install pytest-playwright
                                         --
    $ playwright install ("comando para instalar e instânciar os drivers do navegador e colocar em modo anônimo") 
     

3 - Navegar até a pasta onde o script está localizado ("localizar a pasta onde está o script arquivo '.py' " ---> ex: "C:\Users\seu_usuário\documents\consulta_de_multas")

4 - $ Python <Nome_do_script>.py  (ex: $ Python Buscador.py ---> "Comando para rodar o script")

5 - Em seguida será aberta a janela com o navegador e as consultas sendo executadas --->> IMPORTANTE: NÃO DIGITE NENHUMA TECLA OU MOVIMENTE O MOUSE DURANTE A EXECUÇÃO,
PORQUE PODE NÃO FUNCIONAR CORRETAMENTE E/OU ALTERAR OS RESULTADOS  ---> Caso queira parar a execução é só segurar "CTRL + C" no terminal e a execução será encerrada.


OBS: NÃO ALTERAR A LOCALIZAÇÃO DAS PASTAS E ESTRUTURAS DOS ARQUIVOS, PORQUE O SCRIPT FAZ A BUSCA DOS ARQUIVOS NA RAIZ DO DIRETÓRIO ONDE ESTÁ LOCALIZADO