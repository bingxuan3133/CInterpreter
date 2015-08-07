__author__ = 'JingWen'

from Mapping import *
from RegisterAllocator import *
from Context import *
from ExpressionContext import *
from FlowControlContext import *
from DeclarationContext import *
from DeclarationContext import *
from DefaultContext import *
import struct

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
        self.floatingFlag = 0



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

    def loadFloatingPoint(self,GPR = []):
        number = 0x15 | GPR[0] << 8 | GPR[1] << 16
        return number

    def addFloatingRegister(self, GPR = []):
        #GPR[0] and GPR[1] => the destination registers to store the answer
        #GPR[2] and GPR[3] => the registers that stored the register number
        #GPR[4] and GPR[5] => the registers that stored the register number
        number = 0x15 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14 | GPR[3] << 17 | GPR[4] << 20 | GPR[5] << 23
        return number

    def storeFloatingPointRegister(self, GPR =[]):
        number = 0x15 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14 | GPR[3] << 17
        return number

    def loadFloatingPointRegister(self, GPR = []):
        number = 0x15 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14 | GPR[3] << 17
        return number

    def halt(self):
        return 0xffffffff

    def generateRightCodeFirst(self, token,generateByteCode):
        secondTime = 0
        for index in range(len(token.data)-1, -1, -1):
            token.data[index].generateByteCode(secondTime,token,index)
            secondTime += 1

    def generateLeftCodeFirst(self, token,generateByteCode):
        secondTime = 0
        for index in range(0, len(token.data)):

            token.data[index].generateByteCode(secondTime,token,index)
            secondTime += 1

    def findOutAndGenerateCorrectSideCode(self, token, generateByteCode):
        if token.weight[2] > token.weight[1]:
            self.generateRightCodeFirst(token,generateByteCode)
        else:
            self.generateLeftCodeFirst(token,generateByteCode)

    def decideWhetherToSaveSlotForPopValue(self, status, sequence, generateByteCode, token):
        if self.floatingFlag == 1:
            self.floatingPointRegisterSaving(status, sequence, self.relativeFunction[generateByteCode])
        else:
            self.literalRegisterSaving( status, sequence, generateByteCode)

    def floatingPointRegisterSaving(self, status, sequence, generateByteCode):
        GPR = []
        secondRegister = self.mapping.releaseAWorkingRegister()
        firstRegister = self.mapping.releaseAWorkingRegister()
        thirdRegister = self.mapping.releaseALargestWorkingRegister()
        fourthRegister = self.mapping.releaseALargestWorkingRegister()
        GPR.insert(0,self.mapping.getAFreeWorkingRegister())
        GPR.insert(1, self.mapping.getAFreeWorkingRegister())
        GPR.insert(2, firstRegister)
        GPR.insert(3, secondRegister)
        GPR.insert(4, fourthRegister)
        GPR.insert(5, thirdRegister)

        if self.isStoreFunction(generateByteCode):
            GPR[0]= firstRegister
            GPR[1] =secondRegister
            GPR[2] = fourthRegister
            GPR[3]= thirdRegister
            pass
        Code = generateByteCode(GPR)
        self.byteCodeList.append(Code)

    def literalRegisterSaving(self, status, sequence, generateByteCode):
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

        if self.isStoreFunction(generateByteCode):
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
        thisGenerator.byteCodeList =[]
        def recordTheVariable(self,token):
            if token.data[0].id in thisGenerator.byteRequired:
                thisGenerator.variableCounter += 1
                thisGenerator.memorySize += thisGenerator.byteRequired[token.data[0].id]
                thisGenerator.variablesInThisAST[token.data[1].data[0]] = thisGenerator.memorySize

        def noByteCode(self,sequenceCheck = None, token = None, index = -1):
            if self.id == "(":
                self.data[0].generateByteCode(sequenceCheck)

        def generateLiteralCode(self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadValue
            if sequenceCheck == 0:
                destinationRegister = thisGenerator.mapping.getAFreeWorkingRegister()
            else:
                destinationRegister = thisGenerator.mapping.getALargestWorkingRegister()
            Code = thisGenerator.loadValue([destinationRegister, token.data[index].data[0]])
            thisGenerator.byteCodeList.append(Code)

        def generateFloatingPointLoad (self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadFloatingPoint
            floatPack = struct.pack('!f', token.data[index].data[0])
            if sequenceCheck == 0:
                destinationRegister1 = thisGenerator.mapping.getAFreeWorkingRegister()
                destinationRegister2 = thisGenerator.mapping.getAFreeWorkingRegister()
            else:
                destinationRegister1 = thisGenerator.mapping.getALargestWorkingRegister()
                destinationRegister2 = thisGenerator.mapping.getALargestWorkingRegister()
            Code = thisGenerator.loadFloatingPoint([destinationRegister1,floatPack[0],floatPack[1] ])
            thisGenerator.byteCodeList.append(Code)
            Code = thisGenerator.loadFloatingPoint([destinationRegister2,floatPack[2],floatPack[3] ])
            thisGenerator.byteCodeList.append(Code)
            thisGenerator.floatingFlag = 1

        def generateIdentifierCode(self,sequenceCheck = None, token = None, index = -1):
            if thisGenerator.floatingFlag == 1:
                generateFloatingPointIdentifierCode(self, sequenceCheck, token, index)
            else:
                generateLiteralIdentifierLoad(self, sequenceCheck, token, index)

        def generateLiteralIdentifierLoad(self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadRegister
            if sequenceCheck == 0:
                destinationRegister = thisGenerator.mapping.getAFreeWorkingRegister()
            else:
                destinationRegister = thisGenerator.mapping.getALargestWorkingRegister()
            Code = thisGenerator.loadRegister([destinationRegister, thisGenerator.mapping.framePointerRegister, thisGenerator.variablesInThisAST[token.data[index].data[0]]])
            thisGenerator.byteCodeList.append(Code)

        def generateFloatingPointIdentifierCode(self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadFloatingPointRegister
            if sequenceCheck == 0:
                destinationRegister1 = thisGenerator.mapping.getAFreeWorkingRegister()
                destinationRegister2 = thisGenerator.mapping.getAFreeWorkingRegister()
            else:
                destinationRegister1 = thisGenerator.mapping.getALargestWorkingRegister()
                destinationRegister2 = thisGenerator.mapping.getALargestWorkingRegister()
            Code = thisGenerator.loadFloatingPointRegister([destinationRegister2,destinationRegister1,
                                                            thisGenerator.mapping.framePointerRegister,int(thisGenerator.variablesInThisAST[token.data[index].data[0]]/2),
                                                            thisGenerator.mapping.framePointerRegister,thisGenerator.variablesInThisAST[token.data[index].data[0]]
                                                            ] )
            thisGenerator.byteCodeList.append(Code)
            thisGenerator.floatingFlag = 1

        def generalByteCode(self,sequenceCheck = None, token = None, index = -1):
            if self.id == '(':
                self = self.data[0]
            pushed = thisGenerator.registerAllocator.decideWhetherToPush(self)
            thisGenerator.findOutAndGenerateCorrectSideCode(self, respectiveByteCodeFunction[self.id])

            thisGenerator.decideWhetherToSaveSlotForPopValue(pushed, sequenceCheck, respectiveByteCodeFunction[self.id], token)

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

        def defByteCode(self,sequenceCheck = None, token = None, index = -1):
            recordTheVariable(None, self.data[0])
            sequenceCheck = 0
            self.data[0].data[1].generateByteCode(sequenceCheck, self.data[0], index = 1)
            sequenceCheck = 1
            self.data[1].generateByteCode(sequenceCheck, self, index = 1)
            Code = thisGenerator.storeRegister([thisGenerator.mapping.releaseALargestWorkingRegister(),thisGenerator.mapping.releaseAWorkingRegister()])
            thisGenerator.byteCodeList.append(Code)

            return thisGenerator.byteCodeList

        def declByteCode(self,sequenceCheck = None, token = None, index = -1):
            recordTheVariable(None, self)
            return thisGenerator.byteCodeList
        generationFunction = { '(literal)':([None], [generateLiteralCode]), '(identifier)':([None], [generateIdentifierCode]), '(systemToken)':([None], [noByteCode]),'(floating)':([None], [generateFloatingPointLoad]),
                            '+':([None],[generalByteCode]),'-':([None],[generalByteCode],), '*':([None],[generalByteCode]), '/':([None],[generalByteCode]),'==':([None],[generalByteCode]),'|':([None],[generalByteCode]),'%':([None],[generalByteCode]),
                            '=':([None],[generalByteCode]),'<':([None],[generalByteCode]),'<=':([None],[generalByteCode]),'>':([None],[generalByteCode]),'>=':([None],[generalByteCode]),'&&':([None],[generalByteCode]),
                            'int':([None],[generalByteCode]),'long':([None],[generalByteCode]), 'short':([None],[generalByteCode]),
                               '(def)':([None],[defByteCode]),'(decl)':([None],[declByteCode]),
                             'if':([None],[ifByteCode]),'while':([None],[whileByteCode]),'do':([None],[doByteCode]),'else':([None],[noByteCode]),
                             ',':([None],[noByteCode]),'(multiple)':([None],[noByteCode]),
                              'unsigned':([None],[noByteCode]),'signed':([None],[noByteCode]),
                              '(':([None],[noByteCode]),';':([None],[noByteCode]),')':([None],[noByteCode]),'{':([None],[noByteCode]),'}':([None],[noByteCode]),
                              }

        respectiveByteCodeFunction = {
                                    '=': self.storeRegister, '+': self.addRegister,'-': self.subRegister, '*': self.multiplyRegister, '/': self.divideRegister,'|': self.orRegister,'%':self.modulusRegister,
                                    '==':self.compareRegister,'<':self.compareIsLessThan,'<=':self.compareIsLessThanOrEqual,'>':self.compareIsGreaterThan,'>=':self.compareIsGreaterThanOrEqual,
                                    '&&':self.orRegister,
                                    '(systemToken)': self.nothing, ';': self.nothing, ',': self.nothing, '}': self.nothing, '{': self.nothing}

        self.relativeFunction = {
                            self.addRegister:self.addFloatingRegister,self.storeRegister:self.storeFloatingPointRegister,
                            self.loadRegister:self.loadFloatingPointRegister
                            }

        self.storeFunction =[self.storeRegister, self.storeFloatingPointRegister]

        #Start the initialization
        for context in self.contextManager.allContexts:
            for token in context.symbolTable:
                context.symbolTable[token].generateByteCode = generationFunction[token][1][0]


    def isADeclaration(self, unknownToken):
        if unknownToken in ByteCodeGenerator.byteRequired:
            return True
        else:
            return False

    def isStoreFunction(self, unknownFunction):
        return unknownFunction in self.storeFunction


    def injectPrologue(self, oldList):
        self.mapping.reset()
        if self.memorySize == 0:
            return oldList
        newList=[]
        newList.append(self.loadValue([self.mapping.getAFreeWorkingRegister(), self.memorySize]))
        newList.append(self.subRegister([self.mapping.framePointerRegister, self.mapping.framePointerRegister,self.mapping.releaseAWorkingRegister()]))
        newList.extend(oldList)
        return newList

