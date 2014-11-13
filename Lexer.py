from Context import *

class Lexer:
    def __init__(self, string, context):
        self.lists = []
        self.string = string
        self.context = context
        self.wordGenerator = self.createWordGenerator()
        if string is not None:
            statements = string.split('\n')
            for statement in statements:
                self.lists.append(statement.split())
        self.currentToken = self.advance()
        self.__repr__ = self.revealSelf

    def revealSelf(self):
        return '{0}'.format(self.currentToken)

    def createWordGenerator(self):
        for lst in self.lists:
            for word in lst:
                yield word
        while True:
            yield None

    def advance(self, expectedSymbol = None):
        nextWord = next(self.wordGenerator)
        self.currentToken = self.context.createToken(nextWord)
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expected ' + expectedSymbol + ' but is ' + self.currentToken.id)
        return self.currentToken

    def peep(self, expectedSymbol = None):
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expected ' + expectedSymbol + ' but is ' + self.currentToken.id)
        return self.currentToken