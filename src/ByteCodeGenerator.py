__author__ = 'JingWen'

from Mapping import *
from RegisterAllocator import *


class ByteCodeGenerator:
    byteCodeList = []
    byteRequired = {'char': 1, 'short': 1, 'int': 4, 'long': 4, 'float': 4, 'double': 8}
    variablesInThisAST = {}
    variableCounter = 0
    memorySize = 0


    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        self.mapping = Mapping()
        self.registerAllocator = RegisterAllocator(self)

    def nothing(self):
        pass

    def compareRegister(self,GPR=[]):
        number = 0xf3 | GPR[0] << 8 | GPR[1] << 11
        return number
    def subFrameRegister(self, GPR=[]):
        number = 0xf4 | GPR[0] << 8 | GPR[1] << 11
        return number

    def divideRegister(self, GPR=[]):
        number = 0xf5 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def multiplyRegister(self, GPR=[]):
        number = 0xf6 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def loadMultiple(self, GPR=[]):
        number = 0xf7 | GPR[0] << 8 | GPR[1] << 11
        return number

    def assignRegister(self, GPR=[]):
        number = 0xf8 | GPR[0] << 8 | GPR[1] << 11
        return number

    def storeMultiple(self, GPR=[]):
        number = 0xf9 | GPR[0] << 8 | GPR[1] << 11
        return number

    def addRegister(self,GPR =[]):
        number = 0xfa | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def subRegister(self,GPR=[]):
        number = 0xfb | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def loadValue(self, GPR=[]):
        number = 0xfc | GPR[0] << 8 | GPR[1] << 11
        return number

    def storeValue(self, GPR=[]):
        number = 0xfd | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def loadRegister(self, GPR=[]):
        number = 0xfe | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 17
        return number

    def storeRegister(self, GPR=[]):
        number = 0xff | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 17
        return number

    def generateRightCodeFirst(self, token):
        secondTime = 0
        for index in range(len(token.data)-1, -1, -1):
            if token.data[index].id == '(identifier)':
                if secondTime == 0:
                    Code = self.loadRegister([self.mapping.getAFreeWorkingRegister(), self.mapping.framePointerRegister, self.variablesInThisAST[token.data[index].data[0]]])
                else:
                    Code = self.loadRegister([self.mapping.getALargestWorkingRegister(), self.mapping.framePointerRegister, self.variablesInThisAST[token.data[index].data[0]]])
                self.byteCodeList.append(Code)
            elif token.data[index].id == '(literal)':
                if secondTime == 0:
                    Code = self.loadValue([self.mapping.getAFreeWorkingRegister(), token.data[index].data[0]])
                else:
                    Code = self.loadValue([self.mapping.getALargestWorkingRegister(), token.data[index].data[0]])
                self.byteCodeList.append(Code)
            else:
                token.data[index].generateByteCode()
            secondTime += 1

    def generateLeftCodeFirst(self, token):
        secondTime = 0
        for index in range(0, len(token.data)):
            if token.data[index].id == '(identifier)':
                if secondTime == 0:
                    Code = self.loadRegister([self.mapping.getAFreeWorkingRegister(), self.mapping.framePointerRegister, self.variablesInThisAST[token.data[index].data[0]]])
                else:
                    Code = self.loadRegister([self.mapping.getALargestWorkingRegister(), self.mapping.framePointerRegister, self.variablesInThisAST[token.data[index].data[0]]])
                self.byteCodeList.append(Code)
            elif token.data[index].id == '(literal)':
                if secondTime == 0:
                    Code = self.loadValue([self.mapping.getAFreeWorkingRegister(), token.data[index].data[0]])
                else:
                    Code = self.loadValue([self.mapping.getALargestWorkingRegister(), token.data[index].data[0]])
                self.byteCodeList.append(Code)
            else:
                token.data[index].generateByteCode()
            secondTime += 1


    def findOutAndGenerateCorrectSideCode(self, token):
        if token.weight[2] >= token.weight[1]:
            self.generateRightCodeFirst(token)
        else:
            self.generateLeftCodeFirst(token)

    def decideWhetherToSaveSlotForPopValue(self, status, generateByteCode):
        GPR=[]
        firstRegister = self.mapping.releaseALargestWorkingRegister()
        secondRegister = self.mapping.releaseAWorkingRegister()
        if status != 0:
            count = self.mapping.getASmallestFreeRegisterBeforePop(status)
            GPR.insert(0,count)
            GPR.insert(1,secondRegister)
            GPR.insert(2,firstRegister)
            #self.oracle.getALargestWorkingRegister()
        else:
            GPR.insert(0,secondRegister)
            GPR.insert(1,secondRegister)
            GPR.insert(2,firstRegister)
            self.mapping.getAFreeWorkingRegister()

        if generateByteCode == self.assignRegister or generateByteCode == self.compareRegister:
            GPR[0] = secondRegister
            GPR[1] = firstRegister
        Code = generateByteCode(GPR)
        self.byteCodeList.append(Code)

    def initGeneration(self):
        thisGenerator = self

        def recordTheVariable(self,token):
            if token.id in thisGenerator.byteRequired:
                thisGenerator.variableCounter += 1
                thisGenerator.variablesInThisAST[token.data[0].data[0]] = thisGenerator.byteRequired[token.id]
                thisGenerator.memorySize += thisGenerator.byteRequired[token.id]

        respectiveByteCodeFunction = {'=': self.assignRegister, '+': self.addRegister, '==':self.compareRegister, \
                                            '-': self.subRegister, '*': self.multiplyRegister, '/': self.divideRegister, \
                                            '(systemToken)': self.nothing, ';': self.nothing, ',': self.nothing, '}': self.nothing, '{': self.nothing}

        def generateByteCode(self):
            if thisGenerator.isADeclaration(self.id):
                recordTheVariable(None, self)
            else:
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

    def isADeclaration(self, unknownToken):
        if unknownToken in ByteCodeGenerator.byteRequired:
            return True
        else:
            return False

    def injectPrologue(self, oldList):
        if self.memorySize == 0:
            return oldList
        Code = self.subFrameRegister([self.mapping.framePointerRegister,self.memorySize])
        newList = [Code]
        newList.extend(oldList)
        return newList

