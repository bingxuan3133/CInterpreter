__author__ = 'admin'

class SemanticChecker:
    def __init__(self):
        #self.scopeBuilder = scopeBuilder
        pass

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
