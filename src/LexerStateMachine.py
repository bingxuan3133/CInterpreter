__author__ = 'Jing'

from Context import *

class LexerStateMachine:
    def __init__(self, string, context):
        self.lists = []
        self.string = string
        self.context = context
        if string is not None:
            statements = string.split('\n')
            for statement in statements:
                self.lists.append(statement.strip())
                self.lists.append(' ')
            self.lists.pop()
        #self.currentToken = self.advance()
        #self.__repr__ = self.revealSelf
        self.charGenerator = self.createCharGenerator()


    def createCharGenerator(self):
        for str in self.lists:
            for word in str:
                for ch in word:
                    yield ch
        while True:
            yield None

    def getNextChar(self):
        nextChar = next(self.charGenerator)
        return nextChar