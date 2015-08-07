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
contexts = [declarationContext, expressionContext, defaultContext, flowControlContext]
expressionContext.addInfixOperator('=', 20)
expressionContext.addInfixOperator('==', 20)
expressionContext.addPrefixInfixOperator('+', 70)
expressionContext.addPrefixInfixOperator('-', 70)
expressionContext.addPrefixInfixOperator('*', 100)
expressionContext.addPrefixInfixOperator('/', 100)
expressionContext.addOperator(',', 0)
expressionContext.addOperator(';', 0)
expressionContext.addGroupOperator('(', 0)
expressionContext.addOperator(')', 0)
flowControlContext.addWhileControl('while', 0)
flowControlContext.addIfControl('if', 0)
flowControlContext.addOperator('else',0)
flowControlContext.addBlockOperator('{', 0)
flowControlContext.addOperator('}', 0)
declarationContext.addInt('int', 0)
declarationContext.addShort('short', 0)
declarationContext.addLong('long', 0)
declarationContext.addSignedAndUnsigned('signed', 0)
declarationContext.addSignedAndUnsigned('unsigned', 0)
manager.addContext('Default', defaultContext)
manager.addContext('Declaration', declarationContext)
manager.addContext('Expression', expressionContext)
manager.addContext('FlowControl', flowControlContext)
manager.setCurrentContexts(contexts)

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
    vm.dumpBytecodes(cbytecodes)





