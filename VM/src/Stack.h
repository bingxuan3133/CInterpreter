#ifndef Stack_H
#define Stack_H

#define STACK_SIZE 10
#define isInteger(x) !((x) & 0x800000)  // Bit 24: 0  Indicates an integer
#define isObjectIndex(x) (x) & 0x800000 //         1  Indicates an objectIndex
#define isLocal(x) (x) & 0x400000       // Bit 23: 0  Indicates object in Local heap
#define isGlobal(x) (x) & 0x400000      //         1  Indicates object in Global heap

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

void initStack();
void push(int data);
int pop();
void printStack();

#endif // Stack_H