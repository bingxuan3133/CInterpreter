#include "unity.h"
#include "Instruction.h"
#include <stdio.h>
#include "Exception.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_explore_typecasting(void) {
  char a = 0xaa;
  unsigned char b = 0xaa;
  printf("%d\n", a);
  printf("%d\n", (int) a);
  printf("%d\n", (unsigned int) a);
  printf("%d\n", b);
  printf("%d\n", (int) b);
  printf("%d\n", (unsigned int) b);
  printf("%d\n", 0xaa);
  printf("%d\n", (int) 0xaa);
  printf("%d\n", (unsigned int) 0xaa);
}

void test_explore_addressing(void) {
  int value = 0x5A;   // 0x0028FE2C
  int value2 = 0xA5;  // 0x0028FE28
  int value3 = 0x12345678;  // 0x0028FE24
  printf("value: %p, value2: %p, value3: %p\n", &value, &value2, &value3);
  printf("0x0028FE2C: %x\n", *(int *)((char *)&value)); // 0000005A
  printf("0x0028FE2B: %x\n", *(int *)((char *)&value-1)); // 00005A00
  printf("0x0028FE2A: %x\n", *(int *)((char *)&value-2)); // 005A0000
  printf("0x0028FE29: %x\n", *(int *)((char *)&value-3)); // 5A000000
  printf("0x0028FE28: %x\n", *(int *)((char *)&value-4)); // A5

  printf("&value3+3: %x\n", *(int *)((char *)&value3+3)); // 12
  printf("&value3+2: %x\n", *(int *)((char *)&value3+2)); // 34
  printf("&value3+1: %x\n", *(int *)((char *)&value3+1)); // 56
  printf("&value3+0: %x\n", *(int *)((char *)&value3)); // 78

  printf("&value3+3: %x\n", *(char *)((char *)&value3+3)); // 12
  printf("&value3+2: %x\n", *(char *)((char *)&value3+2)); // 34
  printf("&value3+1: %x\n", *(char *)((char *)&value3+1)); // 56
  printf("&value3+0: %x\n", *(char *)((char *)&value3)); // 78
}

void test_getBits(void) {
  int result;

  result = getBits(0x240002, 23, 3); // getBits from bit 23 to bit 21
  TEST_ASSERT_EQUAL(1, result);
  result = getBits(0x240002, 20, 21); // getBits from bit 20 to bit 19
  TEST_ASSERT_EQUAL(0x40002, result);
}

void test_loadRegisterWithLiteral(void) {
  loadRegisterWithLiteral(ldrImm(0, 2)); // ldr r0, #2
  TEST_ASSERT_EQUAL(2, reg[0].data);
  loadRegisterWithLiteral(ldrImm(1, 2)); // ldr r1, #2
  TEST_ASSERT_EQUAL(2, reg[1].data);
  loadRegisterWithLiteral(ldrImm(2, 2)); // ldr r2, #2
  TEST_ASSERT_EQUAL(2, reg[2].data);
  loadRegisterWithLiteral(ldrImm(7, 2)); // ldr r7, #2
  TEST_ASSERT_EQUAL(2, reg[7].data);
}

void test_loadRegisterWithLiteral_should_keep_data_signed_value(void) {
  loadRegisterWithLiteral(ldrImm(0, -1)); // ldr r0, #-1
  TEST_ASSERT_EQUAL(-1, reg[0].data);
}

void test_loadRegisterFromMemory_should_load_register_with_value_in_reference(void) {
  int value = 0x5A;   // 0x0028FE2C
  int value2 = 0xA5;  // 0x0028FE28
  int value3 = 0x12345678;  // 0x0028FE24

  reg[0].data = 0;
  reg[1].data = (int)&value3;
  loadRegisterFromMemory(ldrMem(0, 1, 0)); // ldr r0, [r1 + 0]
  TEST_ASSERT_EQUAL_HEX(0x12345678, reg[0].data);
  loadRegisterFromMemory(ldrMem(0, 1, 4)); // ldr r0, [r1 + 4]
  TEST_ASSERT_EQUAL_HEX(0xA5, reg[0].data);
  loadRegisterFromMemory(ldrMem(0, 1, 8)); // ldr r0, [r1 + 8]
  TEST_ASSERT_EQUAL_HEX(0x5A, reg[0].data);
}

void test_storeRegisterIntoMemory_should_store_register_into_reference(void) {
  int value = 0;   // 4
  int value2 = 0;  // 0

  reg[1].data = (int)&value2;
  reg[0].data = 0xA5;
  storeRegisterIntoMemory(strMem(0, 1, 0)); // str r0, [r1 + 0]
  TEST_ASSERT_EQUAL_HEX(0xA5, value2);
  reg[0].data = 0x5A;
  storeRegisterIntoMemory(strMem(0, 1, 4)); // str r0, [r1 + 4]
  TEST_ASSERT_EQUAL_HEX(0x5A, value);
}

void test_moveRegister_r0_r1_should_move_r1_to_r0(void) {
  reg[0].data = 0;
  reg[1].data = 0xA5;
  moveRegister(movReg(0, 1)); // mov r0, r1
  TEST_ASSERT_EQUAL_HEX(0xA5, reg[0].data);
}

void test_loadRegisterFromMemorySafe_should_not_throw_an_exception_if_access_to_valid_memory(void) {
  int memory = 2;
  reg[7].data = (int)&memory;
  reg[7].base = (int)&memory;
  reg[7].limit = (int)(&memory)+0;
  Try {
    loadRegisterFromMemorySafe(ldrMemSafe(0, 7, 0)); // ldrs r0, [r7 + 0]
    TEST_ASSERT_EQUAL(2, reg[0].data);
    freeException;
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_loadRegisterFromMemorySafe_should_throw_an_exception_if_access_to_invalid_memory(void) {
  int memory = 2;
  reg[7].data = (int)&memory;
  reg[7].base = (int)&memory;
  reg[7].limit = (int)(&memory)+0;
  Try {
    loadRegisterFromMemorySafe(ldrMemSafe(0, 7, 1)); // ldrs r0, [r7 + 1]
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException;
  }
}

void test_storeRegisterIntoMemorySafe_should_not_throw_an_exception_if_access_to_valid_memory(void) {
  int memory = 0;
  reg[7].data = (int)&memory;
  reg[7].base = (int)&memory;
  reg[7].limit = (int)(&memory)+0;
  reg[0].data = 0x5A;
  Try {
    storeRegisterIntoMemorySafe(strMemSafe(0, 7, 0)); // strs r0, [r7 + 0]
    TEST_ASSERT_EQUAL(0x5A, reg[0].data);
    freeException;
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_storeRegisterIntoMemorySafe_should_throw_an_exception_if_access_to_invalid_memory(void) {
  int memory = 0;
  reg[7].data = (int)&memory;
  reg[7].base = (int)&memory;
  reg[7].limit = (int)(&memory)+0;
  reg[0].data = 0x5A;
  Try {
    storeRegisterIntoMemorySafe(ldrMemSafe(0, 7, 1)); // ldrs r0, [r7 + 1]
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException;
  }
}