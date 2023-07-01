AUTHORIZATION_TOKEN = 'I-trust-U'

# auth
TEXT_YOU_ARE_NOT_AUTHORIZED = 'You are not authorized. Please, send me authorization code'
TEXT_WRONG_AUTH_TOKEN = 'Wrong auth token. Please, send me authorization code'
TEXT_THANKS_YOU_ARE_NOW_AUTHORIZED = 'Thanks! You are authorized to work with me'
TEXT_YOU_ARE_ALREADY_AUTHORIZED = 'You are already authorized'

# cancel
TEXT_NO_ACTIVE_COMMAND = "No active command to cancel. I wasn't doing anything anyway. Zzzzz..."


def FORMAT_COMMAND_HAS_BEEN_CANCELLED(command):
    return f"The command {command} has been cancelled. Anything else I can do for you?\n\n" \
                             "Send /help for a list of commands."


# forget me
TEXT_YOU_ACCOUNT_IS_DELETED = 'You account is deleted'
