__author__ = 'JingWen'
class Oracle:

    registerStatus = [0, 0, 0, 0, 0, 0, 0, 0]   # 1 represent the location of the register is in use
                                                # 0 represent the location is free to be overwrite
    workingRegisterCounter = 0  # Start with the location 0
    MaxRegister = 6  # The maximum available register, the sixth number is to enable the counter move ahead always.
    registerLeft = 5

    def getAFreeWorkingRegister(self):
        temp = 100
        if self.workingRegisterCounter < self.MaxRegister:
            if self.registerStatus[self.workingRegisterCounter] == 0:
                temp = self.workingRegisterCounter
                self.workingRegisterCounter += 1
            else:
                while self.registerStatus[self.workingRegisterCounter] == 1:
                    self.workingRegisterCounter += 1
                temp = self.workingRegisterCounter
            self.registerLeft -= 1
            self.registerStatus[temp] = 1
        return temp

    def releaseAWorkingRegister(self):
        temp = self.MaxRegister - 1
        while self.registerStatus[temp] != 1:
            temp -= 1
        self.registerStatus[temp] = 0
        self.workingRegisterCounter = temp - 1
        self.registerLeft += 1
        return temp
    def getSpecificWorkingRegister(self, numberOfRegister):
        if self.registerStatus[numberOfRegister] == 0:
            self.registerStatus[numberOfRegister] = 1
            self.registerLeft -= 1
