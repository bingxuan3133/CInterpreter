__author__ = 'JingWen'



class ByteCodeGenerator:
    byteCodeList = []
    registerStatus = [0, 0, 0, 0, 0, 0, 0, 0]   # 1 represent the location of the register is in use
                                                # 0 represent the location is free to be overwrite
    workingRegisterCounter = 0  # Start with the location 0, should not exceed 7

    byteRequired = {'int': 4}
    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        pass


    def subRegister (self, registerNumber, valueToSubtract):
        number = 0xfb | registerNumber << 8 | valueToSubtract << 11
        #return format(number, '08x')
        return number

    def loadValue(self, registerNumber, relativeAddress, valueToAssign):
        number = 0xf8 |registerNumber<<8 |relativeAddress<<12 |valueToAssign<<17
        return number

    def generateByteCode(self, token):
        self.byteCodeList =[]
        count =0
        if (len(token)!=0):
            for header in token:
                if header.id in self.byteRequired:
                    count += 1
                else:
                    pass

            code = self.subRegister(7, self.byteRequired[token[0].id]*count)
            self.byteCodeList.append(code)
        count = 0 # reset and reuse it
        for index in range(0,len(token)):
            if token[index].id == 'int':
                count +=1
            if token[index].id == '=':
                code = self.loadValue(7, self.byteRequired[token[0].id]*count, token[index].data[1].data[0])
                self.byteCodeList.append(code)




        return self.byteCodeList

        pass

    #Helper function
    def updateTheWorkingRegisterCounterAndStatus(self):
        if self.workingRegisterCounter > 2:
            self.workingRegisterCounter = 0
        if self.registerStatus[self.workingRegisterCounter] == 0:
            self.registerStatus[self.workingRegisterCounter] = 1




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