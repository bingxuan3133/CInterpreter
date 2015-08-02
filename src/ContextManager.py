class ContextManager:
    def __init__(self):
        self.contexts = {}
        self.currentContexts = []
        self.contextsStack = []
        self.allContexts = []

    def setParser(self, parser):
        self.parser = parser

    def addContext(self, contextName, context):
        if context not in self.contexts:
            self.contexts[contextName] = context
            self.allContexts.append(context)

    def getContext(self, contextName):
        return self.contexts[contextName]

    def setCurrentContexts(self, contexts):
        self.currentContexts = contexts

    def getCurrentContexts(self):
        return self.currentContexts

    def popContexts(self):
        if self.contextsStack.__len__() is 0:
            raise RuntimeError("No contexts is inside the stack.Please contact service person.")
        return self.contextsStack.pop()

    def pushContexts(self, contexts):
        return self.contextsStack.append(contexts)