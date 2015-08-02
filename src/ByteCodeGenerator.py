__author__ = 'JingWen'

from Mapping import *
from RegisterAllocator import *
from Context import *
from ExpressionContext import *
from FlowControlContext import *
from DeclarationContext import *
from DeclarationContext import *
from DefaultContext import *
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
        self.lastUseInstruction =None
        self.contextManager.addContext('Base', self.context)


    def nothing(self):
        pass

    def dumpRegister(self, GPR=[]):
        number = 0x00 | GPR[0] << 8
        return number

    def dumpRegisterHex(self, GPR=[]):
        number = 0x01 | GPR[0] << 8
        return number

    def compareIsLessThan(self, GPR=[]):
        number = 0xf2 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareRegister(self,GPR=[]):
        number = 0xf3 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareIsLessThanOrEqual(self,GPR=[]):
        number = 0xf4 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareIsGreaterThan(self, GPR=[]):
        number = 0xf5 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareIsGreaterThanOrEqual(self, GPR=[]):
        number = 0xf6 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
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

    def orRegister(self, GPR =[]):
        number = 0x11 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def modulusRegister(self,GPR=[]):
        number = 0x12 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def branchIfTrue(self, GPR = []):
        #GPR[0] == The number that needed to be branch
        #GPR[1] == The register number that refers to
        number = 0x14 | GPR[0] << 8 | GPR[1] << 11
        return number

    def branch(self, GPR =[]):
        number = 0x15 | GPR[0] << 8
        return number

    def halt(self):
        return 0xffffffff

    def generateRightCodeFirst(self, token):
        secondTime = 0
        for index in range(len(token.data)-1, -1, -1):
            token.data[index].generateByteCode(secondTime,token,index)
            secondTime += 1

    def generateLeftCodeFirst(self, token):
        secondTime = 0
        for index in range(0, len(token.data)):
            token.data[index].generateByteCode(secondTime,token,index)
            secondTime += 1


    def findOutAndGenerateCorrectSideCode(self, token):
        if token.weight[2] > token.weight[1]:
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
            if self.lastUseInstruction == self.loadRegister:
                GPR[0] = secondRegister
                GPR[1] = firstRegister
            else:
                GPR[0] = firstRegister
                GPR[1] = secondRegister
        Code = generateByteCode(GPR)
        self.byteCodeList.append(Code)

    def initGeneration(self):
        thisGenerator = self

        def recordTheVariable(self,token):
            if token.id in thisGenerator.byteRequired:
                thisGenerator.variableCounter += 1
                thisGenerator.memorySize += thisGenerator.byteRequired[token.id]
                thisGenerator.variablesInThisAST[token.data[0].data[0]] = thisGenerator.memorySize

        def noByteCode(self,sequenceCheck = None, token = None, index = -1):
            if self.id == "(":
                self.data[0].generateByteCode(sequenceCheck)

        def generateLiteralCode(self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadValue
            if sequenceCheck == 0:
                Code = thisGenerator.loadValue([thisGenerator.mapping.getAFreeWorkingRegister(), token.data[index].data[0]])
            else:
                Code = thisGenerator.loadValue([thisGenerator.mapping.getALargestWorkingRegister(), token.data[index].data[0]])
            thisGenerator.byteCodeList.append(Code)
        def generateIdentifierCode(self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadRegister
            if sequenceCheck == 0:
                Code = thisGenerator.loadRegister([thisGenerator.mapping.getAFreeWorkingRegister(), thisGenerator.mapping.framePointerRegister, thisGenerator.variablesInThisAST[token.data[index].data[0]]])
            else:
                Code = thisGenerator.loadRegister([thisGenerator.mapping.getALargestWorkingRegister(), thisGenerator.mapping.framePointerRegister, thisGenerator.variablesInThisAST[token.data[index].data[0]]])
            thisGenerator.byteCodeList.append(Code)

        def generalByteCode(self,sequenceCheck = None, token = None, index = -1):
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

        def ifByteCode(self,sequenceCheck = None, token = None, index = -1):
            self.data[0].data[0].generateByteCode()
            thisGenerator.byteCodeList.append(thisGenerator.branchIfTrue([1,thisGenerator.mapping.releaseAWorkingRegister()]))
            thisGenerator.mapping.reset()
            tempLocation = thisGenerator.byteCodeList.__len__()
            for statement in self.data[1][0].data:
                statement.generateByteCode()
                thisGenerator.mapping.reset()
            thisGenerator.byteCodeList.insert(tempLocation, thisGenerator.branch([thisGenerator.byteCodeList.__len__()-tempLocation]))
            if self.data.__len__() == 3:
                for statement in self.data[2].data[0][0].data:
                    statement.generateByteCode()
                    thisGenerator.mapping.reset()
            return thisGenerator.byteCodeList

        def whileByteCode(self,sequenceCheck = None, token = None, index = -1):
            self.data[0].generateByteCode()
            thisGenerator.byteCodeList.append(thisGenerator.branchIfTrue([1,thisGenerator.mapping.releaseAWorkingRegister()]))
            thisGenerator.mapping.reset()
            tempLocation = thisGenerator.byteCodeList.__len__()
            for statement in self.data[1][0].data:
                statement.generateByteCode()
                thisGenerator.mapping.reset()
            branchSize = thisGenerator.byteCodeList.__len__()-tempLocation
            if branchSize != 0:
                branchSize += 1
            thisGenerator.byteCodeList.insert(tempLocation, thisGenerator.branch([branchSize]))
            thisGenerator.byteCodeList.append(thisGenerator.branch([-branchSize]))
            return thisGenerator.byteCodeList

        def doByteCode(self,sequenceCheck = None, token = None, index = -1):
            tempLocation = thisGenerator.byteCodeList.__len__()
            for statement in self.data[1][0].data:
                statement.generateByteCode()
                thisGenerator.mapping.reset()
            self.data[0].generateByteCode()
            thisGenerator.byteCodeList.append(thisGenerator.branchIfTrue([1,thisGenerator.mapping.releaseAWorkingRegister()]))
            branchSize = thisGenerator.byteCodeList.__len__()-tempLocation+1
            thisGenerator.byteCodeList.append(thisGenerator.branch([-branchSize]))

            return thisGenerator.byteCodeList

        generationFunction = { '(literal)':([None], [generateLiteralCode]), '(identifier)':([None], [generateIdentifierCode]), '(systemToken)':([None], [noByteCode]),'(floating)':([None], [noByteCode]),
                            '+':([None],[generalByteCode]),'-':([None],[generalByteCode],), '*':([None],[generalByteCode]), '/':([None],[generalByteCode]),'==':([None],[generalByteCode]),'|':([None],[generalByteCode]),'%':([None],[generalByteCode]),
                            '=':([None],[generalByteCode]),'<':([None],[generalByteCode]),'<=':([None],[generalByteCode]),'>':([None],[generalByteCode]),'>=':([None],[generalByteCode]),'&&':([None],[generalByteCode]),
                            'int':([None],[generalByteCode]),'long':([None],[generalByteCode]), 'short':([None],[generalByteCode]),
                             'if':([None],[ifByteCode]),'while':([None],[whileByteCode]),'do':([None],[doByteCode]),'else':([None],[noByteCode]),
                             ',':([None],[noByteCode]),'(declaration&definition)':([None],[noByteCode]),
                              'unsigned':([None],[noByteCode]),'signed':([None],[noByteCode]),
                              '(':([None],[noByteCode]),';':([None],[noByteCode]),')':([None],[noByteCode]),'{':([None],[noByteCode]),'}':([None],[noByteCode]),
                              }

        respectiveByteCodeFunction = {
                                    '=': self.storeRegister, '+': self.addRegister,'-': self.subRegister, '*': self.multiplyRegister, '/': self.divideRegister,'|': self.orRegister,'%':self.modulusRegister,
                                    '==':self.compareRegister,'<':self.compareIsLessThan,'<=':self.compareIsLessThanOrEqual,'>':self.compareIsGreaterThan,'>=':self.compareIsGreaterThanOrEqual,
                                    '&&':self.orRegister,
                                    '(systemToken)': self.nothing, ';': self.nothing, ',': self.nothing, '}': self.nothing, '{': self.nothing}


        self.twoParamFunctions =[self.storeRegister]

        #Start the initialization
        self.byteCodeList = []
        for context in self.contextManager.allContexts:
            for token in context.symbolTable:
                context.symbolTable[token].generateByteCode = generationFunction[token][1][0]


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

