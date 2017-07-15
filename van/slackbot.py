import os
import re
import time

from slackclient import SlackClient

import events
from res_reservation import ResourceReservation
from resource_event_listener import ResourceEventListener
from conversation_listener import ConversationListener
from users import Users

BOT_ID = os.environ.get('BOT_ID')
BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')

READ_WEBSOCKET_DELAY = 1


AT_BOT = "<@{0}>".format(BOT_ID)


def post(slack_client, channel, content):
    slack_client.api_call(
        'chat.postMessage',
        channel=channel, text=content,
        as_user=True)


def is_message_to_bot(message, at_bot):
    """
    Parses the incoming message to see if it is addressed to the bot.
    The message is interpreted as addressing the bot if it follows the
    format:
        @{AT_BOT} blah blah blah
        @{AT_BOT}: blah blah blah
    
    :param message: the incoming message 
    :param at_bot: the '@botname' value to detect
    :return: True if the message is addressed to the bot.
    """
    addressed_to_us = False
    if message and 'text' in message:
        message_text = message.get('text')
        if (message_text.startswith(at_bot) or
                message_text.startswith(at_bot + ':')):
            addressed_to_us = True
    return addressed_to_us


def cleanse_command_message(command_message):
    """
    Typically the command message starts with @bot, followed by the
    command and args. For example:
    
    @bot command arg1 arg2 ...
    @bot : command arg1 arg2 ...
    
    This method will strip out the @bot [:] portion of the message
    
    :param command_message: the command message line 
    :return: a tuple of (
        True if the command message matches the expected format, 
        the cleansed message line)
    """
    pattern = re.compile("\s*"+AT_BOT+"\s*[:,-]*\s*")
    return pattern.match(command_message), pattern.sub('', command_message)


def process_command(message_dict, command_processor=None):
    """
    Process a command to the bot, The command is the portion of the post
    from a user with the initial @bot or @bot: portion of the post 
    removed.
    
    :param message_dict: the original message dict for context
    :param command_processor: the command processor function to process a 
        command. The command would be the cleansed message text with
        the @bot prefix stripped.
    :return: the tuple (processed, response dict) where 
        processed is True or False depending on whether the command was handled
        the response dictionary or None if the command was handled
    """
    response = (False, None)
    try:
        matched, message = cleanse_command_message(message_dict['text'])
        if matched and command_processor:
            response = (True, command_processor.process_message(message, message_dict))
    except Exception as e:
        print "Error while processing command. Message: {0}".format(message_dict)
        print "Exception: {0}:{1}".format(e.__class__.__name__, e.message)
        raise e
    return response


def process_message(message, command_processor=None):
    """
    Processes a message that is addressing the bot. The response will be a
    dict with the response text and the channel to respond to.
    
    :param message: the message addressed to the bot. 
    :param command_processor: the command processor object that processes 
        messages
    :return: the response dict
    """
    processed, response = process_command(message, command_processor)
    if not processed:
        response = {
            'channel': message['channel'],
            'text': ':thinking_face: The command is not implemented (yet?)'
        }
    return response


def is_not_none(obj):
    """
    Tests whether the object passed in is not None. There should be an easier 
    way for this.
    
    :param obj: the object to test 
    :return: True if the object is not None
    """
    return obj is not None


slack_client = SlackClient(BOT_API_TOKEN)
users = Users(slack_client)
processor = ResourceReservation(users=users)

events.add_listener(ResourceEventListener(users))
events.add_listener(ConversationListener(users))

if slack_client.rtm_connect():
    print "Connected and running"
    while True:
        for message_dict in slack_client.rtm_read():
            print "Message read: {}".format(message_dict)
            try:
                if is_message_to_bot(message_dict, AT_BOT):
                    response = process_message(message_dict, processor) or {}
                    if response.get('channel') and response.get('text'):
                        post(slack_client,
                             response['channel'], response['text'])
            except Exception as e:
                post(slack_client, message_dict['channel'],
                     ":expressionless: This is where a *500 "
                     "Internal Server Error* would be displayed: {0}-{1}".format(
                        e.__class__.__name__, e.message))

        time.sleep(READ_WEBSOCKET_DELAY)
else:
    print "Connection failed"
