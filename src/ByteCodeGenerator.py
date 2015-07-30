__author__ = 'JingWen'

from Mapping import *
from RegisterAllocator import *
from Context import *
from ExpressionContext import *
from FlowControlContext import *
from DeclarationContext import *
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

    def dumpRegister(self, GPR=[]):
        number = 0x00 | GPR[0] << 8
        return number

    def dumpRegisterHex(self, GPR=[]):
        number = 0x01 | GPR[0] << 8
        return number

    def compareIsLessThan(self, GPR=[]):
        number = 0xf2 | GPR[0] << 8 | GPR[1] << 11
        return number

    def compareRegister(self,GPR=[]):
        number = 0xf3 | GPR[0] << 8 | GPR[1] << 11
        return number

    def loadValue(self, GPR=[]):
        number = 0x02 | GPR[0] << 8 | GPR[1] << 11
        return number

    def loadRegister(self, GPR=[]):
        number = 0x04 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 17
        return number

    def storeRegister(self, GPR=[]):
        number = 0x06 | GPR[0] << 8 | GPR[1] << 11
        return number

    def loadMultiple(self, GPR=[]):
        number = 0x08 | GPR[0] << 8 | GPR[1] << 11
        return number

    def storeMultiple(self, GPR=[]):
        number = 0x0a | GPR[0] << 8 | GPR[1] << 11
        return number

    def subFrameRegister(self, GPR=[]):
        number = 0x0c | GPR[0] << 8 | GPR[1] << 11
        return number

    def addRegister(self,GPR =[]):
        number = 0x0d | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def subRegister(self,GPR=[]):
        number = 0x0e | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def multiplyRegister(self, GPR=[]):
        number = 0x0f | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def divideRegister(self,GPR=[]):
        number = 0x10 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def halt(self):
        return 0xffffffff

    def branchIfFalse(self):
        number = 0x11
        return number
        pass

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
                token.data[index].generateByteCode(secondTime)
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
                token.data[index].generateByteCode(secondTime)
            secondTime += 1


    def findOutAndGenerateCorrectSideCode(self, token):
        if token.weight[2] >= token.weight[1]:
            self.generateRightCodeFirst(token)
        else:
            self.generateLeftCodeFirst(token)

    def decideWhetherToSaveSlotForPopValue(self, status, sequence, generateByteCode):
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
            if sequence == 0 or sequence == None:
                GPR.insert(0,secondRegister)
                GPR.insert(1,secondRegister)
                GPR.insert(2,firstRegister)
                self.mapping.getAFreeWorkingRegister()
            else:
                GPR.insert(0,firstRegister)
                GPR.insert(1,secondRegister)
                GPR.insert(2,firstRegister)
                self.mapping.getALargestWorkingRegister()

        if self.isTwoParameters(generateByteCode):
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

        respectiveByteCodeFunction = {'=': self.storeRegister, '+': self.addRegister, '==':self.compareRegister,'<':self.compareIsLessThan, \
                                            '-': self.subRegister, '*': self.multiplyRegister, '/': self.divideRegister, \
                                            '(systemToken)': self.nothing, ';': self.nothing, ',': self.nothing, '}': self.nothing, '{': self.nothing}

        self.twoParamFunctions =[self.storeRegister, self.compareRegister, self.compareIsLessThan]

        def generalByteCode(self, sequenceCheck=None):
            if thisGenerator.isADeclaration(self.id):
                recordTheVariable(None, self)
            else:
                if self.id == '(':
                    self = self.data[0]
                pushed = thisGenerator.registerAllocator.decideWhetherToPush(self)
                thisGenerator.findOutAndGenerateCorrectSideCode(self)

                thisGenerator.decideWhetherToSaveSlotForPopValue(pushed, sequenceCheck, respectiveByteCodeFunction[self.id])

                thisGenerator.registerAllocator.decideWhetherToPop(pushed)
            return thisGenerator.byteCodeList

        def flowControlByteCode(self):

            self.data[0].data[0].generateByteCode()
            label = thisGenerator.mapping.ifLabel()
            thisGenerator.byteCodeList.append(label)
            thisGenerator.byteCodeList.insert(thisGenerator.byteCodeList.__len__()-1,thisGenerator.branchIfFalse())
            thisGenerator.byteCodeList.insert(thisGenerator.byteCodeList.__len__()-1,label)

            return thisGenerator.byteCodeList
        #Start the initialization
        self.byteCodeList = []
        for context in self.contextManager.currentContexts:
            if isinstance(context, ExpressionContext) or isinstance(context,DeclarationContext):
                for token in context.symbolTable:
                    context.symbolTable[token].generateByteCode = generalByteCode
            elif isinstance(context, FlowControlContext):
                for token in context.symbolTable:
                    context.symbolTable[token].generateByteCode = flowControlByteCode

    def isADeclaration(self, unknownToken):
        if unknownToken in ByteCodeGenerator.byteRequired:
            return True
        else:
            return False

    def isTwoParameters(self, unknownFunction):
        return unknownFunction in self.twoParamFunctions

    def injectPrologue(self, oldList):
        self.mapping.reset()
        if self.memorySize == 0:
            return oldList
        newList=[]
        newList.append(self.loadValue([self.mapping.getAFreeWorkingRegister(), self.memorySize]))
        newList.append(self.subRegister([self.mapping.framePointerRegister, self.mapping.framePointerRegister,self.mapping.releaseAWorkingRegister()]))
        newList.extend(oldList)
        return newList

