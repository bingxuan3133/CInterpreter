#include "Exception.h"
#include <malloc.h>
#include <stdio.h>

Exception *_createException(char *errorMessage, int errorCode, unsigned int programCounter, int bytecode) {
  Exception *e = malloc(sizeof(Exception));
  e->errCode = errorCode;
  e->errMsg = errorMessage;
  e->pc = programCounter;
  e->bc = bytecode;
  return e;
}

void freeException(Exception *e) {
  free(e);
}

void dumpException(Exception *e) {
  printf("%s (%d)\n", e->errMsg, e->errCode);
}