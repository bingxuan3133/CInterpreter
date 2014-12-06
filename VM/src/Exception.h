#ifndef EXCEPTION_H
#define EXCEPTION_H

typedef struct Exception Exception;

struct Exception {
  char* msgString;
};

#define CEXCEPTION_T    Exception
#include "CException.h"

#endif // EXCEPTION_H