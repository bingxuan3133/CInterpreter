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
    byteCodesSize = len(byteCodes)
    cByteCodes_t = c_uint * byteCodesSize
    cByteCodes = cByteCodes_t(*byteCodes)

    vmdll.restype = POINTER(C_Exception)

    exception = vmdll._VMStep(cByteCodes)
    vmdll._VMRun(cByteCodes)





