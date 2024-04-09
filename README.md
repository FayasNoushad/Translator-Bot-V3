# Translator Bot V3
An advanced telegram language translator bot

---

## Features

    - Database ( MongoDB ) Support
    - Broadcast Support
    - Set default language support
    - Direct languages updation from Python Translation Library

---

## Deploy

```sh
git clone https://github.com/FayasNoushad/Translator-Bot-V3.git
cd Translator-Bot
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
# <Create Variables appropriately>
python3 main.py
```

---

## Variables

### Required

- `API_HASH` Your API Hash from my.telegram.org
- `API_ID` Your API ID from my.telegram.org
- `BOT_TOKEN` Your bot token from @BotFather
- `DATABASE_URL` MongoDB URL

### Optional

- `ADMINS` Administrators IDs seperated by whitespace
- `DATABASE_NAME` MongoDB Database Name
- `DEFAULT_LANGUAGE` Default language code

---

## Old Versions

- [Translator-Bot](https://github.com/FayasNoushad/Translator-Bot)
- [Translator-Bot-V2](https://github.com/FayasNoushad/Translator-Bot-V2)

---
