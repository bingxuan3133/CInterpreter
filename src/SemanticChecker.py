__author__ = 'admin'

class SemanticChecker:
    def __init__(self, scopeBuilder=None):
        self.scopeBuilder = scopeBuilder
        self.isEnable = False  # SemanticChecker status (because some tests do not have declaration)

    def semanticCheck(self, token):
        if self.isEnable:
            self.checkIfAllIdentifiersAreDefined(token)
            self.checkIfAssignmentValid(token)
        else:
            return

    #  =================
    #  Assignment check
    #  =================
    def getTokenType(self, token):
        declToken = self.scopeBuilder.findLocal(token.data[0])
        if token.id == '(identifier)':
            typeList = self.getIdentifierDeclarationType(declToken)  # a list of token declaration types - eg: [int, *, []
            return typeList
        else:
            typeList = self.getTokenType(token.data[0])
            if token.id in ('*', '['):
                typeList.pop()
            return typeList

    def getIdentifierDeclarationType(self, token):
        if len(token.data) is 0:
            return [token.id]
        else:
            tokenIdList = []
            if token.id != '(decl)':
                tokenIdList.append(token.id)
            returnedTokenId = self.getIdentifierDeclarationType(token.data[0])
            tokenIdList.extend(returnedTokenId)
            return tokenIdList

    def getIdentifier(self, token):
        if hasattr(token, 'id') and token.id == '(identifier)':
            return token
        else:
            if hasattr(token, 'data') and len(token.data) > 0:
                token = self.getIdentifier(token.data[0])
                return token
            else:
                return None

    def checkIfTypeValid(self, token):
        idenToken = self.getIdentifier(token)
        tokenType = self.getTokenType(token)
        if len(tokenType) == 0:
            caretMessage = ' '*(token.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Invalid type of '{}'\n{}\n{}"\
                                .format(idenToken.line,idenToken.column,idenToken.data[0],idenToken.oriString,caretMessage))

    def checkIfAssignmentValid(self, token):
        if token.id == '=':
            self.checkIfTypeValid(token.data[0])
            self.checkIfTypeValid(token.data[1])
        else:
            self.checkIfTypeValid(token)

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
            raise SyntaxError("Error[{}][{}]:'{}' is not declared\n{}\n{}"\
                             .format(token.line,token.column,token.data[0],token.oriString,caretMessage))
