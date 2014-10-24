from Context import *

class Lexer:
    def __init__(self, string, contexts):
        self.lists = []
        self.string = string
        self.contexts = contexts
        self.wordGenerator = self.createWordGenerator()
        if string is not None:
            statements = string.split('\n')
            for statement in statements:
                self.lists.append(statement.split())
        self.currentToken = self.advance()


    def setContext(self, contexts):
        self.contexts = contexts

    def createWordGenerator(self):
        for lst in self.lists:
            for word in lst:
                yield word
        while True:
            yield None

    def advance(self):
        self.currentToken = self.contexts[0].createToken(next(self.wordGenerator))
        return self.currentToken

    def peep(self):
        return self.currentToken
"""
def advance(self):
    if self.nextValue is not None:
        self.lastValue = self.nextValue
        self.nextValue = None
    else:
        self.lastValue = next(self.wordGenerator)
    token = self.contexts[0].createToken(self.lastValue)
    return token

def lookAHead(self):
    if self.nextValue is None:
        self.nextValue = next(self.wordGenerator)
    return self.contexts[0].createToken(self.nextValue)
"""

"""
for context in self.contexts:
    token = context.createToken(word)
    if(token != SyntaxError):
        break
"""