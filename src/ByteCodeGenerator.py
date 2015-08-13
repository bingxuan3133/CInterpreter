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
    byteRequired = {'char': 1, 'short': 2, 'int': 4, 'long': 4, 'float': 4, 'double': 8}
    variablesInThisAST = {}
    variableStack = []
    variableCounter = 0
    memorySize = 0
    verboseByteCode = False  # inject the C statement into the bytecodes list if True



    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        self.mapping = Mapping()
        self.registerAllocator = RegisterAllocator(self)
        self.lastUseInstruction =None
        self.contextManager.addContext('Base', self.context)
        self.floatingFlag = 0
        self.side = ""



    def nothing(self):
        pass

    def dumpRegister(self, GPR=[]):
        number = 0x00 | GPR[0] << 8
        return number

    def dumpRegisterHex(self, GPR=[]):
        number = 0x01 | GPR[0] << 8
        return number

    def loadValue(self, GPR=[]):
        number = 0x02 | GPR[0] << 8 | GPR[1] << 11
        return number

    def loadRegister(self, GPR=[]):
        number = 0x05 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def storeRegister(self, GPR=[]):
        number = 0x07 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def loadMultiple(self, GPR=[]):
        number = 0x08 | GPR[0] << 8 | GPR[1] << 11
        return number

    def storeMultiple(self, GPR=[]):
        number = 0x0a | GPR[0] << 8 | GPR[1] << 11
        return number

    def addRegister(self,GPR =[]):
        number = 0x0c | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def subRegister(self,GPR=[]):
        number = 0x0d | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def multiplyRegister(self, GPR=[]):
        number = 0x0e | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def divideRegister(self,GPR=[]):
        number = 0x0f | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def orRegister(self, GPR =[]):
        number = 0x11 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def modulusRegister(self,GPR=[]):
        number = 0x12 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def loadFloatingPoint(self,GPR = []):
        number = 0x13 | GPR[0] << 8
        return number

    def immediateFloatingPoint(self, GPR=[]):
        number = GPR[0] | GPR[1] << 8 | GPR[2] << 16 | GPR[3] << 24
        return number

    def loadFloatingPointRegister(self, GPR = []):
        number = 0x14 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def storeFloatingPointRegister(self, GPR =[]):
        number = 0x15 | GPR[0] << 8 | GPR[1] << 11
        return number

    def addFloatingRegister(self, GPR = []):
        number = 0x16 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def branch(self, GPR =[]):
        number = 0x1a | GPR[0] << 8
        return number

    def branchIfTrue(self, GPR = []):
        #GPR[0] == The number that needed to be branch
        #GPR[1] == The register number that refers to
        number = 0x1b | GPR[0] << 8 | GPR[1] << 11
        return number

    def compareIfEqual(self,GPR=[]):
        number = 0x1c | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareIfLesserThan(self, GPR=[]):
        number = 0x1d | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareIfLesserThanOrEqual(self,GPR=[]):
        number = 0x1e | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareIfGreaterThan(self, GPR=[]):
        number = 0x1f | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def compareIfGreaterThanOrEqual(self, GPR=[]):
        number = 0x20 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        return number

    def halt(self):
        return 0xff

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
            return "RIGHT"
        else:
            self.generateLeftCodeFirst(token,generateByteCode)
            return "LEFT"

    def decideWhetherToSaveSlotForPopValue(self, status, sequence, generateByteCode, token):
        if self.floatingFlag == 1:
            generateByteCode=self.relativeFunction[generateByteCode]
        GPR=[]
        firstRegister = self.mapping.releaseALargestWorkingRegister()
        secondRegister = self.mapping.releaseAWorkingRegister()
        if self.isStoreFunction(generateByteCode):
            if self.lastUseInstruction == self.loadRegister:
                GPR = [secondRegister,self.mapping.framePointerRegister,self.variableStack.pop()]
            else:
                GPR = [firstRegister,self.mapping.framePointerRegister,self.variableStack.pop()]
            Code = generateByteCode(GPR)
            self.byteCodeList.append(Code)
            #self.byteCodeList.insert(self.byteCodeList.__len__(),Code)
            return
        else:
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
                if self.side == "RIGHT":
                    temp = GPR[1]
                    GPR[1] =GPR[2]
                    GPR[2] = temp
        Code = generateByteCode(GPR)
        self.byteCodeList.append(Code)

    def initGeneration(self):
        thisGenerator = self
        thisGenerator.byteCodeList =[]
        def recordTheVariable(self,token):
            if thisGenerator.verboseByteCode:
                thisGenerator.byteCodeList.append(token.data[1].oriString)
            if token.data[0].id in thisGenerator.byteRequired:
                thisGenerator.variableCounter += 1
                for member in thisGenerator.variablesInThisAST:
                    thisGenerator.variablesInThisAST[member] += thisGenerator.byteRequired[token.data[0].id]
                thisGenerator.variablesInThisAST[token.data[1].data[0]] = thisGenerator.memorySize
                thisGenerator.memorySize += thisGenerator.byteRequired[token.data[0].id]


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
            #thisGenerator.appendByteCode(Code)

        def generateFloatingPointLoad (self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadFloatingPoint
            floatPack = struct.pack('!d', token.data[index].data[0])
            if sequenceCheck == 0:
                destinationRegister1 = thisGenerator.mapping.getAFreeWorkingRegister()
            else:
                destinationRegister1 = thisGenerator.mapping.getALargestWorkingRegister()
            Code = thisGenerator.loadFloatingPoint([destinationRegister1])
            thisGenerator.byteCodeList.append(Code)
            Code = thisGenerator.immediateFloatingPoint([floatPack[0],floatPack[1],floatPack[2],floatPack[3]])
            thisGenerator.byteCodeList.append(Code)
            Code = thisGenerator.immediateFloatingPoint([floatPack[4],floatPack[5],floatPack[6],floatPack[7]])
            thisGenerator.byteCodeList.append(Code)

            thisGenerator.floatingFlag = 1

        def generateIdentifierCode(self,sequenceCheck = None, token = None, index = -1):
            thisGenerator.lastUseInstruction = thisGenerator.loadRegister
            if sequenceCheck == 0:
                destinationRegister = thisGenerator.mapping.getAFreeWorkingRegister()
            else:
                destinationRegister = thisGenerator.mapping.getALargestWorkingRegister()
            try:
                if thisGenerator.floatingFlag ==1:
                    Code = thisGenerator.loadFloatingPointRegister([destinationRegister, thisGenerator.mapping.framePointerRegister, thisGenerator.variablesInThisAST[token.data[index].data[0]]])
                else:
                    Code = thisGenerator.loadRegister([destinationRegister, thisGenerator.mapping.framePointerRegister, thisGenerator.variablesInThisAST[token.data[index].data[0]]])
                thisGenerator.variableStack.append(thisGenerator.variablesInThisAST[token.data[index].data[0]])
            except KeyError as e:
                raise SyntaxError(Error.generateErrorMessageWithOneArguement("Variable {} is not declared!",token.data[index],e.args[0]))
            thisGenerator.byteCodeList.append(Code)



        def generalByteCode(self,sequenceCheck = None, token = None, index = -1):
            if self.id == '(':
                self = self.data[0]
            pushed = thisGenerator.registerAllocator.decideWhetherToPush(self)
            side = thisGenerator.findOutAndGenerateCorrectSideCode(self, respectiveByteCodeFunction[self.id])
            thisGenerator.side = side

            thisGenerator.decideWhetherToSaveSlotForPopValue(pushed, sequenceCheck, respectiveByteCodeFunction[self.id], token)

            thisGenerator.registerAllocator.decideWhetherToPop(pushed)
            return thisGenerator.byteCodeList

        def ifByteCode(self,sequenceCheck = None, token = None, index = -1):
            self.data[0].data[0].generateByteCode()
            thisGenerator.byteCodeList.append(thisGenerator.branchIfTrue([thisGenerator.mapping.releaseAWorkingRegister(),1]))
            thisGenerator.mapping.reset()
            tempLocation = thisGenerator.byteCodeList.__len__()
            for statement in self.data[1][0].data:
                if isinstance(statement,list):
                    statement = statement[0]
                statement.generateByteCode()
                thisGenerator.mapping.reset()
            thisGenerator.byteCodeList.insert(tempLocation, thisGenerator.branch([thisGenerator.byteCodeList.__len__()-tempLocation]))
            if self.data.__len__() == 3:
                for statement in self.data[2].data[0][0].data:
                    tempLocation = thisGenerator.byteCodeList.__len__()
                    statement.generateByteCode()
                    thisGenerator.mapping.reset()
                    thisGenerator.byteCodeList.insert(tempLocation, thisGenerator.branch([thisGenerator.byteCodeList.__len__()-tempLocation]))
            return thisGenerator.byteCodeList

        def whileByteCode(self,sequenceCheck = None, token = None, index = -1):
            if thisGenerator.verboseByteCode:
                thisGenerator.byteCodeList.append(self.data[0].oriString.strip())
            self.data[0].generateByteCode()
            thisGenerator.byteCodeList.append(thisGenerator.branchIfTrue([thisGenerator.mapping.releaseAWorkingRegister(),1]))
            thisGenerator.mapping.reset()
            tempLocation = thisGenerator.byteCodeList.__len__()
            for statement in self.data[1][0].data:
                if thisGenerator.verboseByteCode:
                    thisGenerator.byteCodeList.append(statement.oriString.strip())
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
            thisGenerator.byteCodeList.append(thisGenerator.branchIfTrue([thisGenerator.mapping.releaseAWorkingRegister(),1]))
            branchSize = thisGenerator.byteCodeList.__len__()-tempLocation+1
            thisGenerator.byteCodeList.append(thisGenerator.branch([-branchSize]))
            return thisGenerator.byteCodeList

        def multipleByteCode(self,sequenceCheck = None, token = None, index = -1):
            for token in self.data:
                token.generateByteCode(sequenceCheck, self.data[0], index = 1)
            return thisGenerator.byteCodeList

        def incrementByteCode(self,sequenceCheck = None, token = None, index = -1):
            stackpointer = thisGenerator.mapping.framePointerRegister
            relativeAddress = thisGenerator.variablesInThisAST[self.data[0].data[0]]
            GPR = [thisGenerator.mapping.getAFreeWorkingRegister(), stackpointer, relativeAddress]
            Code = thisGenerator.loadRegister(GPR)
            thisGenerator.byteCodeList.append(Code)
            Code = thisGenerator.loadValue([thisGenerator.mapping.getALargestWorkingRegister(), 1])
            thisGenerator.byteCodeList.append(Code)
            destinationRegister = thisGenerator.mapping.releaseAWorkingRegister()
            source1 = destinationRegister
            source2 = thisGenerator.mapping.releaseALargestWorkingRegister()
            GPR = [destinationRegister,source1,source2]
            Code = thisGenerator.addRegister(GPR)
            thisGenerator.byteCodeList.append(Code)
            Code = thisGenerator.storeRegister([thisGenerator.mapping.getAFreeWorkingRegister(),stackpointer,relativeAddress])
            thisGenerator.byteCodeList.append(Code)
            return thisGenerator.byteCodeList

        def decrementByteCode(self,sequenceCheck = None, token = None, index = -1):
            stackpointer = thisGenerator.mapping.framePointerRegister
            relativeAddress = thisGenerator.variablesInThisAST[self.data[0].data[0]]
            GPR = [thisGenerator.mapping.getAFreeWorkingRegister(), stackpointer, relativeAddress]
            Code = thisGenerator.loadRegister(GPR)
            thisGenerator.byteCodeList.append(Code)
            Code = thisGenerator.loadValue([thisGenerator.mapping.getALargestWorkingRegister(), 1])
            thisGenerator.byteCodeList.append(Code)
            destinationRegister = thisGenerator.mapping.releaseAWorkingRegister()
            source1 = destinationRegister
            source2 = thisGenerator.mapping.releaseALargestWorkingRegister()
            GPR = [destinationRegister,source1,source2]
            Code = thisGenerator.subRegister(GPR)
            thisGenerator.byteCodeList.append(Code)
            Code = thisGenerator.storeRegister([thisGenerator.mapping.getAFreeWorkingRegister(),stackpointer,relativeAddress])
            thisGenerator.byteCodeList.append(Code)
            return thisGenerator.byteCodeList

        def defByteCode(self,sequenceCheck = None, token = None, index = -1):
            recordTheVariable(None, self.data[0])
            sequenceCheck = 0
            self.data[0].data[1].generateByteCode(sequenceCheck, self.data[0], index = 1)
            sequenceCheck = 1
            self.data[1].generateByteCode(sequenceCheck, self, index = 1)
            firstRegister = thisGenerator.mapping.releaseAWorkingRegister()
            secondRegister = thisGenerator.mapping.releaseALargestWorkingRegister()
            if thisGenerator.lastUseInstruction == thisGenerator.loadRegister:
                GPR = [firstRegister,thisGenerator.mapping.framePointerRegister,thisGenerator.variableStack.pop()]
            else:
                GPR = [secondRegister,thisGenerator.mapping.framePointerRegister,thisGenerator.variableStack.pop()]
            Code = thisGenerator.storeRegister(GPR)
            thisGenerator.byteCodeList.append(Code)

            return thisGenerator.byteCodeList

        def declByteCode(self,sequenceCheck = None, token = None, index = -1):
            recordTheVariable(None, self)
            return thisGenerator.byteCodeList
        generationFunction = {  '(literal)':([None], [generateLiteralCode]),
                                '(identifier)':([None], [generateIdentifierCode]),
                                'EOF':([None], [noByteCode]),
                                '(floating)':([None], [generateFloatingPointLoad]),
                                '+':([None],[generalByteCode]),
                                '-':([None],[generalByteCode]),
                                '*':([None],[generalByteCode]),
                                '/':([None],[generalByteCode]),
                                '==':([None],[generalByteCode]),
                                '|':([None],[generalByteCode]),
                                '%':([None],[generalByteCode]),
                                '=':([None],[generalByteCode]),
                                '!=':([None],[generalByteCode]),
                                '<':([None],[generalByteCode]),
                                '<=':([None],[generalByteCode]),
                                '>':([None],[generalByteCode]),
                                '>=':([None],[generalByteCode]),
                                '&&':([None],[generalByteCode]),
                                'int':([None],[generalByteCode]),
                                'long':([None],[generalByteCode]),
                                'short':([None],[generalByteCode]),
                                'char':([None],[generalByteCode]),
                                'double':([None],[generalByteCode]),
                                'float':([None],[generalByteCode]),
                                '(def)':([None],[defByteCode]),
                                '(decl)':([None],[declByteCode]),
                                'if':([None],[ifByteCode]),
                                'while':([None],[whileByteCode]),
                                'do':([None],[doByteCode]),
                                'else':([None],[noByteCode]),
                                ',':([None],[noByteCode]),
                                '(multiple)':([None],[multipleByteCode]),
                                '--':([None],[decrementByteCode]),
                                '++':([None],[incrementByteCode]),
                                '||':([None],[noByteCode]),
                                '&':([None],[noByteCode]),
                                'unsigned':([None],[noByteCode]),
                                'signed':([None],[noByteCode]),
                                '(':([None],[noByteCode]),
                                ';':([None],[noByteCode]),
                                ')':([None],[noByteCode]),
                                '{':([None],[noByteCode]),
                                '}':([None],[noByteCode]),
                                ']':([None],[noByteCode]),
                                '[':([None],[noByteCode]),
                            }

        respectiveByteCodeFunction = {
                                    '=': self.storeRegister, '+': self.addRegister,'-': self.subRegister, '*': self.multiplyRegister, '/': self.divideRegister,'|': self.orRegister,'%':self.modulusRegister,
                                    '==':self.compareIfEqual,'<':self.compareIfLesserThan,'<=':self.compareIfLesserThanOrEqual,'>':self.compareIfGreaterThan,'>=':self.compareIfGreaterThanOrEqual,
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
        self.memorySize = 0
        return newList

    def appendByteCode(self, ):
        pass
