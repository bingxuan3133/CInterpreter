__author__ = 'JingWen'

class RegisterAllocator:
    def __init__(self, byteCodeGenerator):
        self.generator = byteCodeGenerator

    def decideWhetherToPush(self, token):
        number = 0b000000
        if self.generator.mapping.registerLeft < token.minRequiredRegister:
            registerToPush = token.maxRequiredRegister - self.generator.mapping.registerLeft
            returnedWorkingRegister = self.generator.mapping.releaseAWorkingRegister()
            while returnedWorkingRegister != 'Finish':
                registerToPush -= 1
                number = number | 0b1 << (returnedWorkingRegister)
                if registerToPush == 0:
                    break
                returnedWorkingRegister = self.generator.mapping.releaseAWorkingRegister()
            tempList = [7,number]
            self.generator.storeMultiple(tempList)


        return number

    def decideWhetherToPop(self, number):
        count =0
        if number != 0:
            tempList = [7,number]
            self.generator.loadMultiple(tempList)
            while number != 0:
                bit = number & 0b000001
                number = number >> 1
                if bit == 1:
                    count += 1
            for loop in range(0,count+2):
                self.generator.mapping.getAFreeWorkingRegister()
