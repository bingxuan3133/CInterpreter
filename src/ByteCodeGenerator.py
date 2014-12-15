__author__ = 'JingWen'

from Oracle import *
from Context import *
from ContextManager import *





class ByteCodeGenerator:
    byteCodeList = []
    byteRequired = {'int': 4}
    registersInThisAST = {}

    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        self.oracle = Oracle()

    def assignRegister(self, targetRegister, registerToBeAssigned):
        number = 0xfa | targetRegister << 8 | registerToBeAssigned << 11
        self.byteCodeList.append(number)
        return number

    def storeMultiple(self, targetRegister, registerToPush):
        number = 0xfb | targetRegister << 8 | registerToPush << 11
        self.byteCodeList.append(number)
        return number
    def addRegister(self, registerNumber, valueToAdd):
        number = 0xfc | registerNumber << 8 | valueToAdd << 11
        self.byteCodeList.append(number)
        return number

    def subRegister(self, registerNumber, valueToSubtract):
        number = 0xfb | registerNumber << 8 | valueToSubtract << 11
        self.byteCodeList.append(number)
        return number

    def loadValue(self, registerNumber, valueToAssign):
        number = 0xfc | registerNumber << 8 | valueToAssign << 11
        self.byteCodeList.append(number)
        return number

    def storeValue(self, targetRegister, framePointer, relativeAddress):
        number = 0xfd | targetRegister << 8 | framePointer << 11 | relativeAddress << 14
        self.byteCodeList.append(number)
        return number

    def loadRegister(self, targetRegisterNumber, registerNumber, relativeAddress):
        number = 0xfe | targetRegisterNumber << 8 | registerNumber << 11 | relativeAddress << 17
        self.byteCodeList.append(number)
        return number

    def storeRegister(self, targetRegisterNumber, registerNumber, relativeAddress):
        number = 0xff | targetRegisterNumber << 8 | registerNumber << 11 | relativeAddress << 17
        self.byteCodeList.append(number)
        return number

    def initGeneration(self):
        thisGenerator = self
        def subtract(self):
            pass
        def divide(self):
            pass
        def multiply(self):
            pass
        def nothing(self):
            pass
        def storeValueToRegister(self):
            if thisGenerator.oracle.registerLeft < abs(self.registerRequired) or \
                thisGenerator.oracle.registerLeft < self.leftValue + self.rightValue:
                number = 0b000000 | 0b1 << (6-1-thisGenerator.oracle.releaseAWorkingRegister())
                thisGenerator.storeMultiple(7, number)


            if self.registerRequired > 0:
                for index in range(len(self.data), 0, -1):
                    if self.data[index].id == '(identifier)':
                        thisGenerator.loadRegister(thisGenerator.oracle.getAFreeWorkingRegister(), 7, thisGenerator.registersInThisAST[self.data[index].data[0]])
                    elif self.data[index].id == '(literal)':
                        thisGenerator.loadValue(thisGenerator.oracle.getAFreeWorkingRegister(),self.data[index].data[0])
                    else:
                        self.data[index].generateByteCode()
            else:
                for index in range(0, len(self.data)):
                    if self.data[index].id == '(identifier)':
                        thisGenerator.loadRegister(thisGenerator.oracle.getAFreeWorkingRegister(), 7, thisGenerator.registersInThisAST[self.data[index].data[0]])
                    elif self.data[index].id == '(literal)':
                        thisGenerator.loadValue(thisGenerator.oracle.getAFreeWorkingRegister(),self.data[index].data[0])
                    else:
                        self.data[index].generateByteCode()

            secondRegister = thisGenerator.oracle.releaseAWorkingRegister()
            firstRegister = thisGenerator.oracle.releaseAWorkingRegister()
            thisGenerator.assignRegister(firstRegister, secondRegister)
            return thisGenerator.byteCodeList

        def addRegisterValueAndPlaceIntoARegister(self):
            pass
        def loadIdentifierIntoRegister(self):
            pass
        def loadLiteralIntoRegister(self):
            pass
        def initialization(self):
            variableCounter = 0
            for token in self:
                if token.id in thisGenerator.byteRequired:
                    variableCounter += 1

                thisGenerator.subRegister(7, thisGenerator.byteRequired[self.id]*variableCounter)
                return thisGenerator.byteCodeList

        respectiveByteCodeFunction = {'(literal)': loadLiteralIntoRegister, '(identifier)': loadIdentifierIntoRegister, \
                                            'int': initialization, '=': storeValueToRegister, '+': addRegisterValueAndPlaceIntoARegister, \
                                            '-': subtract, '*': multiply, '/': divide, \
                                            '(systemToken)': nothing, ';': nothing, ',': nothing, '}': nothing, '{': nothing}
        #Start the initialization
        self.byteCodeList = []
        for context in self.contextManager.currentContexts:
            for token in context.symbolTable:
                context.symbolTable[token].generateByteCode = respectiveByteCodeFunction[token]



    #Helper function

    def injectRegisterRequired(self, token):
        registerNumber =[]
        for element in token.data:
            if element.id == '(identifier)' or element.id == '(literal)':
                element.registerRequired = 1
                tempRegisterRequired = 1
            else:
                tempRegisterRequired = self.injectRegisterRequired(element)

            registerNumber.append(tempRegisterRequired)
        if abs(registerNumber[0]) == abs(registerNumber[1]):
            largest = -abs(registerNumber[0])-1
        elif abs(registerNumber[0]) > abs(registerNumber[1]):
            largest = -abs(registerNumber[0])
        else:
            largest = abs(registerNumber[1])
        token.registerRequired = largest
        return largest

    def generateProcessCode(self, token): #Developing
        if token.registerRequired == 1:
            pass
        elif token.registerRequired > 0:
            self.generateProcessCode(token.data[1])
            self.generateProcessCode(token.data[0])
        elif token.registerRequired < 0:
            self.generateProcessCode(token.data[0])
            self.generateProcessCode(token.data[1])
        if token.id == '(identifier)' or token.id == '=':
            function = self.respectiveByteCodeFunction[token.id]
            function(self.getAFreeWorkingRegister(), 7, self.registersInThisAST[token.data[0]])
        else:
            function = self.respectiveByteCodeFunction[token.id]
            function(self.getAFreeWorkingRegister(), token.data[0])






    #For the moment, these function is not been used
    """

        def generateByteCode(self, token):
        if token[0].id == '{':
            token = token[0].data

        self.byteCodeList =[]
        index = 0
        index = self.generateInitializationCode(token, index)

        for value in range(index, len(token)):
            self.injectRegisterRequired(token[value])
            self.generateProcessCode(token[value])


    #define the sub-routine that generate byteCode(Infix)
        def generateInfixByteCode():
            for dataIndex in range(0, len(token.data)):
                if not isinstance(token.data[dataIndex], int):
                    token.data[dataIndex].generateByteCode()
            suitableFunction = self.respectiveByteCodeFunction[self.getAFreeWorkingRegister()]
            code = suitableFunction()
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
        #define the sub-routine that generate byteCode(literal)
        def generateLiteralByteCode():
            self.updateTheWorkingRegisterCounterAndStatus()
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | token.data[0])
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
    def injectLevel(self, token):
        levels =[]
        for element in token.data:
            if element.id == '(identifier)' or element.id == '(literal)':
                element.level = 0
                tempLevel = 0
            else:
                tempLevel = self.injectLevel(element)

            levels.append(tempLevel)
        if abs(levels[0]) >= abs(levels[1]):
            largest = -abs(levels[0])

        else:
            largest = abs(levels[1])
        if largest >= 0:
            largest += 1
        else:
            largest -= 1
        token.level = largest
        return largest

    def assignRegisters(self, register1, register2):
        number = 0xfa | register1 << 8 | register2 << 11
        self.byteCodeList.append(number)
        return number

        #Start to make a fake switch case.
        def storeIntoWorkingRegisterTwo():
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | self.workingRegisterCounter-2 << 8 | self.workingRegisterCounter-1)
            self.registerStatus[self.workingRegisterCounter-1] = 0
            self.registerStatus[self.workingRegisterCounter-2] = 0
            return code
        def storeIntoWorkingRegisterOne():
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | self.workingRegisterCounter+1 << 8 | self.workingRegisterCounter-1)
            self.registerStatus[self.workingRegisterCounter+1] = 0
            self.registerStatus[self.workingRegisterCounter-1] = 0
            return code
        def storeIntoWorkingRegisterZero():
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | self.workingRegisterCounter+1 << 8 | self.workingRegisterCounter+2)
            self.registerStatus[self.workingRegisterCounter+1] = 0
            self.registerStatus[self.workingRegisterCounter+2] = 0
            return code
        storeLocation = {0: storeIntoWorkingRegisterZero, 1: storeIntoWorkingRegisterOne, 2: storeIntoWorkingRegisterTwo}
        ###############################################################################################################
        thisGenerator = self
        #define the sub-routine that generate byteCode(Infix)
        def generateInfixByteCode():
            for dataIndex in range(0, len(token.data)):
                if not isinstance(token.data[dataIndex], int):
                    token.data[dataIndex].generateByteCode()
            self.updateTheWorkingRegisterCounterAndStatus()
            suitableFunction = storeLocation[self.workingRegisterCounter]
            code = suitableFunction()
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
        #define the sub-routine that generate byteCode(literal)
        def generateLiteralByteCode():
            self.updateTheWorkingRegisterCounterAndStatus()
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | token.data[0])
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
        #end define the generation subroutine
        ###############################################################################################################
        #Start the initialization
        self.byteCodeList = []
        if token.id == '(literal)':
            token.generateByteCode = generateLiteralByteCode
        else:
            for context in self.contextManager.currentContexts:
                if token.id in context.symbolTable:
                    if token.arity == self.context.BINARY:
                        token.generateByteCode = generateInfixByteCode
        for dataIndex in range(0, len(token.data)):
            if token.id != '(literal)':
                self.initGeneration(token.data[dataIndex])
    """
