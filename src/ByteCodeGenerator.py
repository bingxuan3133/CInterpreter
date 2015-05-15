__author__ = 'JingWen'

from Oracle import *
from Context import *
from ContextManager import *
from RegisterAllocator import *


class ByteCodeGenerator:
    byteCodeList = []
    byteRequired = {'int': 4}
    registersInThisAST = {}

    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        self.oracle = Oracle()
        self.registerAllocator = RegisterAllocator(self)

    def nothing(self):
        pass
    def divideRegister(self):
        pass
    def multiplyRegister(self, targetRegister, firstRegister, secondRegister):
        number = 0xf6 | targetRegister << 8 | firstRegister << 11 | secondRegister << 14
        self.byteCodeList.append(number)
        return number

    def loadMultiple(self, sourceRegister, destinationRegister):
        number = 0xf7 | sourceRegister << 8 | destinationRegister << 11
        self.byteCodeList.append(number)
        return number
    def assignRegister(self, sourceRegister, destinationRegister, secondRegister=0):
    #Assign FirstRegister into Second Register and store into targetRegister
        number = 0xf8 | sourceRegister << 8 | destinationRegister << 11
        self.byteCodeList.append(number)
        return number

    def storeMultiple(self, targetRegister, registerToPush):
        number = 0xf9 | targetRegister << 8 | registerToPush << 11
        self.byteCodeList.append(number)
        return number

    def addRegister(self,targetRegister, firstRegister, secondRegister):
        number = 0xfa | targetRegister << 8 | firstRegister << 11 | secondRegister << 14
        self.byteCodeList.append(number)
        return number

    def subRegister(self,targetRegister, registerNumber, valueToSubtract):
        number = 0xfb | targetRegister << 8 | registerNumber << 11 | valueToSubtract << 14
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

    def generateRightCodeFirst(self, token):
        secondTime = 0
        for index in range(len(token.data)-1, -1, -1):
            if token.data[index].id == '(identifier)':
                if secondTime == 0:
                    self.loadRegister(self.oracle.getAFreeWorkingRegister(), 7, self.registersInThisAST[token.data[index].data[0]])
                else:
                    self.loadRegister(self.oracle.getALargestWorkingRegister(), 7, self.registersInThisAST[token.data[index].data[0]])
            elif token.data[index].id == '(literal)':
                if secondTime == 0:
                    self.loadValue(self.oracle.getAFreeWorkingRegister(), token.data[index].data[0])
                else:
                    self.loadValue(self.oracle.getALargestWorkingRegister(), token.data[index].data[0])
            else:
                token.data[index].generateByteCode()
            secondTime += 1

    def generateLeftCodeFirst(self, token):
        secondTime = 0
        for index in range(0, len(token.data)):
            if token.data[index].id == '(identifier)':
                if secondTime == 0:
                    self.loadRegister(self.oracle.getAFreeWorkingRegister(), 7, self.registersInThisAST[token.data[index].data[0]])
                else:
                    self.loadRegister(self.oracle.getALargestWorkingRegister(), 7, self.registersInThisAST[token.data[index].data[0]])
            elif token.data[index].id == '(literal)':
                if secondTime == 0:
                    self.loadValue(self.oracle.getAFreeWorkingRegister(), token.data[index].data[0])
                else:
                    self.loadValue(self.oracle.getALargestWorkingRegister(), token.data[index].data[0])
            else:
                token.data[index].generateByteCode()
            secondTime += 1

    def findOutAndGenerateCorrectSideCode(self, token):
        if token.registerRequiredAtThatLevel > 0:
            self.generateRightCodeFirst(token)
        else:
            self.generateLeftCodeFirst(token)

    def decideWhetherToSaveSlotForPopValue(self, status, generateByteCode):
        firstRegister = self.oracle.releaseALargestWorkingRegister()
        secondRegister = self.oracle.releaseAWorkingRegister()
        if status != 0:
            generateByteCode(firstRegister, secondRegister, firstRegister)
            self.oracle.getALargestWorkingRegister()
        else:
            generateByteCode(secondRegister, secondRegister, firstRegister)
            self.oracle.getAFreeWorkingRegister()

    def initGeneration(self):
        thisGenerator = self

        def initialization(self):
            variableCounter = 0
            for token in self:
                if token.id in thisGenerator.byteRequired:
                    variableCounter += 1

                thisGenerator.subRegister(7, thisGenerator.byteRequired[self.id]*variableCounter)
                return thisGenerator.byteCodeList

        respectiveByteCodeFunction = {'int': initialization, '=': self.assignRegister, '+': self.addRegister, \
                                            '-': self.subRegister, '*': self.multiplyRegister, '/': self.divideRegister, \
                                            '(systemToken)': self.nothing, ';': self.nothing, ',': self.nothing, '}': self.nothing, '{': self.nothing}

        def generateByteCode(self):
            pushed = thisGenerator.registerAllocator.decideWhetherToPush(self)
            thisGenerator.findOutAndGenerateCorrectSideCode(self)

            thisGenerator.decideWhetherToSaveSlotForPopValue(pushed, respectiveByteCodeFunction[self.id])

            thisGenerator.registerAllocator.decideWhetherToPop(pushed)
            return thisGenerator.byteCodeList


        #Start the initialization
        self.byteCodeList = []
        for context in self.contextManager.currentContexts:
            for token in context.symbolTable:
                context.symbolTable[token].generateByteCode = generateByteCode



    #For the moment, these function is not been used
    """

        def generateByteCode(self, token):
        if token[0].id == '{':
            token = token[0].data

        self.byteCodeList =[]
        index = 0
        index = self.generateInitializationCode(token, index)

        for value in range(index, len(token)):
            self.injectregisterRequiredAtThatLevel(token[value])
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
