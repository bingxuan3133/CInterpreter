#include "unity.h"
#include "Exception.h"
#include "VirtualMachine.h"
#include "Instruction.h"
#include "Disassembler.h"
#include "Print.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_Exception(void) {
  Exception *exception;
  Try {
    exception = createException("Error: this is a dummy exception", INVALID_MEMORY_ACCESS, 0xffffffff);
    Throw(exception);
  } Catch(exception) {
    dumpException(exception);
    freeException(exception);
  }
}