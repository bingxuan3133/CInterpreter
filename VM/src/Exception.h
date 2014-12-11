#ifndef EXCEPTION_H
#define EXCEPTION_H

typedef struct Exception Exception;
typedef struct Exception* ExceptionPtr;

typedef enum {
  INVALID_MEMORY_ACCESS
} ErrorCode;

struct Exception {
  char* errMsg;
  ErrorCode errCode;
};

extern Exception *exception;

#define CEXCEPTION_T    ExceptionPtr
#define CEXCEPTION_NONE   (ExceptionPtr)(0x5A5A5A5A)
#include "CException.h"

Exception *createException(char *errorMessage, int errorCode);
void freeException(Exception *e);
void dumpException(Exception *e);

#endif // EXCEPTION_H