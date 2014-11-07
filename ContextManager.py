class ContextManager:
    def __init__(self):
        self.contexts = {}
        self.currentContexts = []
        self.contextsStack = []

    def addContext(self, contextName, context):
        if context not in self.contexts:
            self.contexts[contextName] = context

    def getContext(self, contextName):
        return self.contexts[contextName]

    def setContexts(self, contexts):
        self.currentContexts = contexts

    def popContexts(self):
        if self.contextsStack.__len__() is 0:
            raise RuntimeError
        return self.contextsStack.pop()

    def pushContexts(self, contexts):
        return self.contextsStack.append(contexts)