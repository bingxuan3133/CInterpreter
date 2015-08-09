__author__ = 'Jing'

from GeneratorAPI import *
from Parser import *
from VirtualMachine import *

manager = ContextManager()
context = Context(manager)
flowControlContext = FlowControlContext(manager)
defaultContext = DefaultContext(manager)
declarationContext = DeclarationContext(manager)
expressionContext = ExpressionContext(manager)
contexts = [expressionContext, declarationContext, flowControlContext, defaultContext]

manager.addContext('Default', defaultContext)
manager.addContext('Declaration', declarationContext)
manager.addContext('Expression', expressionContext)
manager.addContext('FlowControl', flowControlContext)
manager.setCurrentContexts(contexts)

generator = GeneratorAPI(context, manager)
byteCodeGenerator = ByteCodeGenerator(context, manager)
informationInjector = InformationInjector()
vm = VirtualMachine()

while(1):
    print("Please insert an equation to continue:")
    stopSymbol = ' '
    StringCode = ''
    print('>', end="")
    for statement in iter(input, stopSymbol):
        StringCode = StringCode + '\n' +statement
        print('>', end="")
    StringList = StringCode.split('\n')
    lexer = LexerStateMachine(StringCode, context)
    parser = Parser(lexer, manager)
    manager.setParser(parser)
    tokenList = []
    while lexer.currentToken.id != '(systemToken)':
        token = parser.parseStatements(0)
    byteCodes = generator.generateCode(token)

    byteCodes.append(0xffffffff)  # to halt the VM

    cbytecode = vm.convertToCArray(byteCodes)
    vm.dumpBytecodes(cbytecode)

    vm.disassembleBytecodes(cbytecode)

