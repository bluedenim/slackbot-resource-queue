from abc import ABCMeta, abstractmethod


class Processor:
    """
    Base abstract command processor class. Processor implementations should:
        - override the dispatch() method to map commands to methods and
        - implement the dispatched methods that:
            - accepts a params list of Strings and a context dictionary
            - return a list of text responses
    """
    __metaclass__ = ABCMeta

    NOT_IMPLEMENTED_MSG = ':thinking_face: The command is not implemented (yet?)'

    def __init__(self, users):
        """
        
        :param users: an instance of Users to use for user look-up
        """
        self.users = users

    def not_implemented(self, params, context):
        """
        Default handler of an unimplemented command
        
        :param params: the parameters for the command
        :param context: the context dictionary providing more context info
        :return: response texts
        """
        return [
            Processor.NOT_IMPLEMENTED_MSG
        ]

    def format_at_user(self, user_id):
        """
        Formats a user ID with the <@ > tag. This is used in messages
        to flag the user's attention and also to provide a link to the
        user. If the user_id is None, then "nobody" is returned.
        
        :param user_id: the user ID
        :return: a formatted string suitable for use in a post
        """
        if user_id:
            return "<@{}>".format(user_id)
        else:
            return None

    def format_user(self, user_id, active=True):
        """
        Formats the user either as an active "link" or simply the user's name.
        This method uses the users collaborator to get at user names.
        :param user_id: the user ID to format
        :param active: if True, then an active link to the user is returned.
            If False, then the user name is returned.
            
        :return: the formatted value for the user ID provided or None 
        """
        formatted = None
        if active:
            formatted = self.format_at_user(user_id)
        else:
            if user_id:
                user_profile = self.users.get_user_info(user_id)
                if user_profile:
                    formatted = "{}".format(user_profile['name'])
        return formatted

    def format_users(self, user_ids, active=True):
        """
        Formats a collection of user IDs 
        :param user_ids: user IDs to format
        :param active: if True, then an active link to the user is returned.
            If False, then the user name is returned.
        :return: formatted values for the user IDs provided. If any user ID cannot
            be formatted, it will be skipped from the returned list.
            The returned list CAN be empty.
        """
        if user_ids:
            formatted_values = [
                self.format_user(user_id, active=active)
                for user_id in user_ids if user_id]
            return [formatted_value for formatted_value in formatted_values
                    if formatted_value]
        else:
            return []

    @abstractmethod
    def dispatch(self, command):
        return self.not_implemented

    def process_message(self, message, context_dict):
        """
        Process a message and return a result dictionary. The result dictionary must
        include at least the keys 'channel' and 'text', indicating the channel and
        response text to respond with, respectively.

        :param message: the message to process
        :param context_dict: the context dictionary with information about the
            environment/context of the message
        :return: a dict 
        """
        tokens = message.split()
        command = tokens.pop(0)
        handler = self.dispatch(command) or self.not_implemented
        responses = handler(tokens, context_dict)

        result = {
            'channel': context_dict['channel']
        }
        if responses:
            result['text'] = '\n'.join(responses)
        return result
