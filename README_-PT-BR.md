# [:calendar: Linkedin AutoPost - Automatize suas postagens no LinkedIn e Telegram!](LinkedinTelegramPostScheduleV5.py)

## :page_facing_up: Introdução

:snake: Este script em Python executa um bot do Telegram projetado para automatizar a postagem de notícias e artigos no LinkedIn. Ele utiliza feeds RSS para coletar notícias, gera resumos usando a API do Azure OpenAI, e posta ou agenda postagens no LinkedIn. Este bot é uma ferramenta poderosa para profissionais que desejam manter sua rede atualizada com as últimas notícias do setor, sem o esforço manual de escrever cada postagem.

## :books: Índice
1. [Introdução](#page_facing_up-introdu%C3%A7%C3%A3o)
2. [Funcionalidades](#star-funcionalidades)
3. [Processo de Geração de Resumos](#bulb-processo-de-gera%C3%A7%C3%A3o-de-resumos)
   1. [Seleção de Conteúdo](#1-seleção-de-conteúdo)
   2. [Extração de Conteúdo](#2-extração-de-conteúdo)
   3. [Limpeza de Conteúdo](#3-limpeza-de-conteúdo)
   4. [Tradução (Opcional)](#4-tradução-opcional)
   5. [Geração de Resumo](#5-geração-de-resumo)
   6. [Formatação para Postagem](#6-formatação-para-postagem)
   7. [Tecnologias Envolvidas](#7-tecnologias-envolvidas)
4. [Benefícios](#rocket-benef%C3%ADcios)
5. [Configuração](#hammer_and_wrench-configura%C3%A7%C3%A3o)
6. [Uso](#rocket-uso)
7. [Notas](#memo-notas)
8. [Autor](#bust_in_silhouette-autor)

## :star: Funcionalidades

### 1. **Seleção de Feeds RSS**:
-   Escolha entre diversos feeds RSS para obter notícias e artigos.

### 2. **Geração Automática de Resumos**:
-   Utiliza a API do Azure OpenAI para gerar resumos concisos e relevantes dos artigos.

### 3. **Postagem e Agendamento no LinkedIn**:
-   Permite postar imediatamente ou agendar postagens no LinkedIn, incluindo a seleção de data e hora.

### 4. **Suporte a Múltiplas Línguas**: 
-   Traduz títulos e conteúdos para o português antes da geração do resumo, utilizando a biblioteca googletrans.

### 5. **Interface Interativa**: 
-   Oferece uma interface de usuário amigável no Telegram para fácil navegação e operação.

### 6. **Atualizações de Feeds em Tempo Real**:
-   Verifica atualizações nos feeds RSS selecionados e notifica o usuário sobre novos artigos disponíveis.

## :bulb: Processo de Geração de Resumos

### 1. **Seleção de Conteúdo**

-   O usuário seleciona um feed RSS de interesse, e o bot recupera os artigos mais recentes disponíveis nesse feed.


### 2. **Extração de Conteúdo**

-   Para cada artigo selecionado, o bot extrai o conteúdo principal, incluindo título e corpo do texto. Em alguns casos, também são extraídas as tags Open Graph para obter imagens e descrições mais precisas.


### 3. **Limpeza de Conteúdo**

-   O conteúdo extraído passa por um processo de limpeza para remover tags HTML, caracteres especiais e outros elementos que podem interferir na qualidade do resumo.


### 4. **Tradução (Opcional)**

-   Se necessário, o conteúdo é traduzido para o idioma desejado usando a biblioteca `googletrans`. Esta etapa é importante para garantir que o resumo seja gerado no idioma preferido do usuário.


### 5. **Geração de Resumo**

-   O conteúdo limpo e, se aplicável, traduzido é enviado para a API do Azure OpenAI. Utilizando modelos avançados de linguagem, como o GPT-4 do Azure OpenAI, a API gera um resumo conciso do artigo. Este resumo é otimizado para capturar os pontos principais do conteúdo, mantendo a coerência e a relevância, utilizando um modelo postagem.


### 6. **Formatação para Postagem**

-   O resumo gerado é então formatado de acordo com as melhores práticas de postagem no LinkedIn, incluindo a adição de emojis, hashtags relevantes e uma questão provocativa no final para incentivar o engajamento.


### 7. **Tecnologias Envolvidas**

- **Feedparser**: Utilizado para parsear os feeds RSS e extrair os artigos.
- **BeautifulSoup**: Auxilia na limpeza do conteúdo HTML dos artigos.
- **Googletrans**: Biblioteca para tradução automática de textos.
- **Azure OpenAI API**: Fornece acesso aos modelos de linguagem GPT-4 para a geração de resumos. A escolha dessa API se deve à sua capacidade de entender e sintetizar informações complexas de forma coerente e concisa.


## :rocket: Benefícios

- **Eficiência**: Automatiza o processo de leitura e síntese de informações, economizando tempo.
- **Consistência**: Mantém um padrão de qualidade nos resumos, independentemente do volume de conteúdo processado.
- **Engajamento**: Resumos bem elaborados e formatados de acordo com as diretrizes do LinkedIn podem aumentar o engajamento com o conteúdo postado.
- **Acessibilidade**: Torna mais fácil para os profissionais compartilharem conhecimento e informações relevantes com sua rede, independentemente de barreiras linguísticas ou de tempo.

A geração automática de resumos representa um avanço significativo na forma como os profissionais interagem com e disseminam informações em plataformas de rede profissional como o LinkedIn. Ao aproveitar o poder da inteligência artificial e do processamento de linguagem natural, este bot oferece uma solução eficaz para manter uma presença ativa e informativa online.


## :hammer_and_wrench: Configuração

1. Certifique-se de ter o Python instalado em seu sistema.

2. Faça o download do repositorio para o seu computador.

   ```bash
   git clone https://github.com/RBNoronha/LinkDinAutoPost.git

   cd LinkDinAutoPost
   ```


3. Configure as seguintes credenciais no arquivo `config.py`:

- **Token do Bot do Telegram:**: Obtenha um token criando um bot no Telegram através do BotFather.

   ```bash
   TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
   ```

- **Chaves de API do Azure OpenAI**: Cadastre-se no Azure e crie uma instância do OpenAI para obter suas chaves de API.
   ```base
   AZURE_API_KEY = "YOUR_AZURE_OPENAI_API_KEY"
   AZURE_API_BASE = "YOUR_AZURE_OPENAI_API_BASE"
   GPT_MODEL_32K: = "YOUR_NAME_MODEL_AZURE"
   GPT_MODEL_TURBO = "YOUR_NAME_MODEL_AZURE"
   ```
- **Token de Acesso do LinkedIn**: Crie um aplicativo no LinkedIn e obtenha um token de acesso OAuth2.
   ```bash
   ACCESS_TOKEN: "YOUR_TOKEN_OAUTH2_LINKEDIN"
   ```

4. Configure o arquivo de configuração de logging no arquivo `logging_config.py`:

   ```python
   import logging

   # Create a custom logger
   logger = logging.getLogger(__name__)

   # Set the default logging level
   logger.setLevel(logging.INFO)

   # Create handlers
   console_handler = logging.StreamHandler()
   file_handler = logging.FileHandler('bot.log')

   # Set the logging level for handlers
   console_handler.setLevel(logging.INFO)
   file_handler.setLevel(logging.INFO)

   # Create formatters and add them to handlers
   console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   file_format = logging.Formatter('%(asctime)s - %(name)s - %(levellevel)s - %(message)s')

   console_handler.setFormatter(console_format)
   file_handler.setFormatter(file_format)

   # Add handlers to the logger
   logger.addHandler(console_handler)
   logger.addHandler(file_handler)
   ```

5. Instale as bibliotecas.

   ```bash
   pip install -r requirements.txt
   ```


6. Abra o terminal ou prompt de comando e execute o script `LinkedinTelegramPostScheduleV5.py` para iniciar.

   ```bash
   python LinkedinTelegramPostScheduleV5.py
   ```


## :rocket: Uso

Interaja com o bot através do Telegram. O bot oferece uma interface interativa para escolher feeds RSS, visualizar notícias, gerar resumos e postar ou agendar postagens no LinkedIn.                        


## :memo: Notas

- :key: Certifique-se de ter as credenciais de API corretas para o LinkedIn e o Telegram antes de usar o script.
- :computer: Este script foi testado em sistemas Windows e Linux. Pode haver diferenças na execução em outros sistemas operacionais.

## :bust_in_silhouette: Autor

Este script foi desenvolvido por Renan Besserra. :octocat: Sinta-se à vontade para contribuir, relatar problemas ou enviar solicitações de recursos.# LinkedinTelegramPostScheduleV5.py
