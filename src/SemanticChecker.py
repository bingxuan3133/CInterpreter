__author__ = 'admin'
import Error

class SemanticChecker:
    def __init__(self, scopeBuilder=None):
        self.scopeBuilder = scopeBuilder
        self.isEnable = False  # SemanticChecker status (because some tests do not have declaration)

    def semanticCheck(self, token):
        if self.isEnable:
            self.checkIfAllIdentifiersAreDefined(token)
            self.checkIfAllTokenTypeValid(token)
            self.checkIfAssignmentValid(token)
        else:
            pass
            return

    #  =================
    #  Assignment check
    #  =================
    def checkIfAssignmentValid(self, token):
        if token.id == '=':
            self.checkIfLvalueValid(token)
            leftType = self.getTokenType(token.data[0])
            rightType = self.checkIfAssignmentValid(token.data[1])
            if len(leftType) != len(rightType) or leftType[0] != rightType[0]:
                caretMessage = ' '*(token.column-1)+'^'
                raise SyntaxError("Error[{}][{}]:Incompatible assignment\n{}\n{}"\
                                  .format(token.line,token.column,token.oriString,caretMessage))
        elif token.id == '(def)':
            leftType = self.getTokenType(token.data[0].data[1])
            rightType = self.checkIfAssignmentValid(token.data[1])
            if len(leftType) != len(rightType) or leftType[0] != rightType[0]:
                caretMessage = ' '*(token.column-1)+'^'
                raise SyntaxError("Error[{}][{}]:Incompatible assignment\n{}\n{}"\
                                  .format(token.line,token.column,token.oriString,caretMessage))
        elif token.arity == 3:
            leftType = self.checkIfAssignmentValid(token.data[0])
            rightType = self.checkIfAssignmentValid(token.data[1])
            if len(leftType) > len(rightType):
                return leftType
            else:
                return rightType
        else:
            self.checkIfTokenTypeValid(token)
            typeList = self.getTokenType(token)
            return typeList

    def checkIfAllTokenTypeValid(self, token):
        if token.arity == 3:
            self.checkIfAllTokenTypeValid(token.data[0])
            self.checkIfAllTokenTypeValid(token.data[1])
            pass
        else:
            self.checkIfTokenTypeValid(token)
            pass

    def checkIfLvalueValid(self, token):
        if token.data[0].id == '&':
            raise SyntaxError(Error.generateErrorMessageWithNoArguement('Invalid lvalue type of assignment', token))
        elif token.data[0].id in ('(identifier)', '(literal)'):
            return
        elif token.data[0].arity == 3 and token.data[0].id != '[':
            Error.generateErrorMessageWithNoArguement('Invalid lvalue type of assignment', token)
        else:
            self.checkIfLvalueValid(token.data[0])

    def checkIfTokenTypeValid(self, token):
        idenToken = self.getIdentifier(token)
        if token.id == '(decl)':
            tokenType = self.getTokenType(token.data[1])
        elif token.id == '(def)':
            tokenType = self.getTokenType(token.data[0].data[1])
        else:
            tokenType = self.getTokenType(token)
        if len(tokenType) == 0:
            caretMessage = ' '*(idenToken.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Invalid type of '{}'\n{}\n{}"\
                              .format(idenToken.line,idenToken.column,idenToken.data[0],idenToken.oriString,caretMessage))

    def getTokenType(self, token):      # token = idenToken
        if token.id == '(literal)':
            if isinstance(token.data[0], int):
                return ['int']
            else:
                return ['double']
        declToken = self.scopeBuilder.findGlobal(token.data[0])
        if token.id == '(identifier)':
            typeList = self.getIdentifierDeclarationTypeList(declToken)  # a list of token declaration types - eg: [int, *, []
            return typeList
        else:
            typeList = self.getTokenType(token.data[0])
            if token.id in ('*', '['):
                typeList.pop()
            elif token.id is '&':
                typeList.append('*')
            return typeList

    def getIdentifierDeclarationTypeList(self, token):  # token = declToken from scope
        if len(token.data) is 0:
            return [token.id]
        else:
            tokenIdList = []
            if token.id != '(decl)':
                tokenIdList.append(token.id)
            returnedTokenId = self.getIdentifierDeclarationTypeList(token.data[0])
            tokenIdList.extend(returnedTokenId)
            return tokenIdList

    def getIdentifier(self, token):
        if hasattr(token, 'id') and token.id == '(identifier)':
            return token
        else:
            if hasattr(token, 'data') and len(token.data) > 0:
                if token.id == '(decl)':
                    token = self.getIdentifier(token.data[1])
                else:
                    token = self.getIdentifier(token.data[0])
                return token
            else:
                return None

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
