#!/usr/bin/python

import json
import random
import time

from slackclient import SlackClient

# the filename storing our API token
TOKENFILE = "slack.token"

# the username of our bot
USERNAME = "pibot"

def get_api_token():
    """Fetch our API token from the environment variable"""

    # return the results
    return os.environ.get('SLACK_BOT_TOKEN')


def main():
    """The main stuff that we do"""

    # get our api token
    token = get_api_token()

    # initialize our slack client
    slack_client = SlackClient(token)

    # now get our own ID
    user_list = slack_client.api_call("users.list")
    user_dict = {
        user.get("name"): user.get("id")
        for user in user_list.get("members")
    }

    slack_user_id = user_dict[USERNAME]
    adrian_id = user_dict["adrian"]

    # now start a connection
    if slack_client.rtm_connect():
        print("Connected!")

    # now start our mainloop
    while True:
        for message in slack_client.rtm_read():
            if "text" in message and message["text"].startswith("<@%s>" % slack_user_id):
                print("Message received: %s" % json.dumps(message, indent=2))

                if "snek" in message["text"]:
                    response = "cc"
                    if message["user"] == adrian_id:
                        choices = [
                            "silly frosh, there's no such thing as snek",
                            "snerk",
                            "why are you like this",
                            "go to bed frosh",
                            "sad!",
                        ]
                        response = random.choice(choices)
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message["channel"],
                        text=response,
                        as_user=True)

        time.sleep(1)


if __name__ == '__main__':
    main()
