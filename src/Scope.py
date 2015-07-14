__author__ = 'admin'

import copy

class Scope:
    def __init__(self):
        self.list = []
        self.parentScope = None
        self.__repr__ = self.revealSelf

    def revealSelf(self):
        return '{0}'.format(self.list)

class ScopeBuilder:
    def __init__(self):  # closing brace is used for implementation of buildScope
        self.scope = Scope()
        self.currentScope = copy.copy(self.scope)
        self.interestedTokens = []
        self.scopeHistory = []

    def addScope(self):
        pass

    def buildScope(self, token):
        if token.id is 'int':
            self.currentScope.list.append(token.data[0].data[0])
        elif token.id is '{':
            self.currentScope.parentScope = copy.copy(self.currentScope)
            newScopeList = []
            self.currentScope.list.append(newScopeList)
            self.currentScope.list = newScopeList
        elif token.id is '}':
            self.currentScope = self.currentScope.parentScope
            self.currentScope.list.pop()
        else:
            pass
        self.scopeHistory.append(copy.deepcopy(self.scope.list))
        return

    def removeSubToken(self, token):
        subToken = None
        if token.id is '{':
            subToken = token.data
            token.data = []
        return subToken

    def findLocal(self, identifierName):
        for identifierToken in self.currentScope.list:
            if identifierToken.data[0].data[0] is identifierName:
                return identifierToken
        return None

    def findGlobal(self, identifierName):
        savedScope = self.currentScope
        while self.currentScope.parentScope is not None:
            for identifierToken in self.currentScope.list:
                if isinstance(identifierToken, list):  # is list object
                    break
                elif identifierToken.data[0].data[0] is identifierName:
                    self.currentScope = savedScope
                    return identifierToken
            self.currentScope = self.currentScope.parentScope
        self.currentScope = savedScope
        return None
