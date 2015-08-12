#include "unity.h"
#include "Instruction.h"
#include "VirtualMachine.h"
#include "Exception.h"
#include "Disassembler.h"
#include <stdio.h>

#define merge2Registers(regHigh, regLow) (unsigned long long)reg[regHigh].data << 32 | (unsigned)reg[regLow].data

void setUp(void) {
  VMinit(10);
}

void tearDown(void) {

}

void test_getBits(void) {
  int result;

  result = getBits(0x240002, 23, 3); // getBits from bit 23 to bit 21
  TEST_ASSERT_EQUAL(1, result);
  result = getBits(0x240002, 20, 21); // getBits from bit 20 to bit 19
  TEST_ASSERT_EQUAL(0x40002, result);
}

void test_dumpRegister(void)  {
  reg[1].data = 0x5A;
  dumpRegister(dumpr(REG_1));
}

void test_loadRegisterWithImmediate(void) {
  loadRegisterWithImmediate(ldrImm(REG_0, 2)); // ldr r0, #2
  TEST_ASSERT_EQUAL(2, reg[0].data);
  loadRegisterWithImmediate(ldrImm(REG_1, 2)); // ldr REG_1, #2
  TEST_ASSERT_EQUAL(2, reg[1].data);
  loadRegisterWithImmediate(ldrImm(REG_2, 2)); // ldr r2, #2
  TEST_ASSERT_EQUAL(2, reg[2].data);
  loadRegisterWithImmediate(ldrImm(REG_7, 2)); // ldr r7, #2
  TEST_ASSERT_EQUAL(2, reg[7].data);
}

void test_loadRegisterWithImmediate_should_keep_data_signed_value(void) {
  loadRegisterWithImmediate(ldrImm(0, -1)); // ldr r0, #-1
  TEST_ASSERT_EQUAL(-1, reg[0].data);
}

void test_loadRegisterFromMemory_should_load_register_with_value_in_reference(void) {
  int heap[10] = {0};
  heap[0] = 0x12345678;
  heap[1] = 0x87654321;
  heap[2] = 0x12121212;
  heap[3] = 0x55665566;

  reg[0].data = 0;
  reg[1].data = (int)&heap[0];
  reg[2].data = (int)&heap[3];

  loadRegisterFromMemory(ldrMem(REG_0, REG_1, 0)); // ldr r0, [r1 + 0]
  TEST_ASSERT_EQUAL_HEX(0x12345678, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_1, 4)); // ldr r0, [r1 + 4]
  TEST_ASSERT_EQUAL_HEX(0x87654321, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_1, 8)); // ldr r0, [r1 + 8]
  TEST_ASSERT_EQUAL_HEX(0x12121212, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_2, 0)); // ldr r0, [r2 + 0]
  TEST_ASSERT_EQUAL_HEX(0x55665566, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_2, -4)); // ldr r0, [r2 + -4]
  TEST_ASSERT_EQUAL_HEX(0x12121212, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_2, -8)); // ldr r0, [r2 + -8]
  TEST_ASSERT_EQUAL_HEX(0x87654321, reg[0].data);
}

void test_storeRegisterIntoMemory_should_store_register_into_reference(void) {
  int heap[10] = {0};

  reg[1].data = (int)&heap[0];
  reg[2].data = (int)&heap[1];
  reg[0].data = 0xA5;
  storeRegisterIntoMemory(strMem(REG_0, REG_1, 0)); // str r0, [r1 + 0]
  TEST_ASSERT_EQUAL_HEX(0xA5, heap[0]);
  reg[0].data = 0x20;
  storeRegisterIntoMemory(strMem(REG_0, REG_1, 4)); // str r0, [r1 + 4]
  TEST_ASSERT_EQUAL_HEX(0x20, heap[1]);
  storeRegisterIntoMemory(strMem(REG_0, REG_2, -4)); // str r0, [r2 + #-4]
  TEST_ASSERT_EQUAL_HEX(0x20, heap[0]);
}

void test_moveRegister_r0_REG_1_should_move_REG_1_to_r0(void) {
  reg[0].data = 0;
  reg[1].data = 0xA5;
  moveRegister(movReg(REG_0, DATA, REG_1, NOP, NOP)); // mov r0.data, r1, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0xA5, reg[0].data);
}

