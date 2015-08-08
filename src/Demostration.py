__author__ = 'Jing'

from GeneratorAPI import *
from Parser import *
from VirtualMachine import *

manager = ContextManager()
context = Context(manager)
flowControlContext = FlowControlContext(manager)
defaultContext = DefaultContext(manager)
defaultContext.addKeyword('int')
declarationContext = DeclarationContext(manager)
expressionContext = ExpressionContext(manager)
generator = GeneratorAPI(context, manager)
byteCodeGenerator = ByteCodeGenerator(context, manager)
informationInjector = InformationInjector()

while(1):
    print("Please insert an equation to continue:")
    stopSymbol = ' '
    StringCode = ''
    print('>', end="")
    for statement in iter(input, stopSymbol):
        StringCode = StringCode + '\n' +statement
        print('>', end="")
    StingList = StringCode.split('\n')
    lexer = LexerStateMachine(StringCode, context)
    parser = Parser(lexer, manager)
    manager.setParser(parser)
    tokenList = []
    while lexer.currentToken.id != '(systemToken)':
        token = parser.parseStatements(0)
    byteCodes = generator.generateCode(token)

    vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')

    print (byteCodes)
    byteCodes.append(0xffffffff)  # to halt the VM

    for str in StingList:
        print(str)





