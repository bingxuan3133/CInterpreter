__author__ = 'JingWen'

import os,sys
lib_path = os.path.abspath('\..\src')
sys.path.append(lib_path)

from Context import *
import Error
class DeclarationContext(Context):
    def __init__(self, contextManager):
        Context.__init__(self, contextManager)
        self.addOperator(',', 0)
        self.addOperator('=', 0)  # for declaration context to recognise '='
        self.addOperator(';', 0)  # for declaration context to recognise ';'
        self.addOperator(')', 0)
        self.addOperator(']', 0)
        self.addGroupOperator('(', 0)
        self.addPointerOperator('*', 120)
        self.addSubscriptOperator('[', 150)
        self.addPrimitive('int', 0)
        self.addShortType('short', 0)
        self.addLongType('long', 0)
        self.addSignedAndUnsignedType('signed', 0)
        self.addSignedAndUnsignedType('unsigned', 0)

    def createDeclarationOrDefinitionToken(self, word):
        sym = self.symbol(word)
        sym.arity = None
        sym.__repr__ = revealSelf
        symObj = sym()
        return symObj

    def addGroupOperator(self, id, bindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.peep('(')  # can be deleted
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep(')')
            thisContext.contextManager.parser.lexer.advance()
            return self
        def led(self, leftToken):
            thisContext.contextManager.parser.lexer.advance()
            return self
        sym = self.addOperator(id, bindingPower, nud, led)
        return sym

    def addPointerOperator(self, id, bindingPower):  # *
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(bindingPower)
            if thisContext.getIdentifier(returnedToken) is None:
                if returnedToken.id == '(multiple)':
                    returnedToken = thisContext.getReference(returnedToken)
                caretMessage = ' '*(returnedToken.column-1)+'^'
                raise SyntaxError("Error[{}][{}]:Expecting (identifier) before {}\n{}\n{}"\
                             .format(returnedToken.line,returnedToken.column,returnedToken.id,returnedToken.oriString,caretMessage))
            self.data.append(returnedToken)
            return self
        def led(self, token):
            pass
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting ; before {}\n{}\n{}"\
                             .format(self.line,self.column,self.id,self.oriString,caretMessage))
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addSubscriptOperator(self, id, bindingPower):  # []
        thisContext = self
        def nud(self):
            pass
            """
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting (identifier) before {}\n{}\n{}"\
                             .format(self.line,self.column,self.id,self.oriString,caretMessage))
            """
        def led(self, leftToken):
            self.data.append(leftToken)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            if returnedToken.id == '(multiple)':
                returnedToken = thisContext.getReference(returnedToken)
                caretMessage = ' '*(returnedToken.column-1)+'^'
                raise SyntaxError("Error[{}][{}]:Expecting expression before {}\n{}\n{}"\
                            .format(returnedToken.line,returnedToken.column,returnedToken.id,returnedToken.oriString,caretMessage))
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep(']')
            thisContext.contextManager.parser.lexer.advance()
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def parseIdentifierToken(self):
        identifierToken = self.contextManager.parser.parse(0)  # parser stops when meet '=' or ';'
        return identifierToken

    def parseDefToken(self):
        token = self.contextManager.parser.lexer.peep()
        self.contextManager.pushCurrentContexts()
        self.contextManager.setCurrentContextsByName('Expression', 'Default')
        if token.id == '=':
            token = self.contextManager.parser.lexer.advance()
            expressionToken = self.contextManager.parser.parse(0)
            self.contextManager.setCurrentContexts(self.contextManager.popContexts())
            return expressionToken
        else:
            self.contextManager.setCurrentContexts(self.contextManager.popContexts())
            return None

    def addPrimitive(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = None
            self.sign = 'signed'
            self.reference = self
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            thisContext.contextManager.pushCurrentContexts()
            thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id in ('(identifier)', '*', '('):
                identifierToken = thisContext.parseIdentifierToken()
                thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                expressionToken = thisContext.parseDefToken()
                self.identifierList.append(identifierToken)
                self.expressionList.append(expressionToken)
            elif nextToken.id == 'short':
                self.modifier = 'short'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id == 'long':
                self.modifier = 'long'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'short':
                    self.modifier = 'short'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'long':
                    self.modifier = 'long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                thisContext.contextManager.pushCurrentContexts()
                thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken
        def led(self, token):
            raise SyntaxError
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addSignedAndUnsignedType(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = None
            self.sign = self.id
            self.reference = self
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            thisContext.contextManager.pushCurrentContexts()
            thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id in ('(identifier)', '*', '('):
                
                
                identifierToken = thisContext.parseIdentifierToken()
                thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                expressionToken = thisContext.parseDefToken()
                self.identifierList.append(identifierToken)
                self.expressionList.append(expressionToken)

            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'short':
                    self.modifier = 'short'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'long':
                    self.modifier = 'long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id == 'long':
                self.modifier = 'long'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id == 'short':
                self.modifier = 'short'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:  # Deal with assignment or comma in declaration statement
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                thisContext.contextManager.pushCurrentContexts()
                thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken
        def led(self, token):
            raise SyntaxError
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addLongType(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = 'long'
            self.sign = 'signed'
            self.reference = self
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            thisContext.contextManager.pushCurrentContexts()
            thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
            nextToken = thisContext.contextManager.parser.lexer.advance()

            if nextToken.id in ('(identifier)', '*', '('):
                
                
                identifierToken = thisContext.parseIdentifierToken()
                thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                expressionToken = thisContext.parseDefToken()
                self.identifierList.append(identifierToken)
                self.expressionList.append(expressionToken)
            elif nextToken.id == 'long':
                self.modifier = 'long long'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken

            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            
                            
                            identifierToken = thisContext.parseIdentifierToken()
                            thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                            expressionToken = thisContext.parseDefToken()
                            self.identifierList.append(identifierToken)
                            self.expressionList.append(expressionToken)
                        elif nextToken.id in ('signed', 'unsigned'):
                            self.sign = nextToken.id
                            nextToken = thisContext.contextManager.parser.lexer.advance()
                            if nextToken.id in ('(identifier)', '*', '('):
                                
                                
                                identifierToken = thisContext.parseIdentifierToken()
                                thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                                expressionToken = thisContext.parseDefToken()
                                self.identifierList.append(identifierToken)
                                self.expressionList.append(expressionToken)
                            else:
                                self.errorToken = nextToken
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                thisContext.contextManager.pushCurrentContexts()
                thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken

        def led(self, token):
            raise SyntaxError
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addShortType(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = 'short'
            self.sign = 'signed'
            self.reference = self
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            thisContext.contextManager.pushCurrentContexts()
            thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id in ('(identifier)', '*', '('):
                
                
                identifierToken = thisContext.parseIdentifierToken()
                thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                expressionToken = thisContext.parseDefToken()
                self.identifierList.append(identifierToken)
                self.expressionList.append(expressionToken)
            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                        self.errorToken = nextToken

            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        
                        
                        identifierToken = thisContext.parseIdentifierToken()
                        thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                        expressionToken = thisContext.parseDefToken()
                        self.identifierList.append(identifierToken)
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                thisContext.contextManager.pushCurrentContexts()
                thisContext.contextManager.setCurrentContextsByName('Declaration', 'Default')
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    
                    
                    identifierToken = thisContext.parseIdentifierToken()
                    thisContext.contextManager.setCurrentContexts(thisContext.contextManager.popContexts())
                    expressionToken = thisContext.parseDefToken()
                    self.identifierList.append(identifierToken)
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken

        def led(self, token):
            raise SyntaxError
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def getIdentifier(self, token):
        if hasattr(token, 'id') and token.id == '(identifier)':
            return token
        else:
            if hasattr(token, 'data') and len(token.data) > 0:
                token = self.getIdentifier(token.data[0])
                return token
            else:
                return None

    def getReference(self, token):
        if hasattr(token, 'id') and token.id == '(decl)':
            return token.data[0].reference
        else:
            if hasattr(token, 'data') and len(token.data) > 0:
                token = self.getReference(token.data[0])
                return token
            else:
                return None

    def removeIdentifier(self, token):
        if token.data[0].id == '(identifier)':
            token.data.remove(token.data[0])
        else:
            self.removeIdentifier(token.data[0])

    def handleError(self, token):
        caretMessage = ' '*(token.errorToken.column-1)+'^'
        if token.errorToken.id in (';', '(systemToken)'):
            raise SyntaxError("Error[{}][{}]:Expecting (identifier) before {}\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.id,token.errorToken.oriString,caretMessage))
        elif token.errorToken.id in (token.sign, token.modifier, token.primitive):
            raise SyntaxError("Error[{}][{}]:Duplication of '{}' in declaration statement\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.id,token.errorToken.oriString,caretMessage))
        elif token.errorToken.id in ('short', 'long'):
            raise SyntaxError("Error[{}][{}]:Cannot have both 'short' and 'long' in declaration statement\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.oriString,caretMessage))
        elif token.errorToken.id in ('unsigned', 'signed'):
            raise SyntaxError("Error[{}][{}]:Cannot have both 'signed' and 'unsigned' in this declaration statement\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.oriString,caretMessage))
        else:
            raise SyntaxError("Error[{}][{}]:Expecting (identifier) before {}\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.id,token.errorToken.oriString,caretMessage))

    def buildToken(self, token):
        if token.errorToken is not None:
            self.handleError(token)
        multiple = self.createDeclarationOrDefinitionToken('(multiple)')  # (multiple) carry multiple tokens
        for identifier, expression in zip(token.identifierList, token.expressionList):  # zip used to loop 2 list in one time
            primitiveToken = self.createToken(token.primitive)
            primitiveToken.sign = token.sign
            primitiveToken.modifier = token.modifier
            primitiveToken.reference = token.reference
            declToken = self.createDeclarationOrDefinitionToken('(decl)')  # declaration token
            declToken.data.append(primitiveToken)
            declToken.data.append(self.getIdentifier(identifier))
            primitiveToken.data.append(identifier)
            self.removeIdentifier(primitiveToken)
            if expression is None:
                multiple.data.append(declToken)
            else:
                defToken = self.createDeclarationOrDefinitionToken('(def)')  # definition token
                defToken.data.append(declToken)
                defToken.data.append(expression)  # get definition
                multiple.data.append(defToken)
        return multiple
"""
    def addPointerDeclaration(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        # symClass.led = led
        return symClass
        pass


    def addPrimitive(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.ruleCheck(self)
            return
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

    def addModifier(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.ruleCheck(self)
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

    def ruleCheck(self, token):
        if token.type == 'modifier':
            self.modifier.append(token.id)
            self.modifierCount += 1
        elif token.type == 'primitive':
            self.primitiveCount += 1
        return
"""

"""
        elif firstToken.id == 'int':

            firstToken = deepcopy(secondToken)
            identifierName = self.lexer.advance()
            firstToken.data.append(identifierName)
            list.append(firstToken)
            if self.lexer.peep().id != '(systemToken)':
                tempToken =self.lexer.peep()
                returnedToken = self.parse(bindingPower)
                if returnedToken.id != tempToken.id:
                    list.append(returnedToken)

            while self.lexer.peep().id == ',':
                firstToken = deepcopy(secondToken)
                identifierName = self.lexer.advance()
                firstToken.data.append(identifierName)
                list.append(firstToken)
                if self.lexer.peep().id != '(systemToken)':
                    tempToken =self.lexer.peep()
                    returnedToken = self.parse(bindingPower)
                    if returnedToken.id != tempToken.id:
                        list.append(returnedToken)
            return list
"""
