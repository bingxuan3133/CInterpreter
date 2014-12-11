__author__ = 'JingWen'



class ByteCodeGenerator:
    byteCodeList = []
    registerStatus = [0, 0, 0, 0, 0, 0, 0, 0]   # 1 represent the location of the register is in use
                                                # 0 represent the location is free to be overwrite
    workingRegisterCounter = 0  # Start with the location 0
    MaxRegister = 5  # The maximum available register

    byteRequired = {'int': 4}
    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        pass


    def subRegister (self, registerNumber, valueToSubtract):
        number = 0xfb | registerNumber << 8 | valueToSubtract << 11
        self.byteCodeList.append(number)
        return number

    def loadValue(self, registerNumber, valueToAssign):
        number = 0xf8 | registerNumber << 8 | valueToAssign << 11
        self.byteCodeList.append(number)
        return number

    def storeValue(self, targetRegister, framePointer, relativeAddress):
        number = 0xfe | targetRegister << 8 | framePointer << 11 | relativeAddress << 14
        self.byteCodeList.append(number)
        return number

    def loadRegister(self, targetRegisterNumber, registerNumber, relativeAddress):
        number = 0xff | targetRegisterNumber << 8 | registerNumber << 11 | relativeAddress << 17
        self.byteCodeList.append(number)
        return number

    def generateByteCode(self, token):
        self.byteCodeList =[]
        index = 0
        index = self.generateInitializationCode(token, index)

        #for value in range(index, len(token)):
        #   self.generateProcessCode(token, index)
        return self.byteCodeList

        pass

    #Helper function
    #def generateProcessCode(self, token, index):
     #   if token[index].id == '':
      #  pass
    def generateInitializationCode(self, token, IndexOfTheTree):
        variableCounter =0
        if token[0].id == '{':
            token = token[0].data
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
                self.loadValue(self.getAFreeWorkingRegister(), \
                            token[index].data[1].data[0])
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
