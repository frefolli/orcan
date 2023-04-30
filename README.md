# Bot Telegram Infrastructure
This is the implementations of Svoltamib's telegram bots infrastracture used to semplify the management of the organization's Telegram groups.

## Dependences

You must need python >= 3.10 


## Installation

First step is cloning the repository

    git clone git@github.com:SvoltaMiB/bot-telegram.git

create a new python enviroment in the current directory

    python3 -m venv venv

enter in the enviroment

    source venv/bin/activate

install all dependences

    pip install -r requirements.txt

## Configuration

Create new file .env and add secret credentials like bot-tokens and DB

    ANTISPAM_BOT_API_TOKEN=<API-TOKEN>
    POST_BOT_API_TOKEN=<API-TOKEN>
    REPORT_BOT_API_TOKEN=<API-TOKEN>
    ADMIN_CHAT_ID=<API-TOKEN>
    CHECK_POST_CHAT_ID=<API-TOKEN>
    FORWARD_POST_CHAT_ID=<API-TOKEN>
    SICURA=<Boolean>

Quando `SICURA` non e' uguale a `False` gli utenti non possono essere bannati

## Usage
prova
## How to test
