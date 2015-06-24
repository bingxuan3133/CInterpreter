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
        self.charGenerator = self.createCharGenerator()

        self.currentChar = None
        self.currentString = ''
        self.currentToken = self.advance()

    #Function that belong to "stream"
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
    #end "stream" function

    #API for application
    def advance(self, expectedSymbol = None):
        self.resetTheLexer()
        self.start()
        self.currentToken = self.context.createToken(self.currentString)
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expected ' + expectedSymbol + ' but is ' + self.currentToken.id)
        return self.currentToken

    def peep(self, expectedSymbol = None):
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expected ' + expectedSymbol + ' but is ' + self.currentToken.id)
        return self.currentToken
    #End API

    #State machine for the lexer
    def start(self):
        self.getNextChar()
        self.waitChar()

    def waitChar(self):
        while self.isSpace():
            self.getNextChar()

        if self.isNumber():
            self.captureNumber()
            self.value()

        elif self.isDot():
            self.floatingPointDot()

        elif self.isAlpha() or self.isUnderScore():
            self.captureIdentifier()
            self.identifier()

        elif self.isOperator():
            self.captureOperator()
            self.operator()

        elif self.isEnd():
            return
        else:
            raise SyntaxError("Undefine symbol")

    def value(self):
        while self.isNumber():
            self.captureNumber()

        if self.isDot():
            self.floatingPointDot()
        elif self.isE():
            self.floatingPointE()
        else:
            self.end()

    def floatingPointDot(self):

        tempNumber = 0
        while self.isNumber():
            tempNumber += self.getNextChar()
            tempNumber /= 10
        self.currentString += tempNumber
        if (not self.isNumber()) and self.noIntegerPart():
            raise SyntaxError("Expecting number before/after (.)")

        self.end()

    def floatingPointE(self):
        self.getNextChar()
        if self.isPlusOrMinusSign() or self.isNumber():
            self.floatingPointEWithNotation()
        elif not self.isNumber():
            pass
            raise SyntaxError("Expecting a positive or negative number after E/e.")

    def floatingPointEWithNotation(self):
        tempNumber = 0
        tempResult = int(self.currentString)
        tempNotation = self.currentChar
        if self.isPlusOrMinusSign():
            self.getNextChar()
        while self.isNumber():
            tempNumber *= 10
            tempNumber += int(self.getNextChar())
        if tempNotation == '-':
            for num in range(0, tempNumber):
                tempResult /= 10
        else:
            for num in range(0, tempNumber):
                tempResult *= 10

        self.currentString = str(format(tempResult, '.100f'))

        self.end()

    def identifier(self):
        while self.isNumber() or self.isAlpha() or self.isUnderScore():
            self.captureIdentifier()
        self.end()

    def operator(self):
        if self.isMultipleSymbolOperator():
            self.captureOperator()
        self.end()

    def end(self):
        pass
    #End State Machine

    #Action functions
    def captureNumber(self):
        self.currentString += self.getNextChar()

    def captureIdentifier(self):
        self.currentString += self.getNextChar()

    def captureOperator(self):
        self.currentString = self.getNextChar()

    def resetTheLexer(self):
        self.currentChar = None
        self.currentString = ''

    #End Action functions

    #Checking functions
    def isSpace(self):
        return self.currentChar == ' '

    def isNumber(self):
        if self.currentChar is None:
            return False
        else:
            return self.currentChar.isdigit()

    def isDot(self):
        return self.currentChar == '.'

    def noIntegerPart(self):
        return not isinstance(self.currentChar,(int))

    def isAlpha(self):
        if self.currentChar is None:
            return False
        else:
            return isinstance(self.currentChar, (str)) and self.currentChar != ' '

    def isUnderScore(self):
        return self.currentChar == '_'

    def isOperator(self):
        operatorLibrary = ['+', '-', '*', '/']
        return self.currentChar in operatorLibrary

    def isPlusOrMinusSign(self):
        return self.currentChar == '+' or self.currentChar == '-'

    def isE(self):
        return self.currentChar == 'e' or self.currentChar == 'E'

    def isMultipleSymbolOperator(self):
        return self.isPlusOrMinusSign()

    def isEnd(self):
        return self.currentChar is None
    #End checking functions