import asyncio
import json
import os
import re
import time
import uuid
from calendar import monthrange
from datetime import date, datetime, timedelta
import aiohttp
import feedparser
import openai
import pytz
import requests
import telepot
import telepot.aio
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from googletrans import Translator
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from pytz import timezone


# Variáveis globais para armazenar feeds RSS e artigos

feed_updates = {}
global_articles = None
global_jobs = {}
last_check_dates = {}

# Caminho para o arquivo de última verificação
LAST_CHECK_FILE = "last_check.json"

# Função para remover tags HTML
def remove_html_tags(text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)

# Configurações do Azure OpenAI RBLN
openai.api_type = "azure"
openai.api_base = "YOUR_AZURE_OPENAI_API_BASE"
openai.api_version = "2023-07-01-preview"
openai.api_key = "YOUR_AZURE_API_KEY"

# Configurações do Azure OpenAI RBLN
RBLN_API_BASE = "YOUR_AZURE_OPENAI_API_BASE"
RBLN_API_KEY = "YOUR_AZURE_API_KEY"

# Configurações do Azure OpenAI para redundância
RBPS_API_BASE = "YOUR_AZURE_OPENAI_API_BASE"
RBPS_API_KEY = "YOUR_AZURE_API_KEY"

# Modelo de linguagem GPT criado no Azure OpenAI
GPT_MODEL_32K = "gpt-4-32k"
GPT_MODEL_TURBO = "gpt-4-preview"


def set_openai_config(api_base, api_key):
    openai.api_type = "azure"
    openai.api_base = api_base
    openai.api_version = "2023-07-01-preview"
    openai.api_key = api_key


# API para as configurações do Telegram e LinkedIn
TELEGRAM_TOKEN = "YOURTOKEN"
ACCESS_TOKEN = "YOUTYOKEN"

feed_urls = {
    "/startcustomblog": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-177205926965371099&size=65",
    "/startinfrastructure": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=5272649121701694560&board=CoreInfrastructureandSecurityBlog&size=25",
    "/startazureaiservices": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=3287690017842470215&board=Azure-AI-Services-blog&size=25",
    "/startmicrosoft365": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-7424720648213528660&board=microsoft_365blog&size=25",
    "/startserverless": "https://serverless360.com/feed/",
    "/startnielskok": "https://www.nielskok.tech/feed",
    "/startEducatordeveloper": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-3610219301967395228&board=EducatorDeveloperBlog&size=25",
    "/startlandingpage": "https://devblogs.microsoft.com/landingpage/",
    "/startcommandline": "https://devblogs.microsoft.com/commandline/feed/",
    "/startmikefrobbins": "https://mikefrobbins.com/index.xml",
    "/azuregovernanceandmanagement": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=AzureGovernanceandManagementBlog&size=25",
    "/microsoftentra": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=Identity&size=25",
    "/infrastructuresecurity": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=CoreInfrastructureandSecurityBlog&size=25",
    "/securitycomplianceidentity": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=MicrosoftSecurityandCompliance&size=25",
    "/fasttrackforazure": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=FastTrackforAzureBlog&size=25",
    "/appsonazureblog": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=AppsonAzureBlog&size=25",
    "/windowsitpro": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=Windows-ITPro-blog&size=25",
    "/itopstalkblog": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=ITOpsTalkBlog&size=25",
    "/adamtheautomator": "https://adamtheautomator.com/feed/",
    "/thelazyadministrator": "https://www.thelazyadministrator.com/feed/",
    "/powershellcommunity": "https://devblogs.microsoft.com/powershell-community/feed/",
    "/powershellteam": "https://devblogs.microsoft.com/powershell/feed/",
    "/practical365": "https://practical365.com/feed/",
    "/lukegeek": "https://luke.geek.nz/rss",
    "/wedoazure": "https://wedoazure.ie/feed/",
    "/charbelnemnom": "https://charbelnemnom.com/feed/",
    "/powershellisfun": "https://powershellisfun.com/feed/",
    "/azureappService": "https://azure.github.io/AppService/feed.xml",
    "/azureappService": "https://azure.github.io/AppService/feed.xml",
    "/plainenglishai": "https://ai.plainenglish.io/feed",
    "/azurefeeds": "https://azurefeeds.com/feed/",
    "/lazyadmin": "https://lazyadmin.nl/feed/",
    "/planetpowershell": "https://www.planetpowershell.com/feed",
    "/natehutchinson": "https://www.natehutchinson.co.uk/blog-feed.xml",
    "/ourcloudnetwork": "https://ourcloudnetwork.com/feed/",
    "/techielass": "https://www.techielass.com/rss/",
    "/oceanleaf": "https://oceanleaf.ch/rss/",
    "/microsoftlearn": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=2385852509875677505&board=MicrosoftLearnBlog&size=50",
    "/prajwaldesai": "https://www.prajwaldesai.com/feed/",
    "/admindroid": "https://blog.admindroid.com/feed/",
    "/danielchronlund": "https://danielchronlund.com/feed/",
    "/cswrld": "https://www.cswrld.com/feed/",
    "/cloudarchitekt": "https://www.cloud-architekt.net/feed",
    "/office365itpros": "https://office365itpros.com/feed/",
    "/emsroute": "https://emsroute.com/feed/",
    "/suryendub": "https://suryendub.github.io/feed",
    "/cloudbrothers": "https://cloudbrothers.info/index.xml",
}

