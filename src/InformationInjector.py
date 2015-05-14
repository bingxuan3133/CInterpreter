__author__ = 'JingWen'

class InformationInjector:
    def injectRegisterRequired(self, token):
        registerNumber =[]
        for element in token.data:
            if element.id == '(identifier)' or element.id == '(literal)':
                element.registerRequiredAtThatLevel = 1
                element.maxRequiredRegister = 1
                element.minRequiredRegister = 1
                tempRegisterRequiredAtThatLevel = 1

            else:
                tempRegisterRequiredAtThatLevel = self.injectRegisterRequired(element)

            registerNumber.append(tempRegisterRequiredAtThatLevel)
        if abs(registerNumber[0]) == abs(registerNumber[1]):
            largest = -abs(registerNumber[0])-1
        elif abs(registerNumber[0]) > abs(registerNumber[1]):
            largest = -abs(registerNumber[0])
        else:
            largest = abs(registerNumber[1])
        token.registerRequiredAtThatLevel = largest

        if token.id != '(identifier)' and token.id != '(literal':
            token.maxRequiredRegister = token.data[0].maxRequiredRegister+token.data[1].maxRequiredRegister
            if token.data[0].minRequiredRegister > token.data[1].minRequiredRegister:
                token.minRequiredRegister = token.data[0].minRequiredRegister
            elif token.data[0].minRequiredRegister < token.data[1].minRequiredRegister:
                token.minRequiredRegister = token.data[1].minRequiredRegister
            elif token.data[0].minRequiredRegister == token.data[1].minRequiredRegister:
                token.minRequiredRegister = token.data[0].minRequiredRegister + token.data[1].minRequiredRegister
        return largest