#include "Stack.h"
#include <stdio.h>

Stack stack;
Exception exception;

void initStack() {
  stack.topOfStack = &(stack.stack)[0];
}

void push(int data) {
  if(stack.topOfStack >= &stack.stack[STACK_SIZE]) {
    Throw(STACK_OVERFLOW);
  } else {
    *stack.topOfStack = data;
    stack.topOfStack++;
  }
}

int pop() {
  stack.topOfStack--;
  if(stack.topOfStack < &stack.stack[0])
    Throw(STACK_UNDERFLOW);
  else
    return *stack.topOfStack;
}

void printStack() {
  int *stackPointer;
  for(stackPointer = stack.topOfStack - 1; stackPointer >= &stack.stack[0]; stackPointer--) {
    printf("%d\n", *stackPointer);
  }
}