feed_urls = {
    "/startcustomblog": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-177205926965371099&size=65",
    "/startinfrastructure": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=5272649121701694560&board=CoreInfrastructureandSecurityBlog&size=25",
    "/startazureaiservices": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=3287690017842470215&board=Azure-AI-Services-blog&size=25",
    "/startmicrosoft365": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-7424720648213528660&board=microsoft_365blog&size=25",
    "/startserverless": "https://serverless360.com/feed/",
    "/startnielskok": "https://www.nielskok.tech/feed",
    "/startEducatordeveloper": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-3610219301967395228&board=EducatorDeveloperBlog&size=25",
    "/startlandingpage": "https://devblogs.microsoft.com/landingpage/",
    "/startcommandline": "https://devblogs.microsoft.com/commandline/feed/",
    "/startmikefrobbins": "https://mikefrobbins.com/index.xml",
    "/azuregovernanceandmanagement": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=AzureGovernanceandManagementBlog&size=25",
    "/microsoftentra": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=Identity&size=25",
    "/infrastructuresecurity": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=CoreInfrastructureandSecurityBlog&size=25",
    "/securitycomplianceidentity": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=MicrosoftSecurityandCompliance&size=25",
    "/fasttrackforazure": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=FastTrackforAzureBlog&size=25",
    "/appsonazureblog": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=AppsonAzureBlog&size=25",
    "/windowsitpro": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=Windows-ITPro-blog&size=25",
    "/itopstalkblog": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=-5120206136278231098&board=ITOpsTalkBlog&size=25",
    "/adamtheautomator": "https://adamtheautomator.com/feed/",
    "/thelazyadministrator": "https://www.thelazyadministrator.com/feed/",
    "/powershellcommunity": "https://devblogs.microsoft.com/powershell-community/feed/",
    "/powershellteam": "https://devblogs.microsoft.com/powershell/feed/",
    "/practical365": "https://practical365.com/feed/",
    "/lukegeek": "https://luke.geek.nz/rss",
    "/wedoazure": "https://wedoazure.ie/feed/",
    "/charbelnemnom": "https://charbelnemnom.com/feed/",
    "/powershellisfun": "https://powershellisfun.com/feed/",
    "/azureappService": "https://azure.github.io/AppService/feed.xml",
    "/azureappService": "https://azure.github.io/AppService/feed.xml",
    "/plainenglishai": "https://ai.plainenglish.io/feed",
    "/azurefeeds": "https://azurefeeds.com/feed/",
    "/lazyadmin": "https://lazyadmin.nl/feed/",
    "/planetpowershell": "https://www.planetpowershell.com/feed",
    "/natehutchinson": "https://www.natehutchinson.co.uk/blog-feed.xml",
    "/ourcloudnetwork": "https://ourcloudnetwork.com/feed/",
    "/techielass": "https://www.techielass.com/rss/",
    "/oceanleaf": "https://oceanleaf.ch/rss/",
    "/microsoftlearn": "https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?tid=2385852509875677505&board=MicrosoftLearnBlog&size=50",
    "/prajwaldesai": "https://www.prajwaldesai.com/feed/",
    "/admindroid": "https://blog.admindroid.com/feed/",
    "/danielchronlund": "https://danielchronlund.com/feed/",
    "/cswrld": "https://www.cswrld.com/feed/",
    "/cloudarchitekt": "https://www.cloud-architekt.net/feed",
    "/office365itpros": "https://office365itpros.com/feed/",
    "/emsroute": "https://emsroute.com/feed/",
    "/suryendub": "https://suryendub.github.io/feed",
    "/cloudbrothers": "https://cloudbrothers.info/index.xml",
}

feed_names = {
    "Custom Blog": "/startcustomblog",
    "Infrastructure": "/startinfrastructure",
    "Azure AI Services": "/startazureaiservices",
    "Microsoft 365": "/startmicrosoft365",
    "Serverless": "/startserverless",
    "NielShok": "/startnielskok",
    "Educator Developer": "/startEducatordeveloper",
    "Landing Page": "/startlandingpage",
    "Command Line": "/startcommandline",
    "Mike F Robbins": "/startmikefrobbins",
    "Azure Governance MGMT": "/azuregovernanceandmanagement",
    "Microsoft Entra (Azure AD)": "/microsoftentra",
    "Infrastructure Security": "/infrastructuresecurity",
    "Sec, Compliance Identity": "/securitycomplianceidentity",
    "FastTrack for Azure": "/fasttrackforazure",
    "Apps on Azure Blog": "/appsonazureblog",
    "Windows IT Pro": "/windowsitpro",
    "IT OpsTalk Blog": "/itopstalkblog",
    "Adam the Automator": "/adamtheautomator",
    "The Lazy Administrator": "/thelazyadministrator",
    "PowerShell Community": "/powershellcommunity",
    "PowerShell Team": "/powershellteam",
    "Practical 365": "/practical365",
    "Luke Geek": "/lukegeek",
    "We Do Azure": "/wedoazure",
    "Charbel Nemnom": "/charbelnemnom",
    "Powershell LisFun": "/powershellisfun",
    "Azure App Service": "/azureappService",
    "Plain English AI": "/plainenglishai",
    "Azure Feeds": "/azurefeeds",
    "Lazy Admin": "/lazyadmin",
    "Planet PowerShell": "/planetpowershell",
    "Our Cloud Network": "/ourcloudnetwork",
    "Nate Hutchinson": "/natehutchinson",
    "Techie Lass": "/techielass",
    "Ocean Leaf": "/oceanleaf",
    "Microsoft Learn": "/microsoftlearn",
    "Prajwal Desai": "/prajwaldesai",
    "AdminDroid": "/admindroid",
    "Daniel Chronlund": "/danielchronlund",
    "CSWrld": "/cswrld",
    "Cloud Architekt": "/cloudarchitekt",
    "Office 365 IT Pros": "/office365itpros",
    "EMS Route": "/emsroute",
    "Suryendu B": "/suryendub",
    "Cloud Brothers": "/cloudbrothers",
}


# variáveis globais para armazenar artigos e feeds RSS selecionados pelo usuário
(
    awaiting_confirmation,
    awaiting_schedule,
    selected_article,
    summary,
    article_title,
    article_url,
    global_articles,
    translated_article_title,
    selected_day,
    selected_month,
    selected_year,
) = (None, None, None, None, None, None, None, None, None, None, None)

translator = Translator()
scheduler = BackgroundScheduler()
scheduler.start()
global_jobs = {}


# Função para obter Open Graph Tags de uma URL
def get_open_graph_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    meta_tags = soup.find_all("meta")
    og_tags = {}
    for tag in meta_tags:
        if tag.get("property", "").startswith("og:"):
            og_tags[tag["property"][3:]] = tag["content"]
    return og_tags


