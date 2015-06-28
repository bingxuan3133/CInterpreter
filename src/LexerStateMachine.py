__author__ = 'Jing'

from Context import *
import string

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

        self.currentChar = ''
        self.previousChar = ''
        self.currentString = ''
        self.capture()
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
        self.previousChar = nextChar
        self.currentChar = next(self.charGenerator)
        return nextChar
    #end "stream" function

    #API for application
    def advance(self, expectedSymbol = None):

        self.start()
        self.currentToken = self.context.createToken(self.currentString)
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expecting ' + expectedSymbol + ' before ' + self.currentToken.id)
        self.resetCurrentString()
        return self.currentToken

    def peep(self, expectedSymbol = None):
        if expectedSymbol is not None and self.currentToken.id != expectedSymbol:
            raise SyntaxError('Expecting ' + expectedSymbol + ' before ' + self.currentToken.id)
        return self.currentToken
    #End API

    #State machine for the lexer
    def start(self):
        self.waitChar()

    def waitChar(self):
        while self.isSpace():
            self.getNextChar()

        if self.isZero():
            self.capture()
            self.initialZero()

        elif self.isNumber():
            self.capture()
            self.value()

        elif self.isDot():
            if self.previousChar.isalnum() or self.previousChar == '_':
                self.capture()
                self.end()
            else:
                self.capture()
                self.initialDot()

        elif self.isAlpha() or self.isUnderScore():
            self.capture()
            self.identifier()

        elif self.isOperator():
            self.capture()
            self.operator()

        elif self.isEnd():
            self.currentString = None
            return
        else:
            raise SyntaxError("Undefine symbol")

    def value(self):
        while self.isNumber():
            self.capture()
        if self.isDot():
            self.capture()
            self.floatingPointDot()
        elif self.isE():
            self.floatingPointE()
        else:
            self.end()

    def initialZero(self):
        if self.isHexaSign():
            self.capture()
            self.hexadecimal()
        elif self.isOctal():
            self.capture()
            self.octal()
        elif self.isBinSign():
            self.capture()
            self.binary()
        elif self.isDot():
            self.capture()
            self.floatingPointDot()
        else:
            raise SyntaxError("Expecting X/x, B/b, . or octal number after " + self.previousChar)

    def initialDot(self):
        if self.isNumber():
            self.capture()
            self.floatingPointDot()
        else:
            raise SyntaxError("Expecting number after .")

    def floatingPointDot(self):
        if self.previousChar == None or self.previousChar.isalpha():
            pass
        else:
            while self.isNumber():
                self.capture()

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
            if not self.isNumber():
                raise SyntaxError("Unexpected symbol \"" + self.currentChar + "\" been found after " + tempNotation)
        while self.isNumber():
            tempNumber *= 10
            tempNumber += int(self.getNextChar())

        for num in range(0, tempNumber):
            if tempNotation == '-':
                tempResult /= 10
            else:
                tempResult *= 10

        self.currentString = str(format(tempResult, '.100f'))

        self.end()

    def hexadecimal(self):
        if not self.isHexadecimal():
            raise SyntaxError("Expecting hex number after " + self.currentString)

        while self.isHexadecimal():
            self.capture()

        if self.isAlpha() and not self.isHexadecimal():
            raise SyntaxError ("Expecting hex number after "+self.currentString[self.currentString.__len__()-1])

        self.currentString = str(int(self.currentString, 16))
        self.end()

    def octal(self):
        while self.isOctal():
            self.capture()

        if self.isNumber() and not self.isOctal():
            raise SyntaxError("Expecting octal number after "+self.currentString[self.currentString.__len__()-1])

        self.currentString = str(int(self.currentString, 8))
        self.end()

    def binary(self):
        while self.isBinary():
            self.capture()

        if self.isNumber() and not self.isBinary():
            raise SyntaxError("Expecting binary number after "+self.currentString[self.currentString.__len__()-1])

        self.currentString = str(int(self.currentString, 2))
        self.end()

    def identifier(self):
        while self.isNumber() or self.isAlpha() or self.isUnderScore():
            self.capture()
        self.end()

    def operator(self):
        if self.isMultipleSymbolOperator():
            self.capture()
        self.end()

    def end(self):
        pass
    #End State Machine

    #Action functions
    def capture(self):
        self.currentString += self.getNextChar()

    def resetCurrentString(self):
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

    def isAlpha(self):
        if self.currentChar is None:
            return False
        else:
            return self.currentChar.isalpha() and self.currentChar != ' ' and self.currentChar != '.'

    def isUnderScore(self):
        return self.currentChar == '_'

    def isOperator(self):
        return isinstance(self.currentChar,str) and not self.currentChar.isalpha()

    def isPlusOrMinusSign(self):
        return self.currentChar == '+' or self.currentChar == '-'

    def isE(self):
        return self.currentChar == 'e' or self.currentChar == 'E'

    def isMultipleSymbolOperator(self):
        potentialSymbol = ['+','-','=']
        return self.currentChar in potentialSymbol

    def isEnd(self):
        return self.currentChar is None

    def isZero(self):
        return self.currentChar == '0'

    def isHexaSign(self):
        return self.currentChar == 'X' or self.currentChar == 'x'

    def isBinSign(self):
        return self.currentChar == 'B' or self.currentChar == 'b'

    def isHexadecimal(self):
        if self.currentChar is None:
            return False
        else:
            return self.currentChar in string.hexdigits

    def isOctal(self):
        if self.currentChar is None:
            return False
        else:
            return self.currentChar in string.octdigits

    def isBinary(self):
        if self.currentChar is None:
            return False
        else:
            return self.currentChar == '0' or self.currentChar == '1'
    #End checking functions