#include "unity.h"
#include "VirtualMachine.h"
#include "CException.h"
#include <stdio.h>

void setUp(void)
{
}

void tearDown(void)
{
}

void test_explore(void) {
  initStack();
  Try {
    push(5);
    push(0x0A);
    push(5);
    push(0x0A);
    TEST_ASSERT_EQUAL(10, pop());
    TEST_ASSERT_EQUAL(5, pop());
    TEST_ASSERT_EQUAL(10, pop());
    TEST_ASSERT_EQUAL(5, pop());
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception");
  }
  
	printf("Stack Size: %d\n", sizeof(stack.stack));
  printStack();
}

void test_push_to_full_stack_should_throw_exception_STACK_OVERFLOW(void) {
  int i;

  initStack();
  Try {
    for(i = 0; i <= STACK_SIZE; i++) {
      push(0x0A);
    }
    TEST_FAIL_MESSAGE("Should throw exception STACK_OVERFLOW");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(STACK_OVERFLOW, exception);
  }

	printf("Stack Size: %d\n", sizeof(stack.stack));
  printStack();
}

void test_pop_from_empty_stack_should_throw_exception_STACK_UNDERFLOW(void) {
  int result;

  initStack();
  Try {
    result = pop();
    TEST_FAIL_MESSAGE("Should throw exception STACK_UNDERFLOW");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(STACK_UNDERFLOW, exception);
  }

	printf("Stack Size: %d\n", sizeof(stack.stack));
  printStack();
}