# [:calendar: Linkedin AutoPost - Automatize suas postagens no LinkedIn e Telegram!](LinkedinTelegramPostScheduleV5.py)

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


## :page_facing_up: Introdução

Este script em Python :snake: foi desenvolvido para automatizar o agendamento de postagens no LinkedIn e no Telegram. Ele permite que você programe suas postagens com antecedência, economizando tempo e esforço. 

## :star: Funcionalidades

1. **Agendamento de postagens**: O script permite que você agende suas postagens no LinkedIn e no Telegram para serem publicadas em um horário específico. Isso é útil para manter uma presença consistente nas redes sociais, mesmo quando você não está disponível para fazer as postagens manualmente.

2. **Suporte ao LinkedIn**: O script utiliza a API do LinkedIn para fazer as postagens agendadas. Ele permite que você escreva o conteúdo da postagem, adicione imagens e escolha a data e hora exatas para a publicação.

3. **Suporte ao Telegram**: Além do LinkedIn, o script também suporta o agendamento de postagens no Telegram. Ele utiliza a API do Telegram para fazer as postagens agendadas. Você pode escrever o conteúdo da postagem e escolher a data e hora exatas para a publicação.

4. **Configurações personalizáveis**: O script permite que você personalize as configurações de acordo com suas necessidades. Você pode definir o caminho do arquivo de configuração, onde você pode armazenar suas credenciais de API e outras configurações específicas.

5. **Interface de linha de comando**: O script possui uma interface de linha de comando simples e intuitiva. Ele permite que você execute o script e agende suas postagens com apenas alguns comandos.

## :bulb: Processo de Geração de Resumos

### 1. **Seleção de Conteúdo**

O usuário seleciona um feed RSS de interesse, e o bot recupera os artigos mais recentes disponíveis nesse feed.


### 2. **Extração de Conteúdo**

Para cada artigo selecionado, o bot extrai o conteúdo principal, incluindo título e corpo do texto. Em alguns casos, também são extraídas as tags Open Graph para obter imagens e descrições mais precisas.


### 3. **Limpeza de Conteúdo**

O conteúdo extraído passa por um processo de limpeza para remover tags HTML, caracteres especiais e outros elementos que podem interferir na qualidade do resumo.


### 4. **Tradução (Opcional)**

Se necessário, o conteúdo é traduzido para o idioma desejado usando a biblioteca `googletrans`. Esta etapa é importante para garantir que o resumo seja gerado no idioma preferido do usuário.


### 5. **Geração de Resumo**

O conteúdo limpo e, se aplicável, traduzido é enviado para a API do Azure OpenAI. Utilizando modelos avançados de linguagem, como o GPT-4 do Azure OpenAI, a API gera um resumo conciso do artigo. Este resumo é otimizado para capturar os pontos principais do conteúdo, mantendo a coerência e a relevância, utilizando um modelo postagem.


### 6. **Formatação para Postagem**

O resumo gerado é então formatado de acordo com as melhores práticas de postagem no LinkedIn, incluindo a adição de emojis, hashtags relevantes e uma questão provocativa no final para incentivar o engajamento.


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


3. Configure as seguintes credenciais no script:

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

3. Instale as bibliotecas.

   ```bash
   pip install -r requirements.txt
   ```


4. Abra o terminal ou prompt de comando e execute o script `LinkedinTelegramPostScheduleV5.py` para iniciar.

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
