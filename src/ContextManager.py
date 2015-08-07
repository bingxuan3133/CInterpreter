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
        #try:
        return self.contexts[contextName]
        #except KeyError as keyError:
            #return None

    def setCurrentContexts(self, contexts):
        self.currentContexts = contexts

    def setCurrentContextsByName(self, *contextNames):
        if len(contextNames) > 1:
            self.currentContexts = []
            for contextName in contextNames:
                self.currentContexts.append(self.getContext(contextName))
        else:
            self.currentContexts = [self.getContext(contextNames[0])]

    def getCurrentContexts(self):
        return self.currentContexts

    def popContexts(self):
        if self.contextsStack.__len__() is 0:
            raise RuntimeError("No contexts is inside the stack. Please contact service person.")
        return self.contextsStack.pop()

    def pushContexts(self, contexts):
        self.contextsStack.append(contexts)

    def pushCurrentContexts(self):
        self.contextsStack.append(self.currentContexts)
