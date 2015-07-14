__author__ = 'Jing'

class InStream:
    def __init__(self, string):
        self.lists = []
        self.string = string
        if string is not None:
            statements = string.split('\n')
            for statement in statements:
                self.lists.append(statement.strip())
                self.lists.append(' ')
            self.lists.pop()
        self.charGenerator = self.createCharGenerator()
        self.currentChar = ''
        self.previousChar = ''
        self.oriString = ''
        self.line = 0
        self.column = 0

    def createCharGenerator(self):
        for str in self.lists:
            self.oriString = str
            if str != ' ':
                self.line += 1
            for word in str:
                for ch in word:
                    self.column += 1
                    yield ch
            temp = self.column
            self.column = 0
        self.column = temp
        while True:
            yield None

    def getNextChar(self):
        nextChar = self.currentChar
        self.previousChar = nextChar
        self.currentChar = next(self.charGenerator)
        return nextChar