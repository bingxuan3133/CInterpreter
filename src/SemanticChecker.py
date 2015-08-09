__author__ = 'admin'

class SemanticChecker:
    def __init__(self, scopeBuilder=None):
        self.scopeBuilder = scopeBuilder
        self.isEnable = False  # SemanticChecker status (because some tests do not have declaration)

    def semanticCheck(self, token):
        if self.isEnable:
            self.checkIfAllIdentifiersAreDefined(token)
        else:
            return

    #  =================
    #  Assignment check
    #  =================
    def getTokenType(self, token):
        self.getIdentifier(token)
        #declToken = self.scopeBuilder.findLocal(token.data[0])

    def getIdentifierType(self, token):
        if len(token.data) is 0:
            return [token.id]
        else:
            tokenIdList = []
            if token.id != '(decl)':
                tokenIdList.append(token.id)
            returnedTokenId = self.getIdentifierType(token.data[0])
            tokenIdList.extend(returnedTokenId)
            return tokenIdList

    def getIdentifier(self, token):
        while hasattr(token, 'data') and token.data[0] is not None:
            if hasattr(token, 'id') and token.id == '(identifier)':  # check does token.id exists
                return token
            token = token.data[0]
        return None  # no identifier found

    def compareLeftAndRight(self):
        pass

    #  =================
    #  Declaration check
    #  =================
    def checkIfAllIdentifiersAreDefined(self, token):
        if token.id == '(identifier)':
            self.checkIfIdentifierIsDefined(token)
        else:
            if len(token.data) > 1:
                for tokenData in token.data:
                    self.checkIfAllIdentifiersAreDefined(tokenData)
            else:
                return

    def checkIfIdentifierIsDefined(self, token):  # token = (identifier) token
        declToken = self.scopeBuilder.findGlobal(token.data[0])  # identifier name
        if declToken is None:
            caretMessage = ' '*(token.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Undefined reference '{}'\n{}\n{}"\
                             .format(token.line,token.column,token.data[0],token.oriString,caretMessage))
