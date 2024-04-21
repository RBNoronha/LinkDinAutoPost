# [:calendar: Linkedin AutoPost - Automatize suas postagens no LinkedIn e Telegram!](LinkedinTelegramPostScheduleV5.py)



## Índice

- [Introdução](#introdução)
- [Funcionalidades](#star-funcionalidades)
- [Como usar](#hammer_and_wrench-como-usar)
- [Requisitos](#page_with_curl-requisitos)
- [Notas](#memo-notas)
- [Autor](#bust_in_silhouette-autor)

## Introdução

Este script em Python :snake: foi desenvolvido para automatizar o agendamento de postagens no LinkedIn e no Telegram. Ele permite que você programe suas postagens com antecedência, economizando tempo e esforço. 

## :star: Funcionalidades

1. **Agendamento de postagens**: O script permite que você agende suas postagens no LinkedIn e no Telegram para serem publicadas em um horário específico. Isso é útil para manter uma presença consistente nas redes sociais, mesmo quando você não está disponível para fazer as postagens manualmente.

2. **Texto Persornalizado**:  

2. **Suporte ao LinkedIn**: O script utiliza a API do LinkedIn para fazer as postagens agendadas. Ele permite que você escreva o conteúdo da postagem, adicione imagens e escolha a data e hora exatas para a publicação.

3. **Suporte ao Telegram**: Além do LinkedIn, o script também suporta o agendamento de postagens no Telegram. Ele utiliza a API do Telegram para fazer as postagens agendadas. Você pode escrever o conteúdo da postagem e escolher a data e hora exatas para a publicação.

4. **Configurações personalizáveis**: O script permite que você personalize as configurações de acordo com suas necessidades. Você pode definir o caminho do arquivo de configuração, onde você pode armazenar suas credenciais de API e outras configurações específicas.

5. **Interface de linha de comando**: O script possui uma interface de linha de comando simples e intuitiva. Ele permite que você execute o script e agende suas postagens com apenas alguns comandos.


## :hammer_and_wrench: Como usar

1. Certifique-se de ter o Python instalado em seu sistema.

2. Faça o download do repositorio para o seu computador.

   ```bash
   git clone https://github.com/RBNoronha/LinkDinAutoPost.git

   cd LinkDinAutoPost
   ```

3. Instale as bibliotecas.

   ```bash
   pip install -r requirements.txt
   ```

4. Abra o terminal ou prompt de comando e execute o script `LinkedinTelegramPostScheduleV5.py` para iniciar.

   ```bash
   python LinkedinTelegramPostScheduleV5.py
   ```

5. :computer: Siga as instruções na interface de linha de comando para agendar suas postagens no LinkedIn e no Telegram.

## :page_with_curl: Requisitos

- :snake: Python 3.x
- :books: Bibliotecas Python: asyncio, json, os, re, time, uuid, calendar, datetime, aiohttp, feedparser, openai, pytz, requests, telepot

## :memo: Notas

- :key: Certifique-se de ter as credenciais de API corretas para o LinkedIn e o Telegram antes de usar o script.
- :computer: Este script foi testado em sistemas Windows e Linux. Pode haver diferenças na execução em outros sistemas operacionais.

## :bust_in_silhouette: Autor

Este script foi desenvolvido por Renan Besserra. :octocat: Sinta-se à vontade para contribuir, relatar problemas ou enviar solicitações de recursos.# LinkedinTelegramPostScheduleV5.py
