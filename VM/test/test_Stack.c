#include "unity.h"
#include "Stack.h"
#include <stdio.h>
#include "CException.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_explore_stack(void) {
  Stack *stack = createStack(10);
  Try {
    push(stack, 5);
    push(stack, 0x0A);
    push(stack, 5);
    push(stack, 0x0A);
    TEST_ASSERT_EQUAL(10, pop(stack));
    TEST_ASSERT_EQUAL(5, pop(stack));
    TEST_ASSERT_EQUAL(10, pop(stack));
    TEST_ASSERT_EQUAL(5, pop(stack));
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception");
  }
  
	printf("Stack Size: %d\n", stack->size);
  printStack(stack);
}

void test_createStack_should_create_a_stack_properly(void) {
  Stack *stack = createStack(10);
  TEST_ASSERT_EQUAL(10, stack->size);
  TEST_ASSERT_EQUAL_PTR(stack->stack, stack->topOfStack);
}

void test_push_to_full_stack_should_throw_exception_STACK_OVERFLOW(void) {
  int i;
  Stack *stack = createStack(10);
  Try {
    for(i = 0; i <= STACK_SIZE; i++) {
      push(stack, 0x0A);
    }
    TEST_FAIL_MESSAGE("Should throw exception STACK_OVERFLOW");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(STACK_OVERFLOW, exception);
  }

	printf("Stack Size: %d\n", stack->size);
  printStack(stack);
}

void test_pop_from_empty_stack_should_throw_exception_STACK_UNDERFLOW(void) {
  int result;
  Stack *stack = createStack(10);
  Try {
    result = pop(stack);
    TEST_FAIL_MESSAGE("Should throw exception STACK_UNDERFLOW");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(STACK_UNDERFLOW, exception);
  }

	printf("Stack Size: %d\n", stack->size);
  printStack(stack);
}