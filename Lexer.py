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
        self.__repr__ = self.revealSelf

    def revealSelf(self):
        return '{0}'.format(self.currentToken)

    def setContext(self, contexts):
        self.contexts = contexts

    def createWordGenerator(self):
        for lst in self.lists:
            for word in lst:
                yield word
        while True:
            yield None

    def advance(self, expectedSymbol = None):
        nextWord = next(self.wordGenerator)
        for context in self.contexts:
            self.currentToken = context.createToken(nextWord)
            if self.currentToken != SyntaxError:
                break
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expected ' + expectedSymbol + ' but is ' + self.currentToken.id)
        return self.currentToken

    def peep(self, expectedSymbol = None):
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expected ' + expectedSymbol + ' but is ' + self.currentToken.id)
        return self.currentToken