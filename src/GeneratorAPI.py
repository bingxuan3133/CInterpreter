__author__ = 'Jing'
from ByteCodeGenerator import *
from InformationInjector import *
class GeneratorAPI:
    def __init__(self, context, contextManager):
        self.byteCodeGenerator = ByteCodeGenerator(context, contextManager)
        self.informationInjector = InformationInjector()


    #An API adapter for connecting the others module
    def generateCode(self, tokens):
        Code = None
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
        Code.append(0xffffffff)
        return Code
