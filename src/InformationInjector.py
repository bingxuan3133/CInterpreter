__author__ = 'JingWen'
from ByteCodeGenerator import *
from FlowControlContext import *
class InformationInjector:
    def injectRegisterRequired(self, tokenToInject):
        if(self.bypassTheInjection(tokenToInject)):
            return
        elif tokenToInject.id == 'if':
            token = tokenToInject.data[0].data[0]
            self.injectRegisterRequired(token)
            for token in tokenToInject.data[1][0].data:
                self.injectRegisterRequired(token)
            if tokenToInject.data.__len__() == 3:
                for token in tokenToInject.data[2].data[0][0].data:
                    self.injectRegisterRequired(token)
            return
        elif tokenToInject.id == 'while':
            token = tokenToInject.data[0]
            self.injectRegisterRequired(token)
            for token in tokenToInject.data[1][0].data:
                self.injectRegisterRequired(token)
            return
        elif tokenToInject.id == 'do':
            token = tokenToInject.data[0]
            self.injectRegisterRequired(token)
            for token in tokenToInject.data[1][0].data:
                self.injectRegisterRequired(token)
            return
        elif self.canIgnore(tokenToInject.id):
            token = tokenToInject.data[0]
        elif tokenToInject.id == '(def)':
            token = tokenToInject.data[1]
            self.insertBasicInformationForLiteral(token)
            return
        elif tokenToInject.id == '(None)':
            pass
        elif tokenToInject.id == '(decl)':
            return
        else:
            token = tokenToInject
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
                tempRegisterRequired = self.insertBasicInformationForLiteral(element)
            elif element.id == '(floating)':
                tempRegisterRequired = self.insertBasicInformationForFloat(element)
            else:
                tempRegisterRequired = self.injectRegisterRequired(element)
            registerNumber.append(tempRegisterRequired)

        self.getTheWeightFromChild(token, weightIndex)
        self.findOutTheHeavierSide(token)

        thisLevelRegister = self.getSuitableRegisterFromTheChild(registerNumber)
        token.registerRequired = thisLevelRegister

        if token.id != '(identifier)' and token.id != '(literal)':
            token.maxRequiredRegister = self.determineTheMaxRequiredRegister(token)
            token.minRequiredRegister = self.determineTheMinRequiredRegister(token)

        return thisLevelRegister

    def bypassTheInjection(self,token):
        return ByteCodeGenerator.isADeclaration(self, token.id)

    def insertBasicInformationForLiteral(self, token):
        token.weight = []
        token.registerRequired = 1
        token.maxRequiredRegister = 1
        token.minRequiredRegister = 1
        token.weight.insert(0, 0)
        tempRegisterRequiredAtThatLevel = 1
        return tempRegisterRequiredAtThatLevel

    def insertBasicInformationForFloat(self,token):
        token.weight = []
        token.registerRequired = 2
        token.maxRequiredRegister = 2
        token.minRequiredRegister = 2
        token.weight.insert(0, 0)
        tempRegisterRequiredAtThatLevel = 2
        return tempRegisterRequiredAtThatLevel

    def getTheWeightFromChild(self,token,weightIndex):
        for data in token.data :
            if self.canIgnore(data.id):
                data = data.data[0]
            token.weight.insert(weightIndex, data.weight[0])
            weightIndex += 1

    def findOutTheHeavierSide(self,token):
        firstToken = token.data[0]
        secondToken = token.data[1]
        if self.canIgnore(firstToken.id):
            firstToken = firstToken.data[0]
        if self.canIgnore(secondToken.id):
            secondToken = secondToken.data[0]



        if (firstToken.weight[0]>secondToken.weight[0]):
            token.weight.insert(0, firstToken.weight[0]+1)
        else:
            token.weight.insert(0, secondToken.weight[0]+1)

    def determineTheMaxRequiredRegister(self, token):
        firstToken = token.data[0]
        secondToken = token.data[1]
        if self.canIgnore(firstToken.id):
            firstToken = firstToken.data[0]
        if self.canIgnore(secondToken.id):
            secondToken = secondToken.data[0]
        if self.canIgnore(token.id):
            return firstToken.maxRequiredRegister
        else:
            return firstToken.maxRequiredRegister+secondToken.maxRequiredRegister

    def determineTheMinRequiredRegister(self, token):
        firstToken = token.data[0]
        secondToken = token.data[1]
        if self.canIgnore(firstToken.id):
            firstToken = firstToken.data[0]
        if self.canIgnore(secondToken.id):
            secondToken = secondToken.data[0]

        if self.canIgnore(token.id):
            return firstToken.minRequiredRegister
        elif firstToken.minRequiredRegister > secondToken.minRequiredRegister:
            return firstToken.minRequiredRegister
        elif firstToken.minRequiredRegister < secondToken.minRequiredRegister:
            return secondToken.minRequiredRegister
        elif firstToken.minRequiredRegister == secondToken.minRequiredRegister:
            return firstToken.minRequiredRegister + secondToken.minRequiredRegister

    def getSuitableRegisterFromTheChild(self,registerNumber):
        if abs(registerNumber[0]) == abs(registerNumber[1]):
            suitableRegister = -abs(registerNumber[0])-1
        elif abs(registerNumber[0]) > abs(registerNumber[1]):
            suitableRegister = -abs(registerNumber[0])
        else:
            suitableRegister = abs(registerNumber[1])

        return suitableRegister

    def canIgnore(self, name):
        ignoreList = ['(']
        return name in ignoreList
