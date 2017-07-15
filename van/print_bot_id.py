import os
from slackclient import SlackClient


BOT_NAME = 'queuesem'
BOT_TOKEN = 'xoxb-170547515060-RkoomWy5GyEq4By8XHAeWun9'  # os.environ.get('BOT_TOKEN')

slack_client = SlackClient(BOT_TOKEN)


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

        api_call = slack_client.api_call("channels.list", exclude_archived=1)
        for channel in api_call.get('channels'):
            if 'name' in channel and channel.get('name') == 'queuesem_':
                print("Channel ID for '" + channel.get('name') + "' is " + channel.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)
