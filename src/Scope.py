__author__ = 'admin'

class Scope:
    interestedTokens = []

    def __init__(self, closeBrace):
        self.list = []
        self.parentScope = self.list
        self.closeBrace = closeBrace

    def buildScope(self, token):
        self.currentScope = Scope(self.closeBrace)
        if token.id is '{':
            newList = []
            self.currentScope = Scope(self.closeBrace)
            self.currentScope.parentScope = self.currentScope.list
            self.currentScope.list = newList
        elif token.id is '}':
            self.currentScope.list = self.currentScope.parentScope
            self.currentScope.parentScope.pop()
        else:
            self.currentScope.list.append(token)
        return

    def scanForInterestedTokens(self, tree):
        if type(tree) is list:
            for subTree in tree:
                self.scanForInterestedTokens(subTree)
        else:
            if tree.id is 'int':
                Scope.interestedTokens.append(tree)
            elif tree.id is '{':
                Scope.interestedTokens.append(tree)
                subTree = self.removeSubToken(tree)
                self.scanForInterestedTokens(subTree)
                Scope.interestedTokens.append(self.closeBrace)
        return Scope.interestedTokens

    def removeSubToken(self, token):
        if token.id is '{':
            subToken = token.data
            token.data = []
        return subToken

    def findLocal(self, identifier):
        for dataType in self.currentScope.list:
            if dataType.data[0].data[0] is identifier:
                return dataType
        return None