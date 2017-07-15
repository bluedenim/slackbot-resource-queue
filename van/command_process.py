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
