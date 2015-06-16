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
        self.currentChar = None
        self.currentString = None


    def createCharGenerator(self):
        for str in self.lists:
            for word in str:
                for ch in word:
                    yield ch
        while True:
            yield None

    def getNextChar(self):
        nextChar = self.currentChar
        self.currentChar = next(self.charGenerator)
        return nextChar

    def start(self):
        self.waitChar()

    def waitChar(self):
        while self.isSpace():
            self.getNextChar()

        if self.isNumber():
            self.currentString = 0
            self.captureNumber()
            self.value()

        elif self.isDot():
            self.floatingPoint()

        elif self.isAlpha() or self.isUnderScore():
            self.currentString = ''
            self.captureIdentifier()
            self.identifier()

        elif self.isOperator():
            self.captureOperator()
            self.operator()

    def value(self):
        while self.isNumber():
            self.captureNumber()

        if self.isDot():
            self.floatingPointDot()
        elif self.isE():
            self.floatingPointE()

    def floatingPointDot(self):
        if (not self.isNumber()) and self.noIntegerPart():
            raise SyntaxError("Expecting number before/after (.)")

        tempNumber = 0
        while self.isNumber():
            tempNumber += self.getNextChar()
            tempNumber /= 10
        self.currentString += tempNumber

        self.end()

    def floatingPointE(self):
        if self.isPlusOrMinusSign() or self.isNumber():
            self.capture
        tempNumber = 0
        while self.isNumber():
            tempNumber *= 10
            tempNumber += self.getNextChar()
        for num in range (0,tempNumber):
            self.currentString *= 10

        self.end()



    def identifier(self):
        while self.isNumber() or self.isAlpha() or self.isUnderScore():
            self.captureIdentifier()
        self.end()

    def operator(self):
        while self.isMultipleSymbolOperator():
            self.captureOperator()
        self.end()

    def end(self):
        pass

    def captureNumber(self):
        self.currentString *= 10
        self.currentString += self.getNextChar()

    def captureIdentifier(self):
        self.currentString += self.getNextChar()

    def captureOperator(self):
        self.currentString = self.getNextChar()

    def isSpace(self):
        return  self.currentChar == ' '

    def isNumber(self):
        return isinstance(self.currentChar,(int))

    def isDot(self):
        return self.currentChar == '.'

    def noIntegerPart(self):
        return not isinstance(self.currentChar,(int))

    def isAlpha(self):
        return isinstance(self.currentChar, (str))

    def isUnderScore(self):
        return self.currentChar == '_'

    def isOperator(self):
        operatorLibrary = ['+','-','*','/']
        return self.currentChar in operatorLibrary
