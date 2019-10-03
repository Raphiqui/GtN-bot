import json
import pprint

BOT_TOKEN = None


def fetch_conf():
    with open('conf.json') as json_data_file:
        data = json.load(json_data_file)
    return data["bot_token"]


if __name__ == '__main__':
    BOT_TOKEN = fetch_conf()
    pprint.pprint(BOT_TOKEN)