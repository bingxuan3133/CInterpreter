__author__ = 'Jing'

class InStream:
    def __init__(self, string):
        self.lists = []
        self.string = string
        if string is not None:
            tempWord = ""
            for char in string:
                if char != '\n':
                    tempWord += char
                else:
                    self.lists.append(tempWord)
                    self.lists.append(' ')
                    tempWord = ""
            self.lists.append(tempWord)
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
        self.column = temp + 1
        while True:
            yield None

    def getNextChar(self):
        nextChar = self.currentChar
        self.previousChar = nextChar
        self.currentChar = next(self.charGenerator)
        return nextChar