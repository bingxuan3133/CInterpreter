__author__ = 'Jing'

from GeneratorAPI import *
from Parser import *
from VirtualMachine import *

contextManager = ContextManager()
context = Context(contextManager)
flowControlContext = FlowControlContext(contextManager)
defaultContext = DefaultContext(contextManager)
declarationContext = DeclarationContext(contextManager)
expressionContext = ExpressionContext(contextManager)
contexts = [expressionContext, declarationContext, flowControlContext, defaultContext]

contextManager.addContext('Default', defaultContext)
contextManager.addContext('Declaration', declarationContext)
contextManager.addContext('Expression', expressionContext)
contextManager.addContext('FlowControl', flowControlContext)
contextManager.setCurrentContexts(contexts)

generator = GeneratorAPI(context, contextManager)
byteCodeGenerator = ByteCodeGenerator(context, contextManager)
informationInjector = InformationInjector()
vm = VirtualMachine()
parser = Parser(None, contextManager)
contextManager.setParser(parser)
semanticChecker = SemanticChecker(parser.scopeBuilder)
semanticChecker.isEnable = True

print('Imba the Cinterpreter')
while(1):
    stopSymbol = ' '
    StringCode = ''
    print('> ', end="")
    for statement in iter(input, stopSymbol):
        StringCode = StringCode + '\n' +statement
        print('> ', end="")
    StringList = StringCode.split('\n')
    lexer = LexerStateMachine(StringCode, context)
    parser.lexer = lexer

    tokenList = []
    try:
        token = parser.parseStatements(0)
        byteCodes = generator.generateCode(token)
        vm.VMLoad(byteCodes)
          # to halt the VM
        vm.VMRun()
    except SyntaxError as e:
        print(e.msg)