# Função para gerar resumo usando GPT-4-Turbo API do Azure OpenAI
def generate_summary(article_summary, article_url):
    cleaned_summary = remove_html_tags(article_summary)
    messages = [
        {
            "role": "system",
            "content": f"""Act like Linkedingpt, an advanced platform and language model designed to generate viral posts for LinkedIn, which helps users increase their number of followers and likes on LinkedIn by improving the format and interaction in LinkedIn Feed posts. Use the following rules to get the most views:

            - You are also an Expert in Azure, and Microsoft products, who will post news on LinkedIn to gain organic engagement, using techniques to gain more visibility according to the rules of the LinkedIn algorithm, I will post news in an XML RSS and you summarize in detail, according to the LinkedIn algorithm to gain more visibility.

            - Pay close attention, if the news is in English, always write the summary in BR Portuguese.

            - The first two lines must be creative, engaging, charismatic and intelligent to immediately capture the reader's attention. Start each sentence on a new line and add numbering with emoji to the first two lines for better structuring.

            - The ideal length of the summary is 1,200 and 1,500 characters (never exceed 1,500 characters), written in a professional and organized manner.

            - Use a maximum of 200 characters in each paragraph. At the end of each paragraph there will be an empty line to start the next paragraph.

            - Place an emoji at the beginning of each paragraph, which is related to the written paragraph.

            - An approach with a professional, formal and information-rich tone. Citing examples, code examples, commands or scripts.

            - When you hear commands or scripts from any programming language or framework, always indent the script, command or code separately from the text so that it remains legible and clear to the reader.

            - Structured presentation format, with paragraphs separating different points, with high specificity, always explaining in detail and, if possible, citing examples and how to do it.

            - End the post with a thought-provoking question to encourage community engagement. This should come before hashtags.

            - Always include 4 to 5 Hashtags that are related to the news released at the end of the summary.

            - PAY THIS COMMENT VERY CAREFULLY. Follow ALL of these guidelines to create a post that not only informs, but also engages and inspires, following the rules of the LinkedIn algorithm""",
        },
        {"role": "user", "content": f"Summarize the following news: {cleaned_summary}"},
    ]

    # Moodelo de linguagem GPT-4-Turbo para gerar o resumo, usando a API do Azure OpenAI, com a chave de API do Azure OpenAI RBLN e RBPSForlife, para gerar o resumo, com redundância caso uma das APIs esteja fora do ar.
    try:
        set_openai_config(RBLN_API_BASE, RBLN_API_KEY)
        response = openai.ChatCompletion.create(
            engine=GPT_MODEL_TURBO, messages=messages, temperature=0.5
        )
    except Exception as e:
        print(f"Erro com API OpenAI Primaria: {e}")
        print("Alterando para API OpenAI Secundaria..")
        set_openai_config(RBPS_API_BASE, RBPS_API_KEY)
        response = openai.ChatCompletion.create(
            engine=GPT_MODEL_TURBO, messages=messages, temperature=0.5
        )
    summary = response["choices"][0]["message"]["content"]
    return summary


# Obter URN da pessoa autenticada
ME_RESOURCE = f"https://api.linkedin.com/v2/me"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
me_response = requests.get(ME_RESOURCE, headers=headers)

if "id" not in me_response.json():
    raise Exception(
        "Erro ao obter o perfil do LinkedIn. Verifique o se o token de acesso não está expirado."
    )


# Função para postar no LinkedIn usando a API
def post_to_linkedin(title, description, url):
    owner = "urn:li:person:" + me_response.json()["id"]
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "owner": owner,
        "text": {"text": description},
        "content": {
            "contentEntities": [
                {
                    "entityLocation": url,
                    "thumbnails": [
                        {"resolvedUrl": get_open_graph_tags(url).get("image", "")}
                    ],
                }
            ],
            "title": title,
        },
        "distribution": {"linkedInDistributionTarget": {}},
    }

    # Postar no LinkedIn
    response = requests.post(
        "https://api.linkedin.com/v2/shares", headers=headers, json=payload
    )
    response_data = response.json()
    return response_data


