#ifndef Stack_H
#define Stack_H

#define STACK_SIZE 10
#define isInteger(x) !((x) & 0x800000)  // Bit 24: 0  Indicates an integer
#define isObjectIndex(x) (x) & 0x800000 //         1  Indicates an objectIndex
#define isLocal(x) (x) & 0x400000       // Bit 23: 0  Indicates object in Local heap
#define isGlobal(x) (x) & 0x400000      //         1  Indicates object in Global heap

typedef struct Stack Stack;
struct Stack {
  int *stack;
  int size;
  int *topOfStack;
};

typedef enum {
  STACK_UNDERFLOW,
  STACK_OVERFLOW
} Exception;

extern Exception exception;

Stack *createStack(int size);
void push(Stack *stack, int data);
int pop(Stack *stack);
void printStack(Stack *stack);

#endif // Stack_H