void test_moveRegister_r7_data_or_base_or_limit_r0_should_move_r0_to_r7_data_or_base_or_limit_correctly(void) {
  reg[0].data = 0x01020304;
  moveRegister(movReg(REG_7, DATA, REG_0, NOP, NOP)); // mov r7.data, r0, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0x01020304, reg[7].data);
  moveRegister(movReg(REG_7, BASE, REG_0, NOP, NOP)); // mov r7.base, r0, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0x01020304, reg[7].data);
  moveRegister(movReg(REG_7, LIMIT, REG_0, NOP, NOP)); // mov r7.limit, r0, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0x01020304, reg[7].data);
}

void test_moveRegister_r0_given_0xFF07FF07_should_return_correct_values_for_each_shift_rotate_operations(void) {
  reg[0].data = 0;
  reg[1].data = 0xFF07FF07;
  moveRegister(movReg(REG_0, DATA, REG_1, NOP, NOP)); // mov r0.data, r1, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0xFF07FF07, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, LSL, 8)); // mov r0.data, r1, LSL, #8
  TEST_ASSERT_EQUAL_HEX(0x07FF0700, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, LSR, 8)); // mov r0.data, r1, LSR, #8
  TEST_ASSERT_EQUAL_HEX(0x00FF07FF, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, ASR, 8)); // mov r0.data, r1, ASR, #8
  TEST_ASSERT_EQUAL_HEX(0xFFFF07FF, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, RR, 8));  // mov r0.data, r1, RR, #8
  TEST_ASSERT_EQUAL_HEX(0x07FF07FF, reg[0].data);
}

