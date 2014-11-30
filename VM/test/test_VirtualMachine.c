#include "unity.h"
#include "VirtualMachine.h"
#include "Stack.h"
#include <stdio.h>
#include "CException.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_getBits(void) {
  int result;
  
  result = getBits(0x240002, 23, 3);
  TEST_ASSERT_EQUAL(1, result);
  result = getBits(0x240002, 20, 21);
  TEST_ASSERT_EQUAL(0x40002, result);
}

void test_explore_loadRegisterLiteral(void) {
  loadRegisterLiteral(0x000002);
  TEST_ASSERT_EQUAL(2, reg[0]);
  loadRegisterLiteral(0x200002);
  TEST_ASSERT_EQUAL(2, reg[1]);
  loadRegisterLiteral(0x400002);
  TEST_ASSERT_EQUAL(2, reg[2]);
  loadRegisterLiteral(0xE00002);
  TEST_ASSERT_EQUAL(2, reg[7]);
}

void test_loadRegisterLiteral_should_keep_data_signed_value(void) {
  loadRegisterLiteral(0x1FFFFF);
  TEST_ASSERT_EQUAL(-1, reg[0]);
}

void xtest_add_should_add_top_2_integer_in_stack_and_push_back_the_result_into_the_stack(void) {
  int result;
  
  initStack();
  Try {
    push(5);
    push(0x0A);
    add();
    printf("Stack Size: %d\n", sizeof(stack.stack));
    printStack();
    
    TEST_ASSERT_EQUAL(15, result = pop());
    TEST_ASSERT_EQUAL(1, isInteger(result));
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception");
  }
  
}

void xtest_subtract_should_subtract_tos_integer_from_the_following_integer_and_push_back_the_result_into_stack(void) {
  int result;

  initStack();
  Try {
    push(5);
    push(0x0A);
    subtract();  
    printf("Stack Size: %d\n", sizeof(stack.stack));
    printStack();
  
    TEST_ASSERT_EQUAL(-5, *(stack.topOfStack-1));
    TEST_ASSERT_EQUAL(-5, result = pop());
    TEST_ASSERT_EQUAL(1, isInteger(result));
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception");
  }
}

void xtest_multiply_should_multiply_top_2_integer_in_stack_and_push_the_result_into_the_stack(void) {
  initStack();
  Try {
    push(5);
    push(0x0A);
    multiply();
    TEST_ASSERT_EQUAL(50, *(stack.topOfStack-1));
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception");
  }
  
	printf("Stack Size: %d\n", sizeof(stack.stack));
  printStack();
}

void xtest_divide_should_get_2nd_top_integer_to_divide_by_tos_integer_and_push_back_the_result_into_stack(void) {
  initStack();
  Try {
    push(0x0A);
    push(5);
    divide();
    TEST_ASSERT_EQUAL(2, *(stack.topOfStack-1));
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception");
  }
  
	printf("Stack Size: %d\n", sizeof(stack.stack));
  printStack();
}