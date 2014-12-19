__author__ = 'JingWen'

class RegisterAllocator:
    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        self.oracle = Oracle()