void test_loadRegisterFromMemorySafe_should_not_throw_an_exception_if_access_to_valid_memory(void) {
  int heap[10] = {0};
  Exception *exception;

  heap[9] = 2;
  reg[7].data = (int)&heap[0];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  Try {
    loadRegisterFromMemorySafe(ldrMemSafe(REG_0, REG_7, 36)); // ldrs r0, [r7 + 36]
    TEST_ASSERT_EQUAL(2, reg[0].data);
    freeException(exception);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_loadRegisterFromMemorySafe_should_throw_an_exception_if_access_to_invalid_memory(void) {
  int heap[10] = {0};
  Exception *exception;

  heap[0] = 2;
  heap[1] = 4;
  heap[2] = 6;
  reg[7].data = (int)&heap[0];  // 0
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  Try {
    loadRegisterFromMemorySafe(ldrMemSafe(REG_0, REG_7, 37)); // ldrs r0, [r7 + 37]
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_storeRegisterIntoMemorySafe_should_not_throw_an_exception_if_access_to_valid_memory(void) {
  int heap[10] = {0};
  Exception *exception;

  reg[7].data = (int)&heap[0];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 0x5A;
  Try {
    storeRegisterIntoMemorySafe(strMemSafe(REG_0, REG_7, 0)); // strs r0, [r7 + 0]
    TEST_ASSERT_EQUAL(0x5A, heap[0]);
    freeException(exception);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_storeRegisterIntoMemorySafe_should_throw_an_exception_if_access_to_invalid_memory(void) {
  int memory = 0;
  Exception *exception;

  reg[7].data = (int)&memory;
  reg[7].base = (int)&memory;
  reg[7].limit = 40;
  reg[0].data = 0x5A;
  Try {
    storeRegisterIntoMemorySafe(ldrMemSafe(REG_0, REG_7, 37)); // strs r0, [r7 + 37]
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_loadMultipleRegistersFromMemory_should_load_register_with_data_in_memory(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};

  reg[7].data = (int)&heap[5];
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;

  loadMultipleRegistersFromMemory(ldm(REG_7, R1|R2|R3, INC, NO_UPDATE)); // ldmi r7, [r1, r2, r3]
  TEST_ASSERT_EQUAL(-100, reg[1].data);
  TEST_ASSERT_EQUAL(-50, reg[2].data);
  TEST_ASSERT_EQUAL(-30, reg[3].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);

  loadMultipleRegistersFromMemory(ldm(REG_7, R4|R5|R6, DEC, NO_UPDATE)); // ldmd r7, [r4, r5, r6]
  TEST_ASSERT_EQUAL(-100, reg[4].data);
  TEST_ASSERT_EQUAL(-20, reg[5].data);
  TEST_ASSERT_EQUAL(-10, reg[6].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);

  loadMultipleRegistersFromMemory(ldm(REG_7, R4|R5|R6, INC, UPDATE)); // ldmi r7!, [r4, r5, r6]  r7->heap[8]
  TEST_ASSERT_EQUAL(-100, reg[4].data);
  TEST_ASSERT_EQUAL(-50, reg[5].data);
  TEST_ASSERT_EQUAL(-30, reg[6].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[8], reg[7].data);

  loadMultipleRegistersFromMemory(ldm(REG_7, R0|R1|R2|R3|R4|R5|R6, DEC, UPDATE)); // ldmd r7!, [r1 - r6]
  TEST_ASSERT_EQUAL(20, reg[0].data);
  TEST_ASSERT_EQUAL(-30, reg[1].data);
  TEST_ASSERT_EQUAL(-50, reg[2].data);
  TEST_ASSERT_EQUAL(-100, reg[3].data);
  TEST_ASSERT_EQUAL(-20, reg[4].data);
  TEST_ASSERT_EQUAL(-10, reg[5].data);
  TEST_ASSERT_EQUAL(100, reg[6].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[1], reg[7].data);
}

void test_loadMultipleRegistersFromMemory_load_stack_pointer_address(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};

  reg[7].data = (int)&heap[5];
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;

  loadMultipleRegistersFromMemory(ldm(REG_7, R7, INC, UPDATE)); // ldmi r7!, [r7]  r7->heap[6]
  TEST_ASSERT_EQUAL_HEX((int)&heap[6], reg[7].data);

  loadMultipleRegistersFromMemory(ldm(REG_7, R7, INC, NO_UPDATE)); // ldmi r7, [r7]
  TEST_ASSERT_EQUAL(-50, reg[7].data);                             // Will have serious problem when used as stack pointer next time
}

void test_storeMultipleRegistersIntoMemory_should_load_register_with_data_in_memory(void) {
  int heap[10] = {0};

  reg[7].data = (int)&heap[5];
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;

  storeMultipleRegistersIntoMemory(stm(REG_7, R0|R1|R2, INC, NO_UPDATE)); // stmi r7, [r0, r1, r2]
  TEST_ASSERT_EQUAL(10, heap[5]);
  TEST_ASSERT_EQUAL(-20, heap[6]);
  TEST_ASSERT_EQUAL(30, heap[7]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);

  storeMultipleRegistersIntoMemory(stm(REG_7, R3|R4|R5|R6, DEC, NO_UPDATE)); // stmd r7, [r3, r4, r5, r6]
  TEST_ASSERT_EQUAL(-40, heap[5]);
  TEST_ASSERT_EQUAL(50, heap[4]);
  TEST_ASSERT_EQUAL(-60, heap[3]);
  TEST_ASSERT_EQUAL(70, heap[2]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);


  storeMultipleRegistersIntoMemory(stm(REG_7, R0|R1|R2, INC, UPDATE)); // stmi r7!, [r0, r1, r2]
  TEST_ASSERT_EQUAL(10, heap[5]);
  TEST_ASSERT_EQUAL(-20, heap[6]);
  TEST_ASSERT_EQUAL(30, heap[7]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[8], reg[7].data);

  storeMultipleRegistersIntoMemory(stm(REG_7, R3|R4|R5|R6, DEC, UPDATE)); // stmd r7!, [r3, r4, r5, r6]
  TEST_ASSERT_EQUAL(-40, heap[8]);
  TEST_ASSERT_EQUAL(50, heap[7]);
  TEST_ASSERT_EQUAL(-60, heap[6]);
  TEST_ASSERT_EQUAL(70, heap[5]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[4], reg[7].data);
}

void test_storeMultipleRegistersIntoMemory_store_stack_pointer_address(void) {
  int heap[10] = {0};

  reg[7].data = (int)&heap[5];
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;

  storeMultipleRegistersIntoMemory(stm(REG_7, R7, INC, UPDATE)); // stmi r7!, [r7]  r7->heap[6]
  TEST_ASSERT_EQUAL_HEX((int)&heap[6], reg[7].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], heap[5]);

  storeMultipleRegistersIntoMemory(stm(REG_7, R7, INC, NO_UPDATE)); // stmi r7, [r7]
  TEST_ASSERT_EQUAL_HEX((int)&heap[6], reg[7].data);
}

void test_loadMultipleRegistersFromMemorySafe_should_not_throw_exception_when_memory_is_valid(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  Exception *exception;

  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;

  Try {
    loadMultipleRegistersFromMemorySafe(ldms(REG_7, R1|R2|R3, INC, NO_UPDATE));
    TEST_ASSERT_EQUAL(-100, reg[1].data);
    TEST_ASSERT_EQUAL(-50, reg[2].data);
    TEST_ASSERT_EQUAL(-30, reg[3].data);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_loadMultipleRegistersFromMemorySafe_should_throw_exception_when_stack_pointer_increases_and_exceed_limit_of_valid_memory(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  Exception *exception;

  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;

  Try {
    loadMultipleRegistersFromMemorySafe(ldms(REG_7, R0|R1|R2|R3|R4|R5|R6, INC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(-100, reg[0].data);
    TEST_ASSERT_EQUAL(-50, reg[1].data);
    TEST_ASSERT_EQUAL(-30, reg[2].data);
    TEST_ASSERT_EQUAL(20, reg[3].data);
    TEST_ASSERT_EQUAL(70, reg[4].data);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);

    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_loadMultipleRegistersFromMemorySafe_should_throw_exception_when_stack_pointer_decreases_and_exceed_base_of_valid_memory(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  Exception *exception;

  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;

  Try {
    loadMultipleRegistersFromMemorySafe(ldms(REG_7, R0|R1|R2|R3|R4|R5|R6, DEC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(-100, reg[0].data);
    TEST_ASSERT_EQUAL(-20, reg[1].data);
    TEST_ASSERT_EQUAL(-10, reg[2].data);
    TEST_ASSERT_EQUAL(100, reg[3].data);
    TEST_ASSERT_EQUAL(50, reg[4].data);
    TEST_ASSERT_EQUAL(10, reg[5].data);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);

    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_storeMultipleRegistersIntoMemorySafe_should_not_throw_exception_when_memory_is_valid(void) {
  int heap[10] = {0};
  Exception *exception;

  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;

  Try {
    storeMultipleRegistersIntoMemorySafe(stms(REG_7, R1|R2|R3, INC, NO_UPDATE));
    TEST_ASSERT_EQUAL(-20, heap[5]);
    TEST_ASSERT_EQUAL(30, heap[6]);
    TEST_ASSERT_EQUAL(-40, heap[7]);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_storeMultipleRegistersIntoMemorySafe_should_throw_exception_when_stack_pointer_increases_and_exceed_limit_of_valid_memory(void) {
  int heap[10] = {0};
  Exception *exception;

  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;

  Try {
    storeMultipleRegistersIntoMemorySafe(stms(REG_7, R0|R1|R2|R3|R4|R5|R6, INC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(10, heap[5]);
    TEST_ASSERT_EQUAL(-20, heap[6]);
    TEST_ASSERT_EQUAL(30, heap[7]);
    TEST_ASSERT_EQUAL(-40, heap[8]);
    TEST_ASSERT_EQUAL(50, heap[9]);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);

    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_storeMultipleRegistersIntoMemorySafe_should_throw_exception_when_stack_pointer_decreases_and_exceed_base_of_valid_memory(void) {
  int heap[10] = {0};
  Exception *exception;

  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;

  Try {
    storeMultipleRegistersIntoMemorySafe(stms(REG_7, R0|R1|R2|R3|R4|R5|R6, DEC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(10, heap[5]);
    TEST_ASSERT_EQUAL(-20, heap[4]);
    TEST_ASSERT_EQUAL(30, heap[3]);
    TEST_ASSERT_EQUAL(-40, heap[2]);
    TEST_ASSERT_EQUAL(50, heap[1]);
    TEST_ASSERT_EQUAL(-60, heap[0]);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);

    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_addRegisters_should_add_2_registers(void) {
  reg[0].data = 10;
  reg[1].data = -20;
  addRegisters(add(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL(-10, reg[0].data);
}

void test_subtractRegisters_should_subtract_reg1_from_reg0(void) {
  reg[0].data = -10;
  reg[1].data = 20;
  subtractRegisters(sub(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL(-30, reg[0].data);
}

// void test_subtractRegisterWithImmediate_should_subtract_reg_from_imm(void) {
  // reg[7].data = 0;
  // subtractRegisterWithImmediate(subImm(REG_7, 4));
  
  // TEST_ASSERT_EQUAL(-4, reg[7].data);
// }

void test_multiplyRegisters_should_multiply_2_registers(void) {
  reg[0].data = 10;
  reg[1].data = -20;
  multiplyRegisters(mul(REG_1, REG_0, REG_0, REG_1));
  unsigned long long result = merge2Registers(REG_1, REG_0);

  TEST_ASSERT_EQUAL(-200, result);
}

void test_multiplyRegisters_should_multiply_2_registers_without_overflow_issue(void) {
  reg[0].data = 100000;
  reg[1].data = -100000;
  multiplyRegisters(mul(REG_1, REG_0, REG_0, REG_1));
  unsigned long long result = merge2Registers(REG_1, REG_0);

  TEST_ASSERT_EQUAL_INT64(-10000000000, result);
}

void test_divideRegisters_should_divide_reg1_from_reg0_to_get_quotient_and_remainder(void) {
  reg[0].data = 20;
  reg[1].data = -10;
  divideRegisters(_div(REG_0, REG_1, REG_0, REG_1));
  TEST_ASSERT_EQUAL(-2, reg[0].data); // quotient
  TEST_ASSERT_EQUAL(0, reg[1].data);  // remainder
}

void test_andRegisters_should_bitwise_and_2_registers(void) {
  reg[0].data = 0x00ff00ff;
  reg[1].data = 0x0ff00ff0;
  andRegisters(and(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL_HEX(0x00f000f0, reg[0].data);
}

void test_orRegisters_should_bitwise_or_2_registers(void) {
  reg[0].data = 0x00ff00ff;
  reg[1].data = 0x0ff00ff0;
  orRegisters(or(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL_HEX(0x0fff0fff, reg[0].data);
}

void test_xorRegisters_should_bitwise_xor_2_registers(void) {
  reg[0].data = 0x00ff00ff;
  reg[1].data = 0x0ff00ff0;
  xorRegisters(xor(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL_HEX(0x0f0f0f0f, reg[0].data);
}

void test_branch(void) {
  moveProgramCounter(0x40);
  branch(bra(-0x10));
  TEST_ASSERT_EQUAL_HEX(0x30, getProgramCounter());
}

void test_branchIfTrue(void) {
  moveProgramCounter(0x40);
  branchIfTrue(bit(-0x10));
  TEST_ASSERT_EQUAL_HEX(0x40, getProgramCounter());
  setStatusBit('B');
  branchIfTrue(bit(-0x10));
  TEST_ASSERT_EQUAL_HEX(0x30, getProgramCounter());
}

void test_fldrImm(void) {
  int bytecode[4] = {fldrImm(1), 255, 5050, 0};
  loadVMBytecode(bytecode);
  floadRegisterWithImmediate(fldrImm(1));
  TEST_ASSERT_EQUAL_HEX64(255| (((long long int)5050)<<32), dReg[1].data);
  TEST_ASSERT_EQUAL_HEX(0x2, getProgramCounter());
}

void test_fldr(void) {
  int bytecode[4] = {565, 7272, 5050, 1};
  reg[7].data = (int)&bytecode[0];
  floadRegisterFromMemory(fldr(1, REG_7, 0));
  TEST_ASSERT_EQUAL_HEX64(565|(((long long int)7272)<<32), dReg[1].data);
  floadRegisterFromMemory(fldr(1, REG_7, 4));
  TEST_ASSERT_EQUAL_HEX64(7272|(((long long int)5050)<<32), dReg[1].data);
  floadRegisterFromMemory(fldr(1, REG_7, 8));
  TEST_ASSERT_EQUAL_HEX64(5050|(((long long int)1)<<32), dReg[1].data);
}

void test_fstr(void) {
  int bytecode[4] = {0, 0, 0, 0};
  reg[7].data = (int)&bytecode[0];
  dReg[1].data = 0x12340000005A;
  fstoreRegisterIntoMemory(fstr(1, REG_7, 0));
  TEST_ASSERT_EQUAL_HEX(0x005A, bytecode[0]);
  TEST_ASSERT_EQUAL_HEX(0x1234, bytecode[1]);
  reg[7].data = (int)&bytecode[2];
  dReg[1].data = 0x5A5A00004321;
  fstoreRegisterIntoMemory(fstr(1, REG_7, 0));
  TEST_ASSERT_EQUAL_HEX(0x4321, bytecode[2]);
  TEST_ASSERT_EQUAL_HEX(0x5A5A, bytecode[3]);
  reg[7].data = (int)&bytecode[1];
  dReg[1].data = 0xAAAA0000BBBB;
  fstoreRegisterIntoMemory(fstr(1, REG_7, 0));
  TEST_ASSERT_EQUAL_HEX(0xBBBB, bytecode[1]);
  TEST_ASSERT_EQUAL_HEX(0xAAAA, bytecode[2]);
}