# Função para enviar um seletor de data, divida em etapas, primeiro o dia, depois o mês e depois o ano.
async def send_datepicker(chat_id):
    now = datetime.now()
    year = now.year

    # Criar botões para cada dia do mês
    days = [
        InlineKeyboardButton(text=str(day), callback_data=f"day_{day}")
        for day in range(1, 32)
    ]

    # Criar botões para cada mês
    months = [
        [
            InlineKeyboardButton(text=str(month), callback_data=f"month_{month}")
            for month in range(1, 7)
        ],
        [
            InlineKeyboardButton(text=str(month), callback_data=f"month_{month}")
            for month in range(7, 13)
        ],
    ]

    # Criar botões para o ano atual e o próximo
    years = [
        InlineKeyboardButton(text=str(year + i), callback_data=f"year_{year+i}")
        for i in range(2)
    ]

    # Agrupar os botões em linhas
    keyboard = [days[i : i + 7] for i in range(0, len(days), 7)]  # Dias
    keyboard.extend(months)  # Meses
    keyboard.append(years)  # Anos

    # Enviar a mensagem com o teclado inline
    await bot.sendMessage(
        chat_id,
        "Selecione o dia, mês e ano:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


# Função para lidar com mensagens recebidas
async def handle(msg):
    global awaiting_confirmation, awaiting_schedule, selected_article, summary, article_title, article_url, global_articles, selected_day, selected_month, selected_year
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type != "text":
        await bot.sendMessage(
            chat_id,
            "*Desculpe, eu só posso processar mensagens de texto.*",
            parse_mode="markdown",
        )
        return

    user_input = (
        msg["text"].strip().lower()
    )  # Converte a entrada para minúsculas para evitar problemas de case-sensitivity

    # Processando comando /start
    if user_input == "/start":
        await choose_feed(chat_id)
        return

    # Verificando se o bot está aguardando uma confirmação do usuário
    if awaiting_confirmation:
        await handle_confirmation(user_input, chat_id)
        return

    # Verificando se o bot está aguardando uma solicitação de agendamento
    if selected_day and selected_month and selected_year:
        await handle_schedule_request(chat_id, user_input)
        return

    # Processando comandos de feed RSS
    if user_input in feed_urls:
        await handle_rss_feed(user_input, chat_id)
        return

    # Processando escolha de artigo do usuário
    if user_input.isdigit():
        await handle_article_choice(int(user_input), chat_id)
        return

    else:
        await bot.sendMessage(
            chat_id,
            "*Desculpe, não entendi o seu pedido. Por favor, selecione um feed RSS ou digite um número de artigo.*",
            parse_mode="markdown",
        )

    if summary:
        await send_post_schedule_options(chat_id)
        return


async def send_post_schedule_options(chat_id):
    keyboard = [
        [InlineKeyboardButton(text="Postar", callback_data="postar")],
        [InlineKeyboardButton(text="Agendar", callback_data="agendar")],
    ]

    await bot.sendMessage(
        chat_id,
        "Escolha uma opção:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def choose_feed(chat_id):
    await bot.sendMessage(
        chat_id,
        text="Olá, sou o Linkedingpt, um bot que ajuda você a postar notícias no LinkedIn. Escolha um dos feeds RSS disponíveis:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Custom Blog",
                        callback_data="/startcustomblog",
                    ),
                    InlineKeyboardButton(
                        text="Azure Feeds",
                        callback_data="/azurefeeds",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Azure AI Services",
                        callback_data="/startazureaiservices",
                    ),
                    InlineKeyboardButton(
                        text="Plain English AI",
                        callback_data="/plainenglishai",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Serverless",
                        callback_data="/startserverless",
                    ),
                    InlineKeyboardButton(
                        text="NielShok",
                        callback_data="/startnielskok",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Educator Developer",
                        callback_data="/startEducatordeveloper",
                    ),
                    InlineKeyboardButton(
                        text="Landing Page",
                        callback_data="/startlandingpage",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Command Line",
                        callback_data="/startcommandline",
                    ),
                    InlineKeyboardButton(
                        text="Infrastructure",
                        callback_data="/startinfrastructure",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Azure Governance MGMT",
                        callback_data="/azuregovernanceandmanagement",
                    ),
                    InlineKeyboardButton(
                        text="Microsoft Entra (Azure AD)",
                        callback_data="/microsoftentra",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Infrastructure Security",
                        callback_data="/infrastructuresecurity",
                    ),
                    InlineKeyboardButton(
                        text="Sec, Compliance Identity",
                        callback_data="/securitycomplianceidentity",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="FastTrack for Azure",
                        callback_data="/fasttrackforazure",
                    ),
                    InlineKeyboardButton(
                        text="Apps on Azure Blog",
                        callback_data="/appsonazureblog",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Windows IT Pro",
                        callback_data="/windowsitpro",
                    ),
                    InlineKeyboardButton(
                        text="IT OpsTalk Blog",
                        callback_data="/itopstalkblog",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Adam the Automator",
                        callback_data="/adamtheautomator",
                    ),
                    InlineKeyboardButton(
                        text="The Lazy Administrator",
                        callback_data="/thelazyadministrator",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="PowerShell Community",
                        callback_data="/powershellcommunity",
                    ),
                    InlineKeyboardButton(
                        text="PowerShell Team",
                        callback_data="/powershellteam",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Lazy Admin",
                        callback_data="/lazyadmin",
                    ),
                    InlineKeyboardButton(
                        text="Planet PowerShell",
                        callback_data="/planetpowershell",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Mike F Robbins",
                        callback_data="/startmikefrobbins",
                    ),
                    InlineKeyboardButton(
                        text="Luke Geek",
                        callback_data="/lukegeek",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Practical 365",
                        callback_data="/practical365",
                    ),
                    InlineKeyboardButton(
                        text="Microsoft 365",
                        callback_data="/startmicrosoft365",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="We Do Azure",
                        callback_data="/wedoazure",
                    ),
                    InlineKeyboardButton(
                        text="Charbel Nemnom",
                        callback_data="/charbelnemnom",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Powershell LisFun",
                        callback_data="/powershellisfun",
                    ),
                    InlineKeyboardButton(
                        text="Azure App Service",
                        callback_data="/azureappService",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Our Cloud Network",
                        callback_data="/ourcloudnetwork",
                    ),
                    InlineKeyboardButton(
                        text="Nate Hutchinson",
                        callback_data="/natehutchinson",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Techie Lass",
                        callback_data="/techielass",
                    ),
                    InlineKeyboardButton(
                        text="Ocean Leaf",
                        callback_data="/oceanleaf",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Microsoft Learn",
                        callback_data="/microsoftlearn",
                    ),
                    InlineKeyboardButton(
                        text="Prajwal Desai",
                        callback_data="/prajwaldesai",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="AdminDroid",
                        callback_data="/admindroid",
                    ),
                    InlineKeyboardButton(
                        text="Daniel Chronlund",
                        callback_data="/danielchronlund",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="CSWrld",
                        callback_data="/cswrld",
                    ),
                    InlineKeyboardButton(
                        text="Cloud Architekt",
                        callback_data="/cloudarchitekt",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Office 365 IT Pros",
                        callback_data="/office365itpros",
                    ),
                    InlineKeyboardButton(
                        text="EMS Route",
                        callback_data="/emsroute",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Suryendu B",
                        callback_data="/suryendub",
                    ),
                    InlineKeyboardButton(
                        text="Cloud Brothers",
                        callback_data="/cloudbrothers",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Verificar agendamentos pendentes",
                        callback_data="list_schedules",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Verificar atualizações",
                        callback_data="check_updates",
                    ),
                ],
            ],
        ),
    )


