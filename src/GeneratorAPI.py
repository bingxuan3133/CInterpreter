__author__ = 'Jing'
from ByteCodeGenerator import *
from InformationInjector import *
class GeneratorAPI:
    def __init__(self, context, contextManager):
        self.byteCodeGenerator = ByteCodeGenerator(context, contextManager)
        self.informationInjector = InformationInjector()

    def enableVerboseByteCode(self):
        self.byteCodeGenerator.verboseByteCode =True

    def disableVerboseByteCode(self):
        self.byteCodeGenerator.verboseByteCode =False

    #An API adapter for connecting the others module
    def generateCode(self, tokens):
        Code = []
        self.byteCodeGenerator.byteCodeList = []
        self.byteCodeGenerator.initGeneration()
        if isinstance(tokens, list):
            for token in tokens:
                self.informationInjector.injectRegisterRequired(token)
                Code = token.generateByteCode()
                self.byteCodeGenerator.mapping.reset()
        else:
            self.informationInjector.injectRegisterRequired(tokens)
            Code = tokens.generateByteCode()
            self.byteCodeGenerator.mapping.reset()

        Code = self.byteCodeGenerator.injectPrologue(Code)
        return Code