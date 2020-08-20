import json
from random import random
import requests
import datetime
import random
import sys
import os


def main():
    casting()
    channel, first_word, message, username = get_input()
    if first_word == 'scarydoor' or first_word == 'talesofinterest':
        first_word = random.choice(characters)
    elif first_word == 'talesofinterest':
        first_word = random.choice(characters)
    if not channel:
        channel = default_channel
    icon_url, slack_username, webhook_url, default_channel = cast(first_word)
    quote = get_quote(first_word)
    if quote == "Wait a minute! Is that blimp accurate?":
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        quote = "Yep. It's December 31st, 2999."
        icon_url, slack_username, webhook_url, dc = cast('leelaspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        quote = "My God! A million years!"
        icon_url, slack_username, webhook_url, dc = cast('fryspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
    elif quote == "Can't we get away in the ship?":
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        quote = "I suppose it is technically possible, although I am already in my pajamas."
        icon_url, slack_username, webhook_url, dc = cast('professorspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
    elif quote == "They never made wise use of the land. When my ancestor Reginald Wong landed here, they had no bingo parlors and only one prostitute.":
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        quote = "Pathetic!"
        icon_url, slack_username, webhook_url, dc = cast('benderspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
    elif quote == "Ah yes, better. A lonely weekend in my dumpster with a jar of pennies and tears.":
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        quote = "Sounds good.  See you Monday!"
        icon_url, slack_username, webhook_url, dc = cast('amyspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
    elif quote == "I'm going to jump!":
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        quote = "No!"
        icon_url, slack_username, webhook_url, dc = cast('amyspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        icon_url, slack_username, webhook_url, dc = cast('zoidbergspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
        quote = "Do a flip!"
        icon_url, slack_username, webhook_url, dc = cast('benderspeaks')
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)
    else:
        deliver_line(channel, icon_url, slack_username, quote, webhook_url)


def casting():
    global playbill
    global characters
    global lines
    directory = os.path.dirname(__file__)  # get pathd
    filename = os.path.join(directory, 'screenplay.json')
    print(filename)
    with open(filename, 'r') as fin:
        lines = json.load(fin)
    characters = [member for member in lines]

    log(f"We have speaking parts for: {', '.join(characters)}")

    directory = os.path.dirname(__file__)  # get path
    filename = os.path.join(directory, 'playbill.json')
    with open(filename, 'r', encoding='utf-8') as fin:
        playbill = json.load(fin)
    log(f"playbill.json loaded from {directory}")


def get_input():
    if len(sys.argv) > 2:
        first_word = sys.argv[2].lower()
        msg = f"Script manually triggered with specific arguments.  Trigger word is:  {first_word}"
        log(msg)
        username = 'clean'
        channel = None
        message = None
    elif len(sys.argv) == 1:
        first_word = random.choice(characters)
        msg = f"Script manually triggered with no arguments.  Trigger word is:  {first_word}"
        log(msg)
        username = 'clean'
        channel = None
        message = None
    else:
        webhook_content = sys.argv[1]
        data = json.loads(webhook_content)
        log(f"Webhook event:  {data}")
        message = str(data['text']).lower()
        username = str(data['user_name']).lower()
        channel = str(data['channel_name'])
        print("the message data is " + str(message))
        first_word = message.split(' ', 1)[0].lower()
        second_word = message.split(' ', 2)[0].lower()
        print(second_word)
    return channel, first_word, message, username


def get_quote(first_word):
    quote = random.choice((lines[first_word]))
    return quote


def cast(character):
    webhook_url = ""
    icon_url = random.choice(playbill[character]['icon_url'])
    slack_username = random.choice(playbill[character]['username'])
    default_channel = playbill[character]['default_channel']
    return icon_url, slack_username, webhook_url, default_channel


def deliver_line(channel, icon_url, slack_username, text, webhook_url):
    slack_data = {'channel': '#' + channel,
                  'text': text,
                  'username': slack_username, 'icon_url': icon_url}
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    log(f"{slack_username}:  {text}")


def log(msg):
    directory = os.path.dirname(__file__)  # get path
    filename = os.path.join(directory, 'futurama_screenplay.log')
    print(f"[{datetime.datetime.now().isoformat()} - {msg}")
    with open(filename, 'a', encoding='utf-8') as fout:
        fout.write(f"[{datetime.datetime.now().isoformat()}")
        fout.write(msg)
        fout.write('\n')


if __name__ == '__main__':
    main()
