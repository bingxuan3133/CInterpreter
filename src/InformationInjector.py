__author__ = 'JingWen'

class InformationInjector:
    def injectRegisterRequired(self, token):
        registerNumber =[]
        token.weight = []
        weightIndex = 1
            # **weight**
            #- a list that store data in this format (ownWeight,leftWeight,rightWeight)
            #WHERE
            # =0 - equal weight or no child
            # >0 - right side is heavier

        for element in token.data:

            element.weight = []
            if element.id == '(identifier)' or element.id == '(literal)':
                tempRegisterRequiredAtThatLevel = self.insertBasicInformationForAChildToken(element)
            else:
                tempRegisterRequiredAtThatLevel = self.injectRegisterRequired(element)
            registerNumber.append(tempRegisterRequiredAtThatLevel)

        self.getTheWeightFromChild(token, weightIndex)
        self.findOutTheHeavierSide(token)

        thisLevelRegister = self.getSuitableRegisterFromTheChild(registerNumber)
        token.registerRequiredAtThatLevel = thisLevelRegister

        if token.id != '(identifier)' and token.id != '(literal)':
            token.maxRequiredRegister = self.determineTheMaxRequiredRegister(token)
            token.minRequiredRegister = self.determineTheMinRequiredRegister(token)

        return thisLevelRegister


    def insertBasicInformationForAChildToken(self, token):
        token.weight = []
        token.registerRequiredAtThatLevel = 1
        token.maxRequiredRegister = 1
        token.minRequiredRegister = 1
        token.weight.insert(0, 0)
        tempRegisterRequiredAtThatLevel = 1
        return tempRegisterRequiredAtThatLevel

    def getTheWeightFromChild(self,token,weightIndex):
        for data in token.data :
            token.weight.insert(weightIndex, data.weight[0])
            weightIndex += 1

    def findOutTheHeavierSide(self,token):
        if (token.data[0].weight[0]>token.data[1].weight[0]):
            token.weight.insert(0, token.data[0].weight[0]+1)
        else:
            token.weight.insert(0, token.data[1].weight[0]+1)

    def determineTheMaxRequiredRegister(self, token):
        return token.data[0].maxRequiredRegister+token.data[1].maxRequiredRegister

    def determineTheMinRequiredRegister(self, token):
        if token.data[0].minRequiredRegister > token.data[1].minRequiredRegister:
            return token.data[0].minRequiredRegister
        elif token.data[0].minRequiredRegister < token.data[1].minRequiredRegister:
            return token.data[1].minRequiredRegister
        elif token.data[0].minRequiredRegister == token.data[1].minRequiredRegister:
            return token.data[0].minRequiredRegister + token.data[1].minRequiredRegister

    def getSuitableRegisterFromTheChild(self,registerNumber):
        if abs(registerNumber[0]) == abs(registerNumber[1]):
            suitableRegister = -abs(registerNumber[0])-1
        elif abs(registerNumber[0]) > abs(registerNumber[1]):
            suitableRegister = -abs(registerNumber[0])
        else:
            suitableRegister = abs(registerNumber[1])

        return suitableRegister

