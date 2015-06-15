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
    def __init__(self, closeBrace):  # closing brace is used for implementation of buildScope
        self.scope = Scope()
        self.currentScope = copy.copy(self.scope)
        self.closeBrace = closeBrace
        self.interestedTokens = []

    def buildScope(self, token):
        if token.id is '{':
            self.currentScope.parentScope = copy.copy(self.currentScope)
            newScopeList = []
            self.currentScope.list.append(newScopeList)
            self.currentScope.list = newScopeList
        elif token.id is '}':
            self.currentScope = self.currentScope.parentScope
            self.currentScope.list.pop()
        else:
            self.currentScope.list.append(token)
        return

    def scanForInterestedTokens(self, tree):  # tree: Parsed Tree
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
                self.interestedTokens.append(self.closeBrace)   # add closing brace when detect end of a scope
            else:
                pass
        return self.interestedTokens

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
