import time
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 1. CONFIGURA O HANDLER PARA NO MÁXIMO 5MB POR ARQUIVO E MANTÉM ATÉ 3 ARQUIVOS AANTIFOS
handler = RotatingFileHandler(
    'monitor_indicadores_firefox.log', 
    maxBytes=5*1024*1024, # 5 Megabytes
    backupCount=3         # Mantém os últimos 3 logs
)

logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

# 2. CONFIGURAÇÕES GERAIS
SLA = "https://sisloc.zendesk.com/explore/studio#/dashboards/CEEA2DCEA89639D726481DAC698F73220CF13D1C75DD196EA5B9EFED3BBA8892"
SOLICITACOES = "https://sisloc.zendesk.com/explore/studio#/dashboards/0750661411479DDCD82D3BDFC39D091ED2940BEC794DE502DE6F25787DB050AB"
GERAL = "http://sisloctestefab:8080/"
MONITOR_ACESSO = "http://aqs:8090/"
GERADOR_VERSAO = "http://172.19.1.84:8090/"
HORA_INICIO = "07:45" 
HORA_PARADA = "18:15" 
TEMPO_ALTERNANCIA = 60

# 3. LOOP DE ESPERA (HORÁRIO DE INÍCIO)
print(f"Aguardando o horário de início ({HORA_INICIO})...")
while True:
    hora_agora = datetime.now().strftime("%H:%M")
    if hora_agora >= HORA_INICIO:
        logging.info(f"Horário atingido! Iniciando dashboards às: {hora_agora}")
        print(f"Horário atingido! Iniciando dashboards às {hora_agora}...") 
        break
    time.sleep(60) # Verifica a cada 60 segundos para não sobrecarregar o PC

# 4. CONFIGURAÇÕES PARA EVITAR ERROS NA JANELA
chrome_options = Options()
chrome_options.add_argument("--kiosk") # Inicia em modo tela cheia total (mais estável que o comando fullscreen)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--remote-debugging-port=9222") # Essa opção ajuda o Selenium a manter o controle exclusivo desta instância
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Remove o aviso de "automação"

# 5. INICIALIZA O CHROME
print("Iniciando o Google Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 6. ABRE A PRIMEIRA ABA COM O DASHBOARD DE SLA
    # logging.info("Carregando Dashboard de SLA...") 
    # print("Carregando Dashboard de SLA...")    
    # driver.get(SLA)
    # time.sleep(5)

    # 7. ABRE A SEGUNDA ABA COM O DASHBOARD DE SOLICITAÇÕES
    # print("Carregando Dashboard de Solicitações...")
    # driver.execute_script(f"window.open('{SOLICITACOES}', '_blank');")
    # time.sleep(5)

    # 7.1 ABRE A TERCEIRA ABA COM O DASHBOARD GERAL
    logging.info("Carregando Dashboard Geral...") 
    print("Carregando Dashboard Geral...")
    driver.get(GERAL)
    time.sleep(5) # Tempo para o primeiro carregamento

    # 7.2 ABRE A QUARTA ABA COM O DASHBOARD MONITOR DE ACESSO
    # print("Carregando Dashboard de Monitor de Acesso...")
    # driver.execute_script(f"window.open('{MONITOR_ACESSO}', '_blank');")
    # time.sleep(5)  

    # 7.3 ABRE A QUINTA ABA COM O DASHBOARD GERADOR DE VERSÃO
    print("Carregando Dashboard de Gerador de Versão...")
    driver.execute_script(f"window.open('{GERADOR_VERSAO}', '_blank');")
    time.sleep(5)      


    abas = driver.window_handles
    logging.info(f"Abas identificadas com sucesso: {len(abas)} abas.")

    # 8. VERIFICA SE AS ABAS FORAM CAPTURADASANTES DE CONTINUAR
    if not abas or len(abas) < 2:
        print("Erro: Não foi possível identificar as duas abas.")
        driver.quit()
        exit()

    print(f"Sistema pronto. Alternando abas até às {HORA_PARADA}. Pressione Ctrl+C para interromper manualmente.")

    # 9. LOOP DE DE ALTERNÂNCIA COM VERIFICAÇÃO DE HORÁRIO
    while True:
        hora_atual = datetime.now().strftime("%H:%M")

        if hora_atual >= HORA_PARADA:
            logging.info(f"Horário de parada atingido, expediente sendo encerrado: {hora_atual}. Fechando abas...") 
            print(f"Horário de parada atingido, expediente sendo encerrado ({hora_atual}).")
            break

        # 10. VERIFICA SE CHEGOU A  HORA DE ENCERRAR
        if hora_atual >= HORA_PARADA:
            print(f"Horário de encerramento atingido ({hora_atual}). Finalizando aplicação...")
            break        
            
            # 11. FECHA A ABA 2 (SOLICITAÇÕES)
            driver.switch_to.window(abas[1])
            driver.close()
            time.sleep(1) # Pequena pausa para o navegador processar
            
            # 12. FECHA A ABA 1 (SLA)
            driver.switch_to.window(abas[0])
            driver.close()
            
            print("Abas fechadas. Encerrando aplicação...")
            break # Sai do loop para ir para o driver.quit()

        try:
            # 13. ALTERNA PARA A ABA 1
            driver.switch_to.window(abas[0])
            print(f"[{hora_atual}] Exibindo: SLA")
            time.sleep(TEMPO_ALTERNANCIA)

            # 14. ALTERNA PARA A ABA 2
            driver.switch_to.window(abas[1])
            print(f"[{hora_atual}] Exibindo: Solicitações")
            time.sleep(TEMPO_ALTERNANCIA)     

        except Exception as e: 
            logging.error(f"Erro durante a alternância de abas: {e}")
            time.sleep(5) # Espera um pouco antes de tentar a próxima volta
       
except Exception as e:
    logging.critical(f"Erro crítico no sistema: {e}")

finally:
    logging.info("Executando limpeza final do driver.")

    print("Encerrando a automação...")
    try:
        # 15. VERIFICA SE O DRIVER AINDA ESTÁ ATIVO ANTES DE TENTAR FECHAR AS ABAS
        if driver:
            handles = driver.window_handles # Pega as abas abertas
            for aba in handles:
                driver.switch_to.window(aba)
                driver.close()
            driver.quit()
    except Exception:
        # 16. SE O NAVEGADOR JÁ FOI FECHADO MANUALEMTEN, ELE CAI AQUI E IGNORA O ERRO
        print("O navegador já estava fechado ou a conexão foi perdida.")
    
    print("Processo finalizado.")  