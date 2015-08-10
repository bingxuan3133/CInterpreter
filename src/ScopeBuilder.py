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
        self.types = []  # not implemented (int, char, double, user defined, etc)
        self.currentScope = copy.copy(self.scope)
        self.scopeHistory = []

    def addType(self, *typeTokens):  # not implemented (use for int, char, double, user defined, etc)
        for typeToken in typeTokens:
            self.types.append(typeToken)

    def buildScope(self, token):
        if token.id == '(decl)':
            self.addToCurrentScope(token)
        elif token.id == '(def)':
            self.addToCurrentScope(token.data[0])
        elif token.id == '{':
            self.currentScope.parentScope = copy.copy(self.currentScope)
            newScopeList = []
            self.currentScope.list.append(newScopeList)
            self.currentScope.list = newScopeList
            newScopeDisplayList = []
            self.currentScope.displayList.append(newScopeDisplayList)
            self.currentScope.displayList = newScopeDisplayList
        else:
            pass
        self.scopeHistory.append(copy.deepcopy(self.scope.list))
        return

    def destroyScope(self):
        self.currentScope = self.currentScope.parentScope
        self.currentScope.list.pop()
        self.currentScope.displayList.pop()
        self.scopeHistory.append(copy.deepcopy(self.scope.list))

    def addToCurrentScope(self, declToken):
        if self.findLocal(declToken.data[1].data[0]) is None:   # identifier is not declared before in the same scope
            self.currentScope.list.append(declToken)
            self.currentScope.displayList.append(declToken.data[1].data[0])
        else:                                                   # identifier redeclaration
            token = declToken.data[1]
            caretMessage = ' '*(token.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Redeclaration of '{}'\n{}\n{}"\
                             .format(token.line,token.column,token.data[0],token.oriString,caretMessage))

    def findLocal(self, identifierName):
        for declToken in self.currentScope.list:
            if isinstance(declToken, list):
                break
            elif declToken.data[1].data[0] == identifierName:
                return declToken
        return None

    def findGlobal(self, identifierName):
        token = self.findLocal(identifierName)
        if token is None and self.currentScope.parentScope is not None:
            savedScope = self.currentScope
            self.currentScope = self.currentScope.parentScope
            token = self.findGlobal(identifierName)
            self.currentScope = savedScope
            return token
        else:
            return token
