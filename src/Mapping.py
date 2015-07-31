__author__ = 'JingWen'
class Mapping:

    MaxRegister = 6  # The maximum available register, the sixth number is to enable the counter move ahead always.
    registerFromLeft = 0  # Start with the location 0
    registerFromRight = MaxRegister - 1
    registerLeft = MaxRegister

    framePointerRegister = MaxRegister + 1

    smallerRegisterUsed = 0

    def reset(self):
        self.registerFromLeft = 0  # Start with the location 0
        self.registerFromRight = self.MaxRegister - 1
        self.registerLeft = self.MaxRegister

        self.framePointerRegister = self.MaxRegister + 1

        self.smallerRegisterUsed = 0

    def getAFreeWorkingRegister(self):
        if self.registerLeft == 0:
            raise SyntaxError("No register is free to allocate")
        self.checkReservedRegister()
        temp = self.registerFromLeft
        self.registerFromLeft += 1
        self.registerLeft -= 1
        return temp

    def getALargestWorkingRegister(self):
        if self.registerLeft == 0:
            raise SyntaxError("No register is free to allocate")
        temp = self.registerFromRight
        self.registerFromRight -= 1
        self.registerLeft -= 1
        return temp

    def releaseALargestWorkingRegister(self):
        if self.registerLeft == self.MaxRegister:
            raise SyntaxError("No register can be release")
        self.registerFromRight += 1
        self.registerLeft += 1
        return self.registerFromRight

    def releaseAWorkingRegister(self):
        if self.registerLeft == self.MaxRegister:
            raise SyntaxError("No register can be release")
        self.registerFromLeft -= 1
        self.registerLeft += 1
        return self.registerFromLeft

    def getASmallestFreeRegisterBeforePop(self,status):
        count = 0
        while status != 0:
            status = status >> 1
            count += 1
        self.smallerRegisterUsed += 1
        return count

    def checkReservedRegister(self):
        while self.smallerRegisterUsed > 0:
            self.smallerRegisterUsed -= 1
            self.getAFreeWorkingRegister()

"""
    def getSpecificWorkingRegister(self, numberOfRegister):
        if self.registerStatus[numberOfRegister] == 0:
            self.registerStatus[numberOfRegister] = 1
            self.registerLeft -= 1

    def releaseSpecificWorkingRegister(self, numberOfRegister):
        if self.registerStatus[numberOfRegister] == 1:
            self.registerStatus[numberOfRegister] = 0
            self.registerLeft += 1
"""

