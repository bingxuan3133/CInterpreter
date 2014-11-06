# Pratt's parser implementation
from Lexer import *
from Context import *

class Parser:
    def __init__(self, statement, contexts):
        self.lexer = Lexer(statement, contexts)
        self.contexts = contexts
        self.lexer.setContext(self.contexts)

    def parse(self, bindingPower):
        token = self.lexer.peep()        # token = leftToken
        token = token.nud()
        token2 = self.lexer.peep()
        while bindingPower < token2.bindingPower:  # left < right
            token = token2.led(token)
            token2 = self.lexer.peep()
        return token  # number token: come in first time, else operator token: after rolling in the while loop



