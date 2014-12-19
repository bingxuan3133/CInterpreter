__author__ = 'JingWen'


from distutils.core import setup, Extension

# define the extension module
print_Module = Extension('print_Module', sources=['test.c'])

# run the setup
setup(ext_modules=[print_Module])

print_Module.printSomeThing()