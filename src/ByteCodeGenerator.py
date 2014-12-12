__author__ = 'JingWen'



class ByteCodeGenerator:
    byteCodeList = []
    registerStatus = [0, 0, 0, 0, 0, 0, 0, 0]   # 1 represent the location of the register is in use
                                                # 0 represent the location is free to be overwrite
    workingRegisterCounter = 0  # Start with the location 0
    MaxRegister = 5  # The maximum available register

    byteRequired = {'int': 4}
    registersInThisAST ={}
    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        pass

    def assignRegisters(self, register1, register2):
        number = 0xfa | register1 << 8 | register2 << 11
        self.byteCodeList.append(number)
        return number


    def subRegister (self, registerNumber, valueToSubtract):
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

    def generateByteCode(self, token):
        if token[0].id == '{':
            token = token[0].data

        self.byteCodeList =[]
        index = 0
        index = self.generateInitializationCode(token, index)

        for value in range(index, len(token[0].data)):
            self.injectLevel(token)
            self.generateProcessCode(token, index)
        return self.byteCodeList

        pass

    #Helper function
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

    def generateProcessCode(self, token, index):

        for number in token[0].data[index].data:
            if number.id == '(identifier)':
                self.loadRegister(self.getAFreeWorkingRegister(), 7, self.registersInThisAST[number.data[0]])
                pass
            elif number.id == '(literal)':
                self.loadValue(self.getAFreeWorkingRegister(), number.data[0])
                pass
        self.assignRegisters(self.releaseAWorkingRegister(), self.releaseAWorkingRegister())

    def generateInitializationCode(self, token, IndexOfTheTree):
        variableCounter =0
        if (len(token)!=0):
            for header in token:
                if header.id in self.byteRequired:
                    variableCounter += 1
            self.subRegister(7, self.byteRequired[token[0].id]*variableCounter)

        variableCounter = 0  # reset and reuse it
        count =0
        for index in range(0, len(token)):
            if token[index].id == 'int':
                variableCounter += 1
                count += 1
                IndexOfTheTree+= 1
            elif token[index].id == '=' and count != 0:
                self.registersInThisAST[token[index].data[0].data[0]] = self.byteRequired[token[0].id]*variableCounter
                self.loadValue(self.getAFreeWorkingRegister(), token[index].data[1].data[0])
                self.storeValue(self.releaseAWorkingRegister(), 7, self.byteRequired[token[0].id]*variableCounter)

                count -= 1
                IndexOfTheTree += 1
            else:
                break
        return IndexOfTheTree


    def getAFreeWorkingRegister(self):
        temp = self.workingRegisterCounter
        if self.workingRegisterCounter < self.MaxRegister:
            self.workingRegisterCounter += 1
        return temp

    def releaseAWorkingRegister(self):
        if self.workingRegisterCounter > 0:
            self.workingRegisterCounter -= 1
        return self.workingRegisterCounter




"""
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
