#include "unity.h"
#include "VirtualMachine.h"
#include "Instruction.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_explore_function_pointer_array(void) {
  instruction[1](0x000002);
  TEST_ASSERT_EQUAL(2, reg[0].data);
}