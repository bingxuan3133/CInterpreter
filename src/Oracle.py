__author__ = 'JingWen'
class Oracle:

    registerStatus = [0, 0, 0, 0, 0, 0, 0, 0]   # 1 represent the location of the register is in use
                                                # 0 represent the location is free to be overwrite
    workingRegisterCounter = 0  # Start with the location 0
    MaxRegister = 6  # The maximum available register, the sixth number is to enable the counter move ahead always.
    registerLeft = 5

    def getAFreeWorkingRegister(self):
        temp = self.workingRegisterCounter
        if self.workingRegisterCounter < self.MaxRegister:
            self.workingRegisterCounter += 1
            self.registerLeft -= 1
        return temp

    def releaseAWorkingRegister(self):
        if self.workingRegisterCounter > 0:
            self.workingRegisterCounter -= 1
            self.registerLeft += 1
        return self.workingRegisterCounter