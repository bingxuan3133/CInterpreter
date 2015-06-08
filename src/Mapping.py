__author__ = 'JingWen'
class Mapping:


    MaxRegister = 6  # The maximum available register, the sixth number is to enable the counter move ahead always.
    registerFromLeft = 0  # Start with the location 0
    registerFromRight = MaxRegister - 1
    registerLeft = MaxRegister
    framePointerRegister = MaxRegister + 1

    smallerRegisterUsed = 0

    def getAFreeWorkingRegister(self):
        temp = self.registerFromLeft
        self.registerFromLeft += 1
        self.registerLeft -= 1
        return temp
    def getALargestWorkingRegister(self):
        temp = self.registerFromRight
        self.registerFromRight -= 1
        self.registerLeft -= 1
        return temp
    def releaseALargestWorkingRegister(self):
        self.registerFromRight += 1
        self.registerLeft += 1
        return self.registerFromRight


    def releaseAWorkingRegister(self):

        self.registerFromLeft -= 1
        self.registerLeft += 1
        while self.smallerRegisterUsed > 0:
            self.smallerRegisterUsed -= 1
            self.releaseAWorkingRegister()
        return self.registerFromLeft

    def getASmallestFreeRegisterBeforePop(self,status):
        count = 0
        while status != 0:
            status = status >> 1
            count += 1
        self.smallerRegisterUsed += 1
        return count


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