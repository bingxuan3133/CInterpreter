#include "unity.h"
#include "VirtualMachine.h"
#include "Instruction.h"
#include "Disassembler.h"
#include "Exception.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_explore_function_pointer_array(void) {
  instruction[LDR_IMM](ldrImm(0, 2));
  TEST_ASSERT_EQUAL(2, reg[0].data);
}

void test_read_binary_file(void) {
  FILE *myfile;
  myfile = fopen("myFirstByteCode", "r+");
  int bytecodes[10] = {0};
  char strBuffer[200] = {0};
  bytecodes[0] = getBytecode(myfile);
  bytecodes[1] = getBytecode(myfile);
  bytecodes[2] = getBytecode(myfile);
  bytecodes[3] = 0xffffffff;
  
  disassembleBytecodes(&strBuffer[0], &bytecodes[0]);
  printf("%s\n", strBuffer);
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
}