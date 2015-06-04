__author__ = 'JingWen'

class InformationInjector:
    def injectRegisterRequired(self, token):
        registerNumber =[]
        token.weight = []
        for element in token.data:
            weightIndex = 1

            element.weight = []
            if element.id == '(identifier)' or element.id == '(literal)':
                element.registerRequiredAtThatLevel = 1
                element.maxRequiredRegister = 1
                element.minRequiredRegister = 1

                # **weight**
                # =0 - equal weight or no child
                # >0 - right side is heavier
                # <0 - left side is heavier
                # - a list that store data in this format (ownWeight,leftWeight,rightWeight)
                element.weight.insert(0, 0)

                tempRegisterRequiredAtThatLevel = 1

            else:
                tempRegisterRequiredAtThatLevel = self.injectRegisterRequired(element)
            registerNumber.append(tempRegisterRequiredAtThatLevel)
        token.weight.insert(weightIndex, token.data[0].weight[0])
        token.weight.insert(weightIndex + 1, token.data[1].weight[0])
        if (token.data[0].weight[0]>token.data[1].weight[0]):
            token.weight.insert(0, token.data[0].weight[0]+1)
        else:
            token.weight.insert(0, token.data[1].weight[0]+1)
        if abs(registerNumber[0]) == abs(registerNumber[1]):
            largest = -abs(registerNumber[0])-1
        elif abs(registerNumber[0]) > abs(registerNumber[1]):
            largest = -abs(registerNumber[0])
        else:
            largest = abs(registerNumber[1])
        token.registerRequiredAtThatLevel = largest

        if token.id != '(identifier)' and token.id != '(literal)':
            token.maxRequiredRegister = token.data[0].maxRequiredRegister+token.data[1].maxRequiredRegister
            if token.data[0].minRequiredRegister > token.data[1].minRequiredRegister:
                token.minRequiredRegister = token.data[0].minRequiredRegister
            elif token.data[0].minRequiredRegister < token.data[1].minRequiredRegister:
                token.minRequiredRegister = token.data[1].minRequiredRegister
            elif token.data[0].minRequiredRegister == token.data[1].minRequiredRegister:
                token.minRequiredRegister = token.data[0].minRequiredRegister + token.data[1].minRequiredRegister
        return largest