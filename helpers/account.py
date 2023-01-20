import re
import string
import random


class TokenGenerator:

    TOKEN_PATTERN = re.compile("[A-Z0-9-]{6}")

    @classmethod
    def get_token(cls, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @classmethod
    def validate_token_pattern(cls, token):
        return TokenGenerator.TOKEN_PATTERN.match(token)
