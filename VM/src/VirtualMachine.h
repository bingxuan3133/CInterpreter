#ifndef VirtualMachine_H
#define VirtualMachine_H

#define STACK_SIZE 10

typedef struct Stack Stack;
struct Stack {
  int stack[STACK_SIZE];
  int *topOfStack;
};

typedef enum {
  STACK_UNDERFLOW,
  STACK_OVERFLOW
} Exception;

extern Exception exception;

extern Stack stack;

void printStack();

#endif // VirtualMachine_H