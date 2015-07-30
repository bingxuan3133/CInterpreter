#ifndef EXCEPTION_H
#define EXCEPTION_H

typedef struct Exception Exception;
typedef struct Exception* ExceptionPtr;

#include "VirtualMachine.h" // for getProgramCounter & Exception define

typedef enum {
  INVALID_BYTECODE,
  INVALID_MEMORY_ACCESS
} ErrorCode;

struct Exception {
  char* errMsg;       // error message
  ErrorCode errCode;  // error code
  unsigned int pc;    // program counter
  int bc;             // bytecode or instruction
};

extern char errBuffer[100];

#define CEXCEPTION_T    ExceptionPtr
#define CEXCEPTION_NONE   (ExceptionPtr)(0x5A5A5A5A)
#include "../vendor/ceedling/vendor/c_exception/lib/CException.h"

#define createException(errorMessage, errorCode, bytecode) _createException(errorMessage, errorCode, getProgramCounter(), bytecode)

Exception* _createException(char *errorMessage, int errorCode, unsigned int programCounter, int bytecode);
void freeException(Exception *e);
void dumpException(Exception *e);

#endif // EXCEPTION_H
