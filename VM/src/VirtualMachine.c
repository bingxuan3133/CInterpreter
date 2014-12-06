#include "VirtualMachine.h"

void (*instruction[256])(int)  = {[0x00] = loadRegisterWithLiteral,
                                  [0x01] = loadRegisterWithReference
                                  }; //