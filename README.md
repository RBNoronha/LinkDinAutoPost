
# Linkedinautopost Bot: Script de Automação para Notícias e Postagens no LinkedIn


## Descrição

O Linkedingpt é um script Python avançado projetado para automatizar postagens no LinkedIn utilizando feeds RSS, Azure OpenAI com GPT-4 para geração de resumos, API do Telegram e a API do LinkedIn para publicações. Ideal para profissionais que desejam manter uma presença ativa no LinkedIn com conteúdo atualizado e relevante.

## Funcionalidades

### Coleta de Notícias de Fontes RSS:

- O script usa feeds RSS para coletar notícias. RSS (Really Simple Syndication) é um formato padrão usado para entregar regularmente informações atualizadas, como notícias, em um formato padronizado.
- O script pode estar programado para acessar vários feeds RSS de diferentes fontes de notícias, permitindo a coleta automática de artigos recentes.

### 2. Tradução e Resumo Automático:

- Após coletar as notícias, o script pode usar algoritmos de tradução automática para converter o conteúdo para o idioma desejado.
- Em seguida, pode utilizar tecnologias de inteligência artificial, através da API do Azure OpenAI com redundancia, para resumir as notícias, mantendo os pontos principais e descartando informações menos relevantes.

### 3. Postagem Inteligente no LinkedIn:

- Com as notícias coletadas, traduzidas e resumidas, o script pode então automatizar o processo de postagem no LinkedIn.
- Isso pode incluir a formatação do conteúdo para se adequar aos padrões da plataforma e o agendamento de postagens para horários de pico de atividade, aumentando a visibilidade.

### 4. Integração com LinkedIn e Telegram:

- Além de postar diretamente no LinkedIn, o script pode usar a integração com o Telegram para notificações ou prompts adicionais.
- Permite revisão e seleção manual das notícias a serem postadas.
- Gera novo texto caso o primeiro não te agrade.

## Vantagens do Uso do Script

### Eficiência e Economia de Tempo

- Automatizar a coleta e postagem de notícias poupa um tempo significativo que, de outra forma, seria gasto na pesquisa manual e na formatação de postagens.

### Atualização Contínua

- O script permite manter um fluxo constante de conteúdo, o que é essencial para manter o engajamento na plataforma do LinkedIn.

### Alcance e Relevância Ampliados

- Com a capacidade de traduzir e resumir notícias de diferentes regiões e idiomas, o script amplia o alcance das postagens, tornando-as acessíveis e relevantes para um público mais amplo.

### Personalização e Precisão

- Assegura a qualidade e relevância do conteúdo com o auxílio de IA.

### Flexibilidade e Controle

- Integração com Telegram oferece controle adicional sobre as postagens.

### Melhoria de Engajamento no LinkedIn

- Postagens regulares e de qualidade são fundamentais para manter e aumentar o engajamento na rede, o que pode ser benéfico tanto para perfis pessoais quanto empresariais.

## Pré-requisitos

Antes de iniciar, certifique-se de que as seguintes ferramentas e bibliotecas estejam instaladas em seu sistema:

- Python 3.6 ou superior
- pip (gerenciador de pacotes Python)
- Acesso às APIs do Azure OpenAI, Telegram e LinkedIn

## Clone o Repositorio

```
git clone https://github.com/RBNoronha/LinkDinAutoPost.git
cd LinkDinAutoPost/
```

## Instalação de Dependências

O script requer a instalação de várias bibliotecas Python. Para instalar estas dependências, execute o seguinte comando no terminal:

```
pip install -r requirements.txt
```

Este comando instalará todas as bibliotecas listadas no arquivo `requirements.txt` do seu repositório.

# Guia Detalhado para Obtenção de APIs de Configuração

## Azure OpenAI

### Como Obter a API Key do Azure OpenAI

1. **Crie uma conta no Azure**: Se ainda não tiver uma, [crie sua conta no Azure](https://azure.microsoft.com/pt-br/free/).
2. **Acesse o Portal do Azure**: Faça login no [portal do Azure](https://portal.azure.com/).
3. **Crie um recurso de OpenAI**: No portal do Azure, selecione “Criar um recurso” e procure por “OpenAI”. Siga as instruções para criar um recurso de OpenAI.
4. **Obtenha a API Key**: Uma vez que o recurso estiver configurado, navegue até a seção de chaves no painel de recursos do OpenAI para encontrar sua API Key.

## Telegram Bot API

### Como Criar um Bot e Obter o Token do Telegram

1. **Inicie uma conversa com o BotFather**: No Telegram, procure por “BotFather” e inicie uma conversa.
2. **Crie um novo bot**: Digite `/newbot` e siga as instruções para criar seu bot.
3. **Obtenha o Token do Bot**: Após a criação do bot, o BotFather fornecerá um token, que é a chave de API para o seu bot.

## LinkedIn API

### Como Obter o Access Token do LinkedIn

1. **Crie uma Aplicação no LinkedIn Developer Portal**: Acesse o [LinkedIn Developer Portal](https://www.linkedin.com/developers/) e crie uma nova aplicação.
2. **Configure as permissões da aplicação**: Na configuração da sua aplicação, defina as permissões necessárias para o escopo da API.
3. **Autentique e Obtenha o Access Token**: Use o fluxo de autenticação OAuth 2.0 do LinkedIn para autenticar e obter o Access Token.

## Configuração

O script requer a instalação de várias bibliotecas Python. Para instalar estas dependências, entre na pasta do repositorio clonado e execute o seguinte comando no terminal:

```
pip install -r requirements.txt
```
Este comando instalará todas as bibliotecas listadas no arquivo `requirements.txt` do repositório.

## Configuração de Variáveis e Tokens

Você precisará configurar diversas variáveis e tokens para as APIs do Telegram, Azure OpenAI e LinkedIn.

### Azure OpenAI

Altere as variáveis de configuração do Azure OpenAI com seus próprios valores de API:

```python
openai.api_base = "SEU_AZURE_API_BASE"
openai.api_version = "SEU_AZURE_API_VERSION"
openai.api_key = "SEU_AZURE_API_KEY"
```

### Telegram
Defina o token do seu bot do Telegram:

```python
TELEGRAM_TOKEN = "SEU_TELEGRAM_TOKEN"
```

### LinkedIn
Para a API do LinkedIn, configure o token de acesso:

```python
ACCESS_TOKEN = "SEU_ACCESS_TOKEN"
```

## Execução do Script

Com as dependências instaladas e as variáveis configuradas, você está pronto para executar o script. Para iniciar, execute o seguinte comando no terminal:

```
python linkedinautopost.py
```

Lembre-se de manter o script em execução para que o bot permaneça ativo.

## Comandos do Bot

Após a execução, o bot do Telegram estará ativo e responderá aos seguintes comandos:
- `/start`: Inicia a interação com o bot.
- Comandos adicionais para solicitar informações das APIs do Azure e LinkedIn.
- **Interagir via Telegram**: Use os comandos no chat do Telegram para selecionar feeds, gerar resumos e postar no LinkedIn.

## Conclusão

- Este script representa uma poderosa ferramenta de automação para profissionais e empresas que buscam manter uma presença ativa e relevante no LinkedIn, maximizando o alcance e engajamento com um investimento mínimo de tempo e esforço manual.

## Créditos
- Desenvolvido por Renan Besserra
- Utiliza OpenAI GPT-4, APIs do LinkedIn e Telegram.
