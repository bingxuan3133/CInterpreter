#include <Python.h>
#include "test.h"
#include <Python.h>
#include <stdio.h>
static PyObject* printSomeThing(PyObject *self, PyObject *args)
{
	int A=10;
	int B=50;
	printf("You successfully print!\n");
	return Py_BuildValue("f", A+B);
}



/*  define functions in module */
static PyMethodDef CosMethods[] =
{
     {"printSomeThing", printSomeThing, METH_VARARGS, "get a number"},
     {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC

initcos_module(void)
{
     (void) Py_InitModule("cos_module", CosMethods);
}
