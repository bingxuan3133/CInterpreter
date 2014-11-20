from Context import *
from ContextManager import *

class FlowControlContext(Context):
    def addBlockOperator(self, id, bindingPower = 0 ):
        thisContext = self
        symClass = self.symbol(id, bindingPower)
        """
        def led(self):
            return self

        def nud(self):
            returnedToken = None
            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id == ';':
                nextToken = thisContext.contextManager.parser.lexer.advance()
            while nextToken.id != '}':
                returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
                self.data.append(returnedToken)
                if thisContext.contextManager.parser.lexer.peep().id is '}':
                    break
                nextToken = thisContext.contextManager.parser.lexer.advance()

            thisContext.contextManager.parser.lexer.advance()
            return self


        symClass.nud = nud
        symClass.led = led
        """
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
            thisContext.contextManager.parser.lexer.peep(')')
            contexts = thisContext.contextManager.popContexts()  # pop previously saved context
            thisContext.contextManager.setCurrentContexts(contexts)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parseStatements(self.bindingPower)
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
            thisContext.contextManager.parser.lexer.advance('(')
            thisContext.contextManager.pushContexts(thisContext.contextManager.currentContexts)
            newContext = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setContexts([newContext])
            returnedToken = thisContext.contextManager.parser.parse(bindingPower)
            self.data.append(returnedToken)

            """
            thisContext.contextManager.parser.lexer.advance()
            thisContext.contextManager.parser.lexer.peep(')')
            previousContext = thisContext.contextManager.popContexts()
            thisContext.contextManager.setContexts(previousContext)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(bindingPower)
            self.data.append(returnedToken)
            returnedToken = thisContext.contextManager.parser.lexer.peep()
            if (returnedToken.id == 'else'):
                thisContext.contextManager.parser.lexer.advance('{')
                returnedToken.data.append(thisContext.contextManager.parser.parse(bindingPower))
                self.data.append(returnedToken)
                """
            return self

        def led(self, leftToken):
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def parseStatements(self, bindingPower):
        nextToken = None
        head = self.contextManager.parser.lexer.peep('{')
        self.contextManager.parser.lexer.advance()
        self.ignoreTheSemicolon()
        nextToken = self.contextManager.parser.lexer.peep()
        while nextToken.id is not '}':
            returnedToken = self.contextManager.parser.parse(bindingPower)
            head.data.append(returnedToken)
            self.contextManager.parser.lexer.peep(';')
            self.ignoreTheSemicolon()
            nextToken = self.contextManager.parser.lexer.peep()
        return head

    def parseStatement(self, bindingPower):
        nextToken = None
        head = self.contextManager.parser.lexer.peep('{')
        self.contextManager.parser.lexer.advance()
        self.ignoreTheSemicolon()
        nextToken = self.contextManager.parser.lexer.peep()
        while nextToken.id is not '}':
            returnedToken = self.contextManager.parser.parse(bindingPower)
            head.data.append(returnedToken)
            self.contextManager.parser.lexer.peep(';')
            self.ignoreTheSemicolon()
            nextToken = self.contextManager.parser.lexer.peep()
        return head

    def ignoreTheSemicolon(self): #Helper function for parseStatement
        while self.contextManager.parser.lexer.peep().id is ';':
            self.contextManager.parser.lexer.advance()