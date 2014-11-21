from Context import *
from ContextManager import *

class FlowControlContext(Context):
    def addBlockOperator(self, id, bindingPower = 0 ):
        thisContext = self
        symClass = self.symbol(id, bindingPower)
        def led(self):
            return self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.parseStatement(bindingPower)
            nextToken = thisContext.contextManager.parser.lexer.peep(';')
            nextToken = thisContext.contextManager.parser.lexer.advance()
            self.data.append(returnedToken)
            while thisContext.contextManager.parser.lexer.peep().id is not '}':
                thisContext.contextManager.parser.lexer.advance()
                returnedToken = thisContext.parseStatement(bindingPower)
                nextToken = thisContext.contextManager.parser.lexer.peep(';')
                nextToken = thisContext.contextManager.parser.lexer.advance()
                self.data.append(returnedToken)
            return self
        symClass.nud = nud
        symClass.led = led
        symClass = self.addOperator(id, bindingPower) #removed the nud and led.
        return symClass

    def addWhileControl(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance('(')
            contexts = thisContext.contextManager.getCurrentContexts()
            thisContext.contextManager.pushContexts(contexts)  # save context
            default = thisContext.contextManager.getContext('Default')
            expression = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setCurrentContexts([expression, default])
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            wadisthis = thisContext.contextManager.parser.lexer.peep(')')
            contexts = thisContext.contextManager.popContexts()  # pop previously saved context
            thisContext.contextManager.setCurrentContexts(contexts)
            wadisthis = thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.parseStatement(self.bindingPower)
            self.data.append(returnedToken)
            return self
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addDoWhileControl(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            context = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setCurrentContexts([context])               # Will be implement as push into stack later
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep()
            context2 = thisContext.contextManager.getContext('FlowControl')
            thisContext.contextManager.setCurrentContexts([context, context2])     # Will be implement as pop from stack later
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        def led(self):
            pass
        symClass = self.symbol(id,bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addIfControl(self,id,bindingPower=0):
        thisContext = self
        def nud(self):
            headToken = thisContext.contextManager.parser.lexer.advance('(')
            thisContext.contextManager.pushContexts(thisContext.contextManager.currentContexts)
            newContext = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setCurrentContexts([newContext])
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(bindingPower)
            headToken.data.append(returnedToken)
            self.data.append(headToken)
            thisContext.contextManager.parser.lexer.peep(')')
            tempContext =  thisContext.contextManager.popContexts()
            thisContext.contextManager.setCurrentContexts(tempContext)
            nextToken = thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.parseStatement(bindingPower)
            self.data.append(returnedToken)
            return self
        def led(self, leftToken):
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def parseStatement(self, bindingPower):
        if self.contextManager.parser.lexer.peep().id is ';':
            self.contextManager.parser.lexer.advance()
            return
        returnedToken = self.contextManager.parser.parse(bindingPower)
        if returnedToken is None:
            return None
        else:
            if returnedToken.id is '{':
                self.contextManager.parser.lexer.peep('}')
            else:
                self.contextManager.parser.lexer.peep(';')
            return returnedToken

    def ignoreTheSemicolon(self): #Helper function for parseStatement
        while self.contextManager.parser.lexer.peep().id is ';':
            self.contextManager.parser.lexer.advance()