__author__ = 'admin'

class Scope:
    def __init__(self, closeBrace):
        self.list = []
        self.currentScope = self.list
        self.interestedTokens = []
        self.closeBrace = closeBrace

    def buildScope(self, token):
        if token.id is '{':
            newList = []
            self.currentScope.append(newList)
            self.parentScope = self.currentScope
            self.currentScope = newList
        elif token.id is '}':
            self.currentScope = self.parentScope
            self.parentScope.pop()
        else:
            self.currentScope.append(token)
        return

    def scanForInterestedTokens(self, tree):
        if type(tree) is list:
            for subTree in tree:
                self.scanForInterestedTokens(subTree)
        else:
            if tree.id is 'int':
                self.interestedTokens.append(tree)
            elif tree.id is '{':
                self.interestedTokens.append(tree)
                subTree = self.removeSubToken(tree)
                self.scanForInterestedTokens(subTree)
                self.interestedTokens.append(self.closeBrace)
        return self.interestedTokens

    def removeSubToken(self, token):
        if token.id is 'int':
            pass
        elif token.id is '{':
            subToken = token.data
            token.data = []
        return subToken
