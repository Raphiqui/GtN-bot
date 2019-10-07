# GtN-bot

Creation of a bot using [Telegram](https://telegram.org) app.
With Botfather's help you should be able to create your own bot. Be sure to keep the bot's key 
which should looks like this 
```704418931:AAEtcZ*************```

If you're using a virtual environment use the following commands to create and activate it
```
python -m venv /path/to/new/virtual/environment

.\venv\Scripts\activate
```

Then use this to download the requirements 
```
pip install -r requirements.txt
```

Be aware that to run this code you need to add a file named <strong>conf.json</strong>
by using the following commands, 
```
cd GtN-bot
touch conf.json
```
then fill it with this code
```
{
    "bot_token":"YOUR_BOT_TOKEN"
}
```

To start the program use the following command
```
python app.py
```