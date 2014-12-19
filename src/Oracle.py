__author__ = 'JingWen'
class Oracle:

    registerStatus = [0, 0, 0, 0, 0, 0, 0, 0]   # 1 represent the location of the register is in use
                                                # 0 represent the location is free to be overwrite
    workingRegisterCounter = 0  # Start with the location 0
    MaxRegister = 6  # The maximum available register, the sixth number is to enable the counter move ahead always.
    registerLeft = 5

    def getAFreeWorkingRegister(self):
        temp = 0
        while self.registerStatus[temp] != 0:
            if temp > self.MaxRegister-1: #Error chance remark
                return 'Finish'
            temp += 1
        self.registerStatus[temp] = 1
        self.workingRegisterCounter = temp + 1
        return temp
    def getALargestWorkingRegister(self):
        temp = self.MaxRegister -1
        while self.registerStatus[temp] != 0:
            if temp < 0:
                return 'Finish'
            temp -= 1
        self.registerStatus[temp] = 1
        self.workingRegisterCounter = temp - 1
        return temp
    def releaseALargestWorkingRegister(self):
        temp = self.MaxRegister - 1
        while self.registerStatus[temp] != 1:
            if temp == -1:
                return 'Finish'
            temp -= 1
        self.registerStatus[temp] = 0
        self.workingRegisterCounter = temp
        self.registerLeft += 1
        return temp

    def releaseAWorkingRegister(self):
        temp = 0
        while self.registerStatus[temp] != 1:
            if temp > self.MaxRegister-1:
                return 'Finish'
            temp += 1
        self.registerStatus[temp] = 0
        self.workingRegisterCounter = temp
        self.registerLeft += 1
        return temp


    def getSpecificWorkingRegister(self, numberOfRegister):
        if self.registerStatus[numberOfRegister] == 0:
            self.registerStatus[numberOfRegister] = 1
            self.registerLeft -= 1

    def releaseSpecificWorkingRegister(self, numberOfRegister):
        if self.registerStatus[numberOfRegister] == 1:
            self.registerStatus[numberOfRegister] = 0
            self.registerLeft += 1
