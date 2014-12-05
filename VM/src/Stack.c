#include "Stack.h"
#include <stdio.h>
#include <malloc.h>

Exception exception;

Stack *createStack(int size) {
  Stack *stack = malloc(sizeof(Stack));
  stack->size = size;
  stack->stack = malloc(stack->size * sizeof(int));
  stack->topOfStack = &(stack->stack)[0];
  
  return stack;
}

void push(Stack *stack, int data) {
  if(stack->topOfStack >= &stack->stack[stack->size]) {
    Throw(STACK_OVERFLOW);
  } else {
    *stack->topOfStack = data;
    stack->topOfStack++;
  }
}

int pop(Stack *stack) {
  stack->topOfStack--;
  if(stack->topOfStack < &stack->stack[0])
    Throw(STACK_UNDERFLOW);
  else
    return *stack->topOfStack;
}

void printStack(Stack *stack) {
  int *stackPointer;
  for(stackPointer = stack->topOfStack - 1; stackPointer >= &stack->stack[0]; stackPointer--) {
    printf("%d\n", *stackPointer);
  }
}