# Função para lidar com a confirmação do usuário
async def handle_confirmation(user_input, chat_id):
    global awaiting_confirmation
    if user_input.lower() == "s":
        response_data = post_to_linkedin(article_title, summary, article_url)
        if "id" in response_data:
            await bot.sendMessage(
                chat_id, "*Postado com sucesso no LinkedIn.*", parse_mode="markdown"
            )
        else:
            await bot.sendMessage(
                chat_id, "*Erro ao postar no LinkedIn.*", parse_mode="markdown"
            )
    elif user_input.lower() == "n":
        await bot.sendMessage(chat_id, "*Postagem cancelada.*", parse_mode="markdown")
    else:
        await bot.sendMessage(
            chat_id,
            "*Resposta inválida. Por favor, responda com 'S' para SIM ou 'N' para NÃO.*",
            parse_mode="markdown",
        )
        return  # Retorna para evitar redefinir awaiting_confirmation
    awaiting_confirmation = False  # Resetando o estado de awaiting_confirmation


# Função para enviar um seletor de hora
async def send_hourpicker(chat_id):
    # Criar botões para cada hora
    hours = [
        InlineKeyboardButton(text=f"{hour:02d}:00", callback_data=f"hour_{hour:02d}")
        for hour in range(24)
    ]

    # Agrupar os botões em linhas de 6 botões
    keyboard = [hours[i : i + 6] for i in range(0, len(hours), 6)]

    # Enviar a mensagem com o teclado inline
    await bot.sendMessage(
        chat_id,
        "Selecione a hora:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


# Função para enviar um seletor de minutos
async def send_minute_picker(chat_id, selected_hour):
    # Criar botões para cada intervalo de 15 minutos
    minutes = [
        InlineKeyboardButton(
            text=f"{selected_hour}:{minute:02d}",
            callback_data=f"time_{selected_hour}:{minute:02d}",
        )
        for minute in range(0, 60, 15)
    ]

    # Enviar a mensagem com o teclado inline
    await bot.sendMessage(
        chat_id,
        "Selecione os minutos:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[minutes]),
    )


# Função para lidar com a solicitação de agendamento do usuário

# Caminho para o arquivo de agendamentos
SCHEDULE_FILE = "schedules.json"


# Carregar agendamentos do arquivo
def load_schedules():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r") as f:
            return json.load(f)
    return {}


# Salvar agendamentos no arquivo
def save_schedules(schedules):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedules, f)


# Carregar agendamentos existentes
schedules = load_schedules()


def restore_schedules():
    for job_id, job_data in schedules.items():
        try:
            # Verifica se 'run_date' está presente no dicionário
            if "run_date" in job_data:
                schedule_datetime = datetime.strptime(
                    job_data["run_date"], "%Y-%m-%dT%H:%M:%S"
                )
                scheduler.add_job(
                    post_to_linkedin,
                    "date",
                    run_date=schedule_datetime,
                    args=job_data["args"],
                    id=job_id,
                )
            else:
                print(f"O agendamento {job_id} não possui 'run_date'.")
        except Exception as e:
            print(f"Erro ao restaurar o agendamento {job_id}: {e}")


# Chamar a função para restaurar os agendamentos
restore_schedules()


# Modificar a função handle_schedule_request para salvar os agendamentos
async def handle_schedule_request(chat_id, selected_time):
    global translated_article_title, selected_day, selected_month, selected_year, schedules

    try:
        # Convertendo a string selected_time para um objeto datetime.time
        schedule_time = datetime.strptime(selected_time, "%H:%M").time()

        # Verificando se a data foi selecionada
        if (
            selected_day is not None
            and selected_month is not None
            and selected_year is not None
        ):
            # Criando um objeto datetime com a data e hora selecionadas
            schedule_datetime = datetime.combine(
                date(selected_year, selected_month, selected_day), schedule_time
            )

            # Adicionando o trabalho de agendamento
            job = scheduler.add_job(
                post_to_linkedin,
                "date",
                run_date=schedule_datetime,
                args=[article_title, summary, article_url],
                id=translated_article_title,  # Usando o título traduzido do artigo como ID do trabalho
            )
            # Salvar o agendamento no dicionário e no arquivo
            schedules[job.id] = {
                "run_date": schedule_datetime.isoformat(),
                "args": [article_title, summary, article_url],
            }
            save_schedules(schedules)

            await bot.sendMessage(
                chat_id, "*Postagem agendada com sucesso.*", parse_mode="markdown"
            )
        else:
            await bot.sendMessage(
                chat_id,
                "*Erro ao agendar a postagem. Por favor, selecione uma data válida.*",
                parse_mode="markdown",
            )
    except ValueError as e:
        await bot.sendMessage(
            chat_id,
            f"*Ocorreu um erro ao agendar: {e}*",
            parse_mode="markdown",
        )
    finally:
        # Resetando as seleções
        selected_day = selected_month = selected_year = None


