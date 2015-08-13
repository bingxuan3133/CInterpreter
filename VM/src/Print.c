#include "Print.h"
#include <stdio.h>
#include <stdarg.h>

char *pythonBuffer = NULL;

int _printf(const char *format, ...) {
	va_list args;
	va_start(args, format);
	if(pythonBuffer)
		vsprintf(pythonBuffer, format, args);
	else
		vprintf(format, args);
	va_end(args);
}
