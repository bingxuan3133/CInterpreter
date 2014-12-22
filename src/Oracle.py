__author__ = 'JingWen'
class Oracle:


    MaxRegister = 6  # The maximum available register, the sixth number is to enable the counter move ahead always.
    registerFromLeft = 0  # Start with the location 0
    registerFromRight = MaxRegister - 1
    registerLeft = 5

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
        return self.registerFromLeft


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