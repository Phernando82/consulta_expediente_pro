import csv
from logging import PlaceHolder
import PySimpleGUI as sg
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from anticaptchaofficial.recaptchav2proxyless import *
from chave import solver_key
from site_url import url
import csv
from csv import writer
from datetime import datetime, date


def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=800,600', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)
        
    chrome_options.add_experimental_option('prefs', {
        # Desabilitar a confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos downloads
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    # Precisamos definir os parâmetros dentro da função 
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1, # em quanto tempo ele vai tentar
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )
    
    return driver, wait # retornar as configurações de wait


def buscar_dados(url, nie, numero, ano):
    print(nie)
    print(numero)
    print(ano)
    print('A buscar')
    driver, wait = iniciar_driver()
    driver.get(url)
    driver.maximize_window()
    sleep(2)
    campo_nie = driver.find_element(By.ID,'codigoNieCompleto')
    campo_nie.send_keys(nie)
    sleep(2)
    campo_numero = driver.find_element(By.ID,'numero')
    campo_numero.send_keys(numero)
    sleep(2)
    campo_ano = driver.find_element(By.ID,'yearSolicitud')
    campo_ano.send_keys(ano)
    sleep(5)
    site_key = driver.find_element(By.XPATH,'//*[@id="captchaTramite"]/div/div/div').get_attribute('outerHTML')
    sitekey_clean = site_key.split('" data-expired-callback')[0].split('data-sitekey="')[1]
    print(sitekey_clean)
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(solver_key)
    solver.set_website_url(url)
    solver.set_website_key(sitekey_clean) 
    g_response = solver.solve_and_return_solution()

    if g_response!= 0:
        print(f'g_response:{g_response}')
        driver.execute_script(f'document.getElementById("g-recaptcha-response").value="{g_response}"')
        sleep(15)
        # driver.find_element(By.XPATH, '//*[@id="recaptcha-demo-submit"]').click()
    else:
        print(f'Task finished with error: {solver.err_string}')              
    sleep(5)
    botao_enviar = driver.find_element(By.ID,'submitNac')
    botao_enviar.click()
    sleep(5)
    dados = driver.find_elements(By.XPATH,'//div[@id="consulta_telematica_expedientes_nacionalidad_española_residencia"]/div/div[2]/p/b')# /p[5]/b/text()
    sleep(5)
    expediente = []
    for dado in dados:
        print(dado.text)
        expediente.append(dado.text)
    data = date.today()
    data = data.strftime('-%d-%m-%Y')
    with open(f'expedientes{data}.csv', 'a', encoding='utf-8', newline='') as csvfile:
        expedientes = csv.reader(csvfile, delimiter=',', quotechar='|')
        writer_object = writer(csvfile)
        writer_object.writerow(expediente)
    sleep(10)
    driver.close()


def buscar_todos():
    with open('datos.csv', newline='') as csvfile:        
        clientes = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(clientes)
        for row in clientes:
            nombre = str((row[0]))
            nie = str((row[1]))
            numero = str((row[2]))
            ano = str((row[3]))
            buscar_dados(url,nie,numero,ano)
    

if __name__ == '__main__':
    buscar_todos()


       