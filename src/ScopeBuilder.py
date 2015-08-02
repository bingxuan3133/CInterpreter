__author__ = 'admin'

import copy

class Scope:
    def __init__(self):
        self.list = []
        self.displayList = []
        self.parentScope = None
        self.__repr__ = self.revealSelf

    def revealSelf(self):
        return '{}'.format(self.displayList)

class ScopeBuilder:
    def __init__(self):  # closing brace is used for implementation of buildScope
        self.scope = Scope()
        self.types = []
        self.currentScope = copy.copy(self.scope)
        self.scopeHistory = []

    def addType(self, *typeTokens):
        for typeToken in typeTokens:
            self.types.append(typeToken)

    def buildScope(self, token):
        if token.id == '(decl)':
            self.currentScope.list.append(token)
            self.currentScope.displayList.append(token.data[1].data[0])
        elif token.id == '(def)':
            self.currentScope.list.append(token.data[0])
            self.currentScope.displayList.append(token.data[0].data[1].data[0])
        elif token.id == '{':
            self.currentScope.parentScope = copy.copy(self.currentScope)
            newScopeList = []
            self.currentScope.list.append(newScopeList)
            self.currentScope.list = newScopeList
            newScopeDisplayList = []
            self.currentScope.displayList.append(newScopeDisplayList)
            self.currentScope.displayList = newScopeDisplayList
        elif token.id == '}':
            self.currentScope = self.currentScope.parentScope
            self.currentScope.list.pop()
            self.currentScope.displayList.pop()
        else:
            pass
        self.scopeHistory.append(copy.deepcopy(self.scope.list))
        return

    def removeSubToken(self, token):
        subToken = None
        if token.id == '{':
            subToken = token.data
            token.data = []
        return subToken

    def findLocal(self, identifierName):
        for declToken in self.currentScope.list:
            if declToken.data[0].data[0].data[0] == identifierName:
                return declToken
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

    def xfindGlobal(self, identifierName):
        token = self.findLocal(identifierName)
        if token is None and self.currentScope.parentScope is not None:
            savedScope = self.currentScope
            self.currentScope = self.currentScope.parentScope
            token = self.xfindGlobal(self.currentScope)
            self.currentScope = savedScope
            return token
        return None
