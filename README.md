🚀 Novo projeto publicado no GitHub!

Recentemente subi para o repositório um projeto de automação de dashboards, desenvolvido em Python.
A aplicação abre o Zendesk em abas do Google Chrome / Mozilla Firefox e alterna entre elas em intervalos definidos, garantindo monitoramento contínuo e automatizado.

🐍 Linguagem
Python: todo o script foi construído em Python, aproveitando tanto módulos nativos quanto bibliotecas externas.

📦 Bibliotecas da standard library
time → controle de pausas e intervalos.
datetime → captura e formatação de horários, definindo início e término da execução.
logging + RotatingFileHandler → registro estruturado de logs, com rotação automática de arquivos (até 5 MB cada, mantendo 3 históricos).

🌐 Bibliotecas externas
selenium → automação de navegador (abertura de abas, alternância e execução de scripts).
webdriver_manager → gerenciamento automático do ChromeDriver.
Configurações avançadas do Chrome via Options e Service para maior estabilidade e controle da execução.

🔗 Integração com serviços externos
O script acessa dashboards do Zendesk diretamente via navegador, permitindo acompanhamento em tempo real.
Embora não consuma APIs REST/JSON, realiza integração prática com aplicações web por meio de automação.

✅ Resumo das tecnologias
Linguagem: Python
Biblioteca padrão: time, datetime, logging
Bibliotecas externas: selenium, webdriver_manager
Integração web: dashboards do Zendesk via navegador

Esse projeto mostra como é possível unir automação de processos, monitoramento inteligente e boas práticas de logging para criar soluções simples e eficazes.
