__author__ = 'Jing'

from Context import *
from InStream import *
import string

class LexerStateMachine:
    def __init__(self, string, context):
        self.context = context
        self.inStream = InStream(string)
        self.currentString = ''
        self.capture()
        self.currentToken = self.advance()

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
            self.inStream.getNextChar()

        if self.isZero():
            self.capture()
            self.initialZero()

        elif self.isNumber():
            self.capture()
            self.value()

        elif self.isDot():
            if self.inStream.previousChar.isalnum() or self.inStream.previousChar == '_':
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
            caretMessage = ' '*(self.inStream.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting X/x, B/b, . or octal number after {}.\n{}\n{}"\
                              .format(self.inStream.line,self.inStream.column,self.inStream.previousChar,self.inStream.oriString,caretMessage))

    def initialDot(self):
        if self.isNumber():
            self.capture()
            self.floatingPointDot()
        else:
            caretMessage = ' '*(self.inStream.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting number after .\n{}\n{}"\
                              .format(self.inStream.line,self.inStream.column,self.inStream.oriString,caretMessage))

    def floatingPointDot(self):
        if self.inStream.previousChar == None or self.inStream.previousChar.isalpha():
            pass
        else:
            while self.isNumber():
                self.capture()

        self.end()

    def floatingPointE(self):
        self.inStream.getNextChar()
        if self.isPlusOrMinusSign() or self.isNumber():
            self.floatingPointEWithNotation()
        elif not self.isNumber():
            caretMessage = ' '*(self.inStream.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting a positive or negative number after E/e.\n{}\n{}"\
                              .format(self.inStream.line,self.inStream.column,self.inStream.oriString,caretMessage))

    def floatingPointEWithNotation(self):
        tempNumber = 0
        tempResult = int(self.currentString)
        tempNotation = self.inStream.currentChar
        if self.isPlusOrMinusSign():
            self.inStream.getNextChar()
            if not self.isNumber():
                caretMessage = ' '*(self.inStream.column-1)+'^'
                raise SyntaxError("Error[{}][{}]:Unexpected symbol \"{}\" been found after {}\n{}\n{}"\
                                  .format(self.inStream.line,self.inStream.column,self.inStream.currentChar, tempNotation,self.inStream.oriString,caretMessage))
        while self.isNumber():
            tempNumber *= 10
            tempNumber += int(self.inStream.getNextChar())

        for num in range(0, tempNumber):
            if tempNotation == '-':
                tempResult /= 10
            else:
                tempResult *= 10

        self.currentString = str(format(tempResult, '.100f'))

        self.end()

    def hexadecimal(self):
        if not self.isHexadecimal():
            caretMessage = ' '*(self.inStream.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting hex number after {}\n{}\n{}"\
                              .format(self.inStream.line,self.inStream.column,self.currentString,self.inStream.oriString,caretMessage))

        while self.isHexadecimal():
            self.capture()

        if self.isAlpha() and not self.isHexadecimal():
            caretMessage = ' '*(self.inStream.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting hex number after {}\n{}\n{}"\
                              .format(self.inStream.line,self.inStream.column,self.currentString[self.currentString.__len__()-1],self.inStream.oriString,caretMessage))
        self.currentString = str(int(self.currentString, 16))
        self.end()

    def octal(self):
        while self.isOctal():
            self.capture()

        if self.isNumber() and not self.isOctal():
            caretMessage = ' '*(self.inStream.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting octal number after {}\n{}\n{}"\
                              .format(self.inStream.line,self.inStream.column,self.currentString[self.currentString.__len__()-1],self.inStream.oriString,caretMessage))

        self.currentString = str(int(self.currentString, 8))
        self.end()

    def binary(self):
        while self.isBinary():
            self.capture()

        if self.isNumber() and not self.isBinary():
            caretMessage = ' '*(self.inStream.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting binary number after {}\n{}\n{}"\
                              .format(self.inStream.line,self.inStream.column,self.currentString[self.currentString.__len__()-1],self.inStream.oriString,caretMessage))

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
        self.currentString += self.inStream.getNextChar()

    def resetCurrentString(self):
        self.currentString = ''

    #End Action functions

    #Checking functions
    def isSpace(self):
        return self.inStream.currentChar == ' '

    def isNumber(self):
        if self.inStream.currentChar is None:
            return False
        else:
            return self.inStream.currentChar.isdigit()

    def isDot(self):
        return self.inStream.currentChar == '.'

    def isAlpha(self):
        if self.inStream.currentChar is None:
            return False
        else:
            return self.inStream.currentChar.isalpha() and self.inStream.currentChar != ' ' and self.inStream.currentChar != '.'

    def isUnderScore(self):
        return self.inStream.currentChar == '_'

    def isOperator(self):
        return isinstance(self.inStream.currentChar,str) and not self.inStream.currentChar.isalpha()

    def isPlusOrMinusSign(self):
        return self.inStream.currentChar == '+' or self.inStream.currentChar == '-'

    def isE(self):
        return self.inStream.currentChar == 'e' or self.inStream.currentChar == 'E'

    def isMultipleSymbolOperator(self):
        potentialSymbol = ['+','-','=']
        return self.inStream.currentChar in potentialSymbol

    def isEnd(self):
        return self.inStream.currentChar is None

    def isZero(self):
        return self.inStream.currentChar == '0'

    def isHexaSign(self):
        return self.inStream.currentChar == 'X' or self.inStream.currentChar == 'x'

    def isBinSign(self):
        return self.inStream.currentChar == 'B' or self.inStream.currentChar == 'b'

    def isHexadecimal(self):
        if self.inStream.currentChar is None:
            return False
        else:
            return self.inStream.currentChar in string.hexdigits

    def isOctal(self):
        if self.inStream.currentChar is None:
            return False
        else:
            return self.inStream.currentChar in string.octdigits

    def isBinary(self):
        if self.inStream.currentChar is None:
            return False
        else:
            return self.inStream.currentChar == '0' or self.inStream.currentChar == '1'
    #End checking functions