# Função para lidar com a escolha de feed RSS do usuário
async def handle_rss_feed(user_input, chat_id):
    global global_articles
    await bot.sendMessage(
        chat_id,
        "*Bem-vindo! Por favor, selecione o feed RSS do qual deseja coletar as notícias.*",
        parse_mode="markdown",
    )

    # Criação de um botão para cada feed RSS
    keyboard = [
        [InlineKeyboardButton(text=key, callback_data=feed_urls[key])]
        for key in feed_urls
    ]
    await bot.sendMessage(
        chat_id,
        "Escolha o feed:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


# Enviar notificação de geração de resumo
async def send_summary_generation_notification(chat_id):
    await bot.sendMessage(
        chat_id,
        "*O processo de geração do resumo encontra-se em andamento. Por favor, aguarde enquanto o sistema procede com a produção do resumo.*",
        parse_mode="markdown",
    )


# Função para lidar com a escolha de artigo do usuário
async def handle_article_choice(article_index, chat_id):
    global selected_article, article_url, article_title, summary, awaiting_confirmation, awaiting_schedule, translated_article_title

    # Verifica se global_articles foi definido
    if global_articles is None:
        await bot.sendMessage(
            chat_id,
            "*Nenhuma notícia foi listada ainda. Por favor, selecione um feed RSS primeiro.*",
            parse_mode="markdown",
        )
        return

    if not 0 < article_index <= len(global_articles):
        await bot.sendMessage(
            chat_id,
            "*Número de artigo inválido. Por favor, tente novamente.*",
            parse_mode="markdown",
        )
        return

    # Resetando o estado do bot
    if isinstance(global_articles, list):
        selected_article = global_articles[article_index - 1]
        article_url = selected_article.link
        article_title = selected_article.title
        translated_article_title = translator.translate(article_title, dest="pt").text
    else:
        await bot.sendMessage(
            chat_id,
            "*Nenhuma notícia foi listada ainda. Por favor, selecione um feed RSS primeiro.*",
            parse_mode="markdown",
        )
        return

    # Enviar notificação de geração de resumo
    await send_summary_generation_notification(chat_id)

    # Gerar resumo
    summary = generate_summary(selected_article.summary, article_url)
    await bot.sendMessage(chat_id, f"*Resumo: {summary} *", parse_mode="markdown")

    # Enviar opções de postagem
    keyboard = [
        [
            InlineKeyboardButton(text="Postar", callback_data="postar"),
            InlineKeyboardButton(text="Agendar", callback_data="agendar"),
        ],
        [
            InlineKeyboardButton(
                text="Gerar novo texto", callback_data="gerar_novo_texto"
            )
        ],
        [
            InlineKeyboardButton(
                text="Escolher outra notícia", callback_data="escolher_outra_noticia"
            )
        ],
        [InlineKeyboardButton(text="Cancelar", callback_data="cancelar")],
    ]
    await bot.sendMessage(
        chat_id,
        "Escolha uma opção:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


# Função para listar os agendamentos pendentes
async def list_schedules(chat_id):
    jobs = scheduler.get_jobs()
    if jobs:
        await bot.sendMessage(
            chat_id, "*Agendamentos pendentes:*", parse_mode="markdown"
        )
        keyboard = []
        for job in jobs:
            # Formata a data e a hora para o formato dd/mm/yy HH:MM
            formatted_time = job.next_run_time.strftime("%d/%m/%y %H:%M")
            await bot.sendMessage(
                chat_id,
                f"- {job.id} agendado para {formatted_time}",
                parse_mode="markdown",
            )
            cancel_id = str(
                uuid.uuid4()
            )  # Cria um identificador único para o botão de cancelamento
            global_jobs[cancel_id] = (
                job.id
            )  # Adiciona o trabalho ao dicionário global_jobs
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=f"Cancelar {job.id}", callback_data=f"cancel_{cancel_id}"
                    )
                ]
            )
        keyboard.append(
            [InlineKeyboardButton(text="Cancelar todos", callback_data="cancel_all")]
        )
        await bot.sendMessage(
            chat_id,
            "Selecione um agendamento para cancelar:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        )
    else:
        await bot.sendMessage(
            chat_id, "*Não há agendamentos pendentes.*", parse_mode="markdown"
        )


# Função auxiliar para enviar botões de atualização dos feeds
async def send_feed_update_buttons(chat_id):
    global feed_updates  # Referência à variável global

    update_messages = []
    for feed_command, articles in feed_updates.items():
        feed_name = next(
            (name for name, command in feed_names.items() if command == feed_command),
            "Unknown Feed",
        )
        update_messages.append(f"{feed_name}: {len(articles)} novos artigos")
    update_message = "\n".join(update_messages)
    await bot.sendMessage(chat_id, update_message)

    # Criar botões para feeds com atualizações
    keyboard = [
        [
            InlineKeyboardButton(
                text=feed_name, callback_data=f"feed_update_{feed_command}"
            )
        ]
        for feed_command, articles in feed_updates.items()
        for feed_name, command in feed_names.items()
        if command == feed_command
    ]
    # Adicionar botão para voltar para a tela de escolha dos feeds
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Voltar para escolha dos feeds", callback_data="choose_feed"
            )
        ]
    )

    await bot.sendMessage(
        chat_id,
        "Selecione um feed para ver as atualizações ou volte para escolha dos feeds:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


# Função para verificar atualizações nos feeds
async def check_feed_updates(chat_id):
    global feed_updates, last_check_dates  # Referência às variáveis globais

    await bot.sendMessage(chat_id, "Verificando atualizações dos feeds...")
    now = datetime.now(pytz.utc)
    feed_updates.clear()  # Limpa o dicionário de atualizações
    for feed_command, feed_url in feed_urls.items():
        last_check_str = last_check_dates.get(feed_command)
        if not last_check_str:
            # Se não houver uma última data de verificação, use o dia anterior
            last_check = (datetime.utcnow() - timedelta(days=1)).replace(
                tzinfo=pytz.utc
            )
        else:
            # Se last_check_str for uma string, converte para datetime offset-aware
            if isinstance(last_check_str, str):
                last_check = datetime.fromisoformat(last_check_str).replace(
                    tzinfo=pytz.utc
                )
            else:
                # Se last_check_str já for um datetime, usa diretamente
                last_check = last_check_str

        feed = feedparser.parse(feed_url)
        new_articles = [
            entry
            for entry in feed.entries
            if "published_parsed" in entry
            and datetime(*entry.published_parsed[:6], tzinfo=pytz.utc) > last_check
        ]
        if new_articles:
            feed_updates[feed_command] = new_articles  # Usar feed_command como chave
        last_check_dates[feed_command] = (
            now.isoformat()
        )  # Atualiza a última data de verificação

    # Salvar as últimas datas de verificação no arquivo
    save_last_check_dates(last_check_dates)

    # Enviar a contagem de atualizações para o usuário
    if feed_updates:
        await send_feed_update_buttons(chat_id)
    else:
        await bot.sendMessage(chat_id, "Não há novos artigos em nenhum feed.")


# Função para mostrar atualizações de um feed específico
async def show_feed_updates(chat_id, feed_command):
    global feed_updates  # Referência à variável global

    feed_name = next(
        (name for name, command in feed_names.items() if command == feed_command),
        "Unknown Feed",
    )
    if (
        feed_command in feed_updates
    ):  # Usar o comando do feed para acessar as atualizações
        new_articles = feed_updates[feed_command]
        for article in new_articles:
            # Traduzindo o título
            translated_title = translator.translate(article.title, dest="pt").text
            # Verificando e formatando a data de publicação
            publication_date = time.strftime("%d/%m/%Y", article.published_parsed)
            message = f"{translated_title} (Publicado em: {publication_date})"
            await bot.sendMessage(chat_id, message)
        # Após mostrar as atualizações, enviar os botões novamente
        await send_feed_update_buttons(chat_id)
    else:
        await bot.sendMessage(chat_id, f"Não há novos artigos em {feed_name}.")


# Função para lidar com o retorno da escolha do usuário
# Função para lidar com o retorno da escolha do usuário
async def on_callback_query(msg):
    global global_articles, selected_day, selected_month, selected_year, article_title, summary, article_url, translated_article_title, selected_article, schedules
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")

    # Verifica se o usuário clicou no botão "Gerar novo texto"
    if query_data == "gerar_novo_texto":
        if selected_article is not None:
            # Gerar novo resumo
            summary = generate_summary(selected_article.summary, article_url)
            await bot.sendMessage(
                from_id, f"*Novo resumo: {summary} *", parse_mode="markdown"
            )
            # Apresentar as opções novamente
            keyboard = [
                [
                    InlineKeyboardButton(text="Postar", callback_data="postar"),
                    InlineKeyboardButton(text="Agendar", callback_data="agendar"),
                ],
                [
                    InlineKeyboardButton(
                        text="Gerar novo texto", callback_data="gerar_novo_texto"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Escolher outra notícia",
                        callback_data="escolher_outra_noticia",
                    )
                ],
                [InlineKeyboardButton(text="Cancelar", callback_data="cancelar")],
            ]
            await bot.sendMessage(
                from_id,
                "Escolha uma opção:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
            )
        else:
            await bot.sendMessage(from_id, "Nenhuma notícia selecionada.")
        return

    # Verifica se o usuário clicou no botão "Escolher outra notícia"
    if query_data == "escolher_outra_noticia":
        for i, article in enumerate(global_articles):
            translated_title = translator.translate(article.title, dest="pt").text
            await bot.sendMessage(from_id, f"{i+1}. {translated_title}")
        await bot.sendMessage(
            from_id,
            "*Por favor, indique a notícia que deseja resumir informando o número correspondente.*",
            parse_mode="markdown",
        )
        return

    # Verifica se o usuário clicou no botão "Cancelar"
    if query_data == "cancelar":
        await bot.sendMessage(from_id, "*Operação cancelada.*", parse_mode="markdown")
        await choose_feed(from_id)
        return

    # Verifica se o usuário clicou no botão "Agendar"
    if query_data == "agendar":
        await bot.answerCallbackQuery(query_id, text="Agendamento selecionado.")
        await send_datepicker(from_id)  # Chame a função que exibe o seletor de data
        return

    # Verifica se o usuário clicou no botão "Postar"
    if query_data == "postar":
        await bot.answerCallbackQuery(query_id, text="Postagem selecionada.")
        response_data = post_to_linkedin(article_title, summary, article_url)
        if "id" in response_data:
            await bot.sendMessage(
                from_id, "*Postado com sucesso no LinkedIn.*", parse_mode="markdown"
            )
        else:
            await bot.sendMessage(
                from_id, "*Erro ao postar no LinkedIn.*", parse_mode="markdown"
            )
        return

    if query_data.startswith("cancel_"):
        if query_data == "cancel_all":
            scheduler.remove_all_jobs()
            await bot.answerCallbackQuery(
                query_id, text="Todos os agendamentos foram cancelados."
            )
        else:
            cancel_id = query_data[len("cancel_") :]
            job_id = global_jobs.get(cancel_id)
            if job_id is not None:
                scheduler.remove_job(job_id)
                await bot.answerCallbackQuery(
                    query_id, text=f'O agendamento "{job_id}" foi cancelado.'
                )
        return

    # Verifica se o usuário clicou no botão "Verificar agendamentos pendentes"
    if query_data == "list_schedules":
        await list_schedules(from_id)
        return

    # Verifica se o usuário clicou no botão "Verificar atualizações"
    if query_data == "check_updates":
        await check_feed_updates(from_id)
        return

    if query_data.startswith("feed_update_"):
        feed_command = query_data.split("feed_update_")[1]
        await show_feed_updates(from_id, feed_command)
        return

    if query_data == "choose_feed":
        await choose_feed(from_id)  # Chame a função que exibe os feeds para escolha
        return

    if query_data.startswith("cancel_"):
        if query_data == "cancel_all":
            for job_id in list(schedules.keys()):
                scheduler.remove_job(job_id)
            schedules.clear()
            save_schedules(schedules)
            await bot.answerCallbackQuery(
                query_id, text="Todos os agendamentos foram cancelados."
            )
        else:
            cancel_id = query_data[len("cancel_") :]
            job_id = global_jobs.get(cancel_id)
            if job_id is not None and job_id in schedules:
                scheduler.remove_job(job_id)
                del schedules[job_id]
                save_schedules(schedules)
                await bot.answerCallbackQuery(
                    query_id, text=f'O agendamento "{job_id}" foi cancelado.'
                )
        return
    # Verifica se o usuário selecionou um dia
    if query_data.startswith("day_"):
        selected_day = int(query_data[len("day_") :])
        await bot.answerCallbackQuery(query_id, text=f"Dia {selected_day} selecionado.")
        if selected_month and selected_year:
            await send_hourpicker(
                from_id
            )  # Chame a função que exibe as horas para escolha
        return

    # Verifica se o usuário selecionou um mês
    if query_data.startswith("month_"):
        selected_month = int(query_data[len("month_") :])
        await bot.answerCallbackQuery(
            query_id, text=f"Mês {selected_month} selecionado."
        )
        if selected_day and selected_year:
            await send_hourpicker(
                from_id
            )  # Chame a função que exibe as horas para escolha
        return

    # Verifica se o usuário selecionou um ano
    if query_data.startswith("year_"):
        selected_year = int(query_data[len("year_") :])
        await bot.answerCallbackQuery(query_id, text=f"Ano {selected_year} selecionado.")
        if selected_day and selected_month:
            await send_hourpicker(
                from_id
            )  # Chame a função que exibe as horas para escolha
        return

    # Verifica se o usuário selecionou uma hora
    if query_data.startswith("hour_"):
        selected_hour = query_data[len("hour_") :].zfill(
            2
        )  # Garante que a hora tenha dois dígitos
        await bot.answerCallbackQuery(
            query_id, text=f"Hora {selected_hour}:00 selecionada."
        )
        await send_minute_picker(
            from_id, selected_hour
        )  # Chame a função que exibe os minutos para escolha
        return

    # Verifica se o usuário selecionou um horário completo
    if query_data.startswith("time_"):
        selected_time = query_data[len("time_") :].zfill(
            5
        )  # Garante que o horário tenha o formato HH:MM
        await bot.answerCallbackQuery(
            query_id, text=f"Horário {selected_time} selecionado."
        )
        await handle_schedule_request(
            from_id, selected_time
        )  # Chame a função de agendamento com o horário selecionado
        return

    # Verifica se o dado retornado é um feed RSS válido
    if query_data in feed_urls:
        feed_url = feed_urls[query_data]
        await bot.answerCallbackQuery(query_id, text="Processando feed RSS...")
        feed = feedparser.parse(feed_url)
        articles = feed.entries

        # Limita o número de notícias para 25 se o feed escolhido for startmikefrobbins
        if query_data == "/startmikefrobbins" and len(articles) > 50:
            articles = articles[:50]

        if query_data == "/charbelnemnom" and len(articles) > 50:
            articles = articles[:50]

        if query_data == "/azurefeeds" and len(articles) > 65:
            articles = articles[:65]

        if query_data == "/planetpowershell" and len(articles) > 50:
            articles = articles[:50]

        if query_data == "/office365itpros" and len(articles) > 50:
            articles = articles[:50]

        global_articles = articles  # Agora isto está definindo a variável global

        # Envia uma mensagem informando que o feed está sendo traduzido
        feed_name = [
            name for name, command in feed_names.items() if command == query_data
        ][0]
        await bot.sendMessage(
            from_id,
            f"*Realizando a tradução dos títulos das notícias do Feed {feed_name}, por favor, aguarde...*",
            parse_mode="markdown",
        )

        for i, article in enumerate(articles):
            try:
                # Traduzindo o título
                translated_title = translator.translate(article.title, dest="pt").text

                # Verificando e formatando a data de publicação
                if hasattr(article, "published_parsed"):
                    publication_date = time.strftime(
                        "%d/%m/%Y", article.published_parsed
                    )
                    message = (
                        f"{i+1}. {translated_title} (Publicado em: {publication_date})"
                    )
                else:
                    # Se a data de publicação não estiver disponível
                    message = f"{i+1}. {translated_title}"

                await bot.sendMessage(from_id, message)

            except TypeError:
                await bot.sendMessage(from_id, f"{i+1}. Erro na tradução do título")

        await bot.sendMessage(
            from_id,
            "*Por favor, indique a notícia que deseja resumir informando o número correspondente.*",
            parse_mode="markdown",
        )

    else:
        await bot.answerCallbackQuery(query_id, text="Erro ao processar feed RSS.")


# Carregar a última data de verificação do arquivo ou inicializar com o dia anterior
def load_last_check_dates():
    try:
        if os.path.exists(LAST_CHECK_FILE) and os.path.getsize(LAST_CHECK_FILE) > 0:
            with open(LAST_CHECK_FILE, "r") as f:
                last_check_data = json.load(f)
                # Converter todas as datas de string para datetime offset-aware
                for feed_command, last_check_str in last_check_data.items():
                    last_check_data[feed_command] = datetime.fromisoformat(
                        last_check_str
                    ).replace(tzinfo=pytz.utc)
                return last_check_data
        else:
            # Se o arquivo não existir ou estiver vazio, inicialize com o dia anterior
            yesterday = (
                (datetime.utcnow() - timedelta(days=1))
                .replace(tzinfo=pytz.utc)
                .isoformat()
            )
            last_check_dates = {
                feed_command: yesterday for feed_command in feed_urls.keys()
            }
            save_last_check_dates(last_check_dates)
            return last_check_dates
    except json.JSONDecodeError:
        # Se ocorrer um erro de decodificação, inicialize com o dia anterior
        yesterday = (
            (datetime.utcnow() - timedelta(days=1)).replace(tzinfo=pytz.utc).isoformat()
        )
        last_check_dates = {
            feed_command: yesterday for feed_command in feed_urls.keys()
        }
        save_last_check_dates(last_check_dates)
        return last_check_dates


# Salvar a última data de verificação no arquivo
def save_last_check_dates(last_check_dates):
    with open(LAST_CHECK_FILE, "w") as f:
        # Converter todas as datas para string ISO antes de salvar
        last_check_data = {
            feed_command: (
                last_check_date.isoformat()
                if isinstance(last_check_date, datetime)
                else last_check_date
            )
            for feed_command, last_check_date in last_check_dates.items()
        }
        json.dump(last_check_data, f)


# Carregar as últimas datas de verificação existentes
last_check_dates = load_last_check_dates()

# Inicializar o bot
bot = telepot.aio.Bot(TELEGRAM_TOKEN)

client_session = None


async def init_client_session():
    global client_session
    client_session = aiohttp.ClientSession(  # Inicializar a sessão do cliente
        headers={"User-Agent": "Mozilla/5.0"}
    )


# Configurar o loop de mensagens
loop = asyncio.get_event_loop()
loop.create_task(
    bot.message_loop({"chat": handle, "callback_query": on_callback_query})
)
loop.run_until_complete(init_client_session())
# Iniciar o bot

print("Bot iniciado. Aguardando comandos...")
loop.run_forever()
