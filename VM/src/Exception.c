#include "Exception.h"
#include <malloc.h>
#include <stdio.h>

Exception *exception;

Exception *createException(char *errorMessage, int errorCode) {
  Exception *e = malloc(sizeof(Exception));
  e->errMsg = errorMessage;
  e->errCode = errorCode;
  return e;
}

void freeException(Exception *e) {
  free(e);
}

void dumpException(Exception *e) {
  printf("%s (%d)\n", e->errMsg, e->errCode);
}