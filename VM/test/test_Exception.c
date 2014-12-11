#include "unity.h"
#include "Exception.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_Exception(void) {
  Try {
    exception = createException("Error: this is a dummy exception", INVALID_MEMORY_ACCESS);
    Throw(exception);
  } Catch(exception) {
    dumpException(exception);
    freeException(exception);
  }
}