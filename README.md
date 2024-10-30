# [:calendar: Linkedin AutoPost - Automate your LinkedIn and Telegram posts!](LinkedinTelegramPostScheduleV5.py)

## :page_facing_up: Introduction

:snake: This Python script runs a Telegram bot designed to automate the posting of news and articles on LinkedIn. It uses RSS feeds to collect news, generates summaries using the Azure OpenAI API, and posts or schedules posts on LinkedIn. This bot is a powerful tool for professionals who want to keep their network updated with the latest industry news, without the manual effort of writing each post.

## :books: Table of Contents
1. [Introduction](#page_facing_up-introduction)
2. [Features](#star-features)
3. [Summary Generation Process](#bulb-summary-generation-process)
    1. [Content Selection](#1-content-selection)
    2. [Content Extraction](#2-content-extraction)
    3. [Content Cleaning](#3-content-cleaning)
    4. [Translation (Optional)](#4-translation-optional)
    5. [Summary Generation](#5-summary-generation)
    6. [Formatting for Posting](#6-formatting-for-posting)
    7. [Technologies Used](#7-technologies-used)
4. [Benefits](#rocket-benefits)
5. [Configuration](#hammer_and_wrench-configuration)
6. [Usage](#rocket-usage)
7. [Notes](#memo-notes)
8. [Author](#bust_in_silhouette-author)

## :star: Features

### 1. **RSS Feed Selection**:
- Choose from various RSS feeds to get news and articles.

### 2. **Automatic Summary Generation**:
- Uses the Azure OpenAI API to generate concise and relevant summaries of articles.

### 3. **Posting and Scheduling on LinkedIn**:
- Allows immediate posting or scheduling of posts on LinkedIn, including date and time selection.

### 4. **Multi-Language Support**:
- Translates titles and content to Portuguese before summary generation, using the googletrans library.

### 5. **Interactive Interface**:
- Provides a user-friendly interface on Telegram for easy navigation and operation.

### 6. **Real-Time Feed Updates**:
- Checks for updates in the selected RSS feeds and notifies the user about new available articles.

## :bulb: Summary Generation Process

### 1. **Content Selection**

- The user selects an RSS feed of interest, and the bot retrieves the latest available articles from that feed.


### 2. **Content Extraction**

- For each selected article, the bot extracts the main content, including title and body text. In some cases, Open Graph tags are also extracted to obtain more accurate images and descriptions.


### 3. **Content Cleaning**

- The extracted content goes through a cleaning process to remove HTML tags, special characters, and other elements that may interfere with the quality of the summary.


### 4. **Translation (Optional)**

- If necessary, the content is translated to the desired language using the `googletrans` library. This step is important to ensure that the summary is generated in the user's preferred language.


### 5. **Summary Generation**

- The cleaned content, if applicable, is sent to the Azure OpenAI API. Using advanced language models like Azure OpenAI's GPT-4, the API generates a concise summary of the article. This summary is optimized to capture the main points of the content while maintaining coherence and relevance, using a post-like model.


### 6. **Formatting for Posting**

- The generated summary is then formatted according to best practices for posting on LinkedIn, including the addition of emojis, relevant hashtags, and a provocative question at the end to encourage engagement.


### 7. **Technologies Used**

- **Feedparser**: Used to parse RSS feeds and extract articles.
- **BeautifulSoup**: Assists in cleaning the HTML content of articles.
- **Googletrans**: Library for automatic text translation.
- **Azure OpenAI API**: Provides access to GPT-4 language models for summary generation. The choice of this API is due to its ability to understand and synthesize complex information in a coherent and concise manner.


## :rocket: Benefits

- **Efficiency**: Automates the process of reading and summarizing information, saving time.
- **Consistency**: Maintains a quality standard in summaries, regardless of the volume of processed content.
- **Engagement**: Well-crafted and formatted summaries according to LinkedIn guidelines can increase engagement with the posted content.
- **Accessibility**: Makes it easier for professionals to share knowledge and relevant information with their network, regardless of language or time barriers.

Automatic summary generation represents a significant advancement in how professionals interact with and disseminate information on professional networking platforms like LinkedIn. By harnessing the power of artificial intelligence and natural language processing, this bot offers an effective solution for maintaining an active and informative online presence.


## :hammer_and_wrench: Configuration

1. Make sure you have Python installed on your system.

2. Download the repository to your computer.

    ```bash
    git clone https://github.com/RBNoronha/LinkDinAutoPost.git

    cd LinkDinAutoPost
    ```


3. Configure the following credentials in the `config.py` file:

- **Telegram Bot Token**: Obtain a token by creating a bot on Telegram through BotFather.

    ```bash
    TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
    ```

- **Azure OpenAI API Keys**: Sign up for Azure and create an OpenAI instance to get your API keys.
    ```base
    AZURE_API_KEY = "YOUR_AZURE_OPENAI_API_KEY"
    AZURE_API_BASE = "YOUR_AZURE_OPENAI_API_BASE"
    GPT_MODEL_32K: = "YOUR_NAME_MODEL_AZURE"
    GPT_MODEL_TURBO = "YOUR_NAME_MODEL_AZURE"
    ```

- **LinkedIn Access Token**: Create an application on LinkedIn and obtain an OAuth2 access token.
    ```bash
    ACCESS_TOKEN: "YOUR_TOKEN_OAUTH2_LINKEDIN"
    ```

4. Set up logging configuration in the `logging_config.py` file:

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
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    ```

5. Install the required libraries.

    ```bash
    pip install -r requirements.txt
    ```


6. Open the terminal or command prompt and run the `LinkedinTelegramPostScheduleV5.py` script to start.

    ```bash
    python LinkedinTelegramPostScheduleV5.py
    ```


## :rocket: Usage

Interact with the bot through Telegram. The bot provides an interactive interface to choose RSS feeds, view news, generate summaries, and post or schedule posts on LinkedIn.


## :memo: Notes

- :key: Make sure you have the correct API credentials for LinkedIn and Telegram before using the script.
- :computer: This script has been tested on Windows and Linux systems. There may be differences in execution on other operating systems.

## :bust_in_silhouette: Author

This script was developed by Renan Besserra. :octocat: Feel free to contribute, report issues, or submit feature requests. # LinkedinTelegramPostScheduleV5.py
