__author__ = 'JingWen'

class RegisterAllocator:
    def __init__(self, byteCodeGenerator):
        self.generator = byteCodeGenerator

    def decideWhetherToPush(self, token):
        number = 0b000000
        if self.generator.oracle.registerLeft < token.minRequiredRegister:
            registerToPush = token.maxRequiredRegister - self.generator.oracle.registerLeft
            returnedWorkingRegister = self.generator.oracle.releaseALargestWorkingRegister()

            while returnedWorkingRegister != 'Finish':
                registerToPush -= 1
                number = number | 0b1 << (returnedWorkingRegister)
                if registerToPush == 0:
                    break
                returnedWorkingRegister = self.generator.oracle.releaseALargestWorkingRegister()

            self.generator.storeMultiple(7, number)


        return number

    def decideWhetherToPop(self, number):
        count =0
        if number != 0:
            self.generator.loadMultiple(7, number)
            while number != 0:
                bit = number | 0b000001
                number = number >> 1
                if bit == 1:
                    self.generator.oracle.getSpecificWorkingRegister(count)
                count += 1