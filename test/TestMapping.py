__author__ = 'Jing'


import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

import unittest
import random
from Mapping import *



class TestMapping(unittest.TestCase):
    def setUp(self):
        self.mapping = Mapping()


    def test_Mapping_class_will_set_the_initial_value(self):
        self.assertEqual(self.mapping.registerFromLeft, 0)
        self.assertEqual(self.mapping.registerFromRight, self.mapping.MaxRegister-1)
        self.assertEqual(self.mapping.framePointerRegister, self.mapping.MaxRegister+1)
        self.assertEqual(self.mapping.registerLeft, self.mapping.MaxRegister)
        self.assertEqual(self.mapping.smallerRegisterUsed, 0)

    def test_getAFreeWorkingRegister_will_return_0(self):
        result = self.mapping.getAFreeWorkingRegister()
        self.assertEqual(result, 0)
        self.assertEqual(self.mapping.registerFromLeft, 1)
        self.assertEqual(self.mapping.registerLeft, self.mapping.MaxRegister-1)

    def test_getAFreeWorkingRegister_will_return_1_when_0_is_been_occupied(self):
        self.mapping.registerFromLeft = 1
        self.mapping.registerLeft -= 1
        result = self.mapping.getAFreeWorkingRegister()
        self.assertEqual(result, 1)
        self.assertEqual(self.mapping.registerFromLeft, 2)
        self.assertEqual(self.mapping.registerLeft, self.mapping.MaxRegister-2)

    def test_getAFreeWorkingRegister_will_return_the_next_number(self):
        testNumber = random.randint(0, self.mapping.MaxRegister-1)
        self.mapping.registerFromLeft = testNumber
        testNumberLeft = self.mapping.MaxRegister - testNumber
        self.mapping.registerLeft = testNumberLeft
        result = self.mapping.getAFreeWorkingRegister()
        self.assertEqual(result,testNumber)
        self.assertEqual(self.mapping.registerFromLeft, testNumber+1)
        self.assertEqual(self.mapping.registerLeft, testNumberLeft-1)

    def test_getAFreeWorkingRegister_will_throw_ReferenceError_exception(self):
        self.mapping.registerLeft = 0
        try:
            self.mapping.getAFreeWorkingRegister()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e :
            self.assertEqual("No register is free to allocate", e.msg)


    def test_getALargestWorkingRegister_will_return_the_largest_value(self):
        result = self.mapping.getALargestWorkingRegister()
        self.assertEqual(result, self.mapping.MaxRegister-1)
        self.assertEqual(self.mapping.registerFromRight, self.mapping.MaxRegister-2)
        self.assertEqual(self.mapping.registerLeft, self.mapping.MaxRegister -1)

    def test_getALargestWorkingRegister_will_return_the_4_value_when_registerFromRight_is_4(self):
        self.mapping.registerFromRight = 4
        self.mapping.registerLeft = 5
        result = self.mapping.getALargestWorkingRegister()
        self.assertEqual(result, 4)
        self.assertEqual(self.mapping.registerFromRight, 3)
        self.assertEqual(self.mapping.registerLeft, 4)

    def test_getALargestWorkingRegister_will_return_the_value_of_registerFromRight(self):
        testNumber =random.randint(0, self.mapping.MaxRegister-1)
        self.mapping.registerFromRight = testNumber
        testNumberLeft = self.mapping.MaxRegister-(testNumber)
        self.mapping.registerLeft = testNumberLeft
        result = self.mapping.getALargestWorkingRegister()
        self.assertEqual(result, testNumber)
        self.assertEqual(self.mapping.registerFromRight,testNumber-1)
        self.assertEqual(self.mapping.registerLeft, testNumberLeft-1)

    def test_getALargestWorkingRegister_will_return_the_value_of_registerFromRight_when_the_Maxregister_is_changed(self):
        self.mapping.MaxRegister = random.randint(0,99999999999)
        testNumber =random.randint(0, self.mapping.MaxRegister-1)
        self.mapping.registerFromRight = testNumber
        testNumberLeft = self.mapping.MaxRegister-(testNumber+1)
        self.mapping.registerLeft = testNumberLeft
        result = self.mapping.getALargestWorkingRegister()
        self.assertEqual(result, testNumber)
        self.assertEqual(self.mapping.registerFromRight,testNumber-1)
        self.assertEqual(self.mapping.registerLeft, testNumberLeft-1)

    def test_getALargestWorkingRegister_will_throw_ReferenceError_exception(self):
        self.mapping.registerLeft = 0
        try:
            self.mapping.getALargestWorkingRegister()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("No register is free to allocate",e.msg)

    def test_releaseALargestWorkingRegister_will_return_5_when_registerFromRight_is_4(self):
        self.mapping.registerFromRight = 4
        self.mapping.registerLeft = 5
        result = self.mapping.releaseALargestWorkingRegister()
        self.assertEqual(result, 5)
        self.assertEqual(self.mapping.registerFromRight, 5)
        self.assertEqual(self.mapping.registerLeft, 6)

    def test_releaseALargestWorkingRegister_will_return_the_value_that_less_than_registerFromRight_by_1(self):
        self.mapping.MaxRegister = random.randint(0, 999999999)
        testNumber =random.randint(0, self.mapping.MaxRegister-1)
        self.mapping.registerFromRight = testNumber
        testNumberLeft = self.mapping.MaxRegister-(testNumber+1)
        self.mapping.registerLeft = testNumberLeft
        result = self.mapping.releaseALargestWorkingRegister()
        self.assertEqual(result, testNumber+1)
        self.assertEqual(self.mapping.registerFromRight, testNumber+1)
        self.assertEqual(self.mapping.registerLeft, testNumberLeft+1)

    def test_releaseALargestWorkingRegister_will_throw_ReferenceError_exception(self):
        self.mapping.registerLeft = random.randint(0, 99999999)
        self.mapping.MaxRegister = self.mapping.registerLeft
        try:
            self.mapping.releaseALargestWorkingRegister()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("No register can be release",e.msg)


    def test_releaseAWorkingRegister_will_decrease_registerFromLeft_by_1(self):
        testNumber = random.randint(0, self.mapping.MaxRegister-1)
        self.mapping.registerFromLeft = testNumber
        testNumberLeft = self.mapping.MaxRegister - testNumber-1
        self.mapping.registerLeft = testNumberLeft
        result = self.mapping.releaseAWorkingRegister()
        self.assertEqual(result, testNumber-1)
        self.assertEqual(self.mapping.registerLeft, testNumberLeft+1)

    def test_releaseAWorkingRegister_will_throw_ReferenceError_exception(self):
        self.mapping.registerLeft = random.randint(0, 99999999)
        self.mapping.MaxRegister = self.mapping.registerLeft
        try:
            self.mapping.releaseAWorkingRegister()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("No register can be release",e.msg)


if __name__ == '__main__':
    unittest.main()
