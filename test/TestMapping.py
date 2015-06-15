__author__ = 'Jing'

import unittest
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
        result = self.mapping.getAFreeWorkingRegister()
        self.assertEqual(result, 1)
        self.assertEqual(self.mapping.registerFromLeft, 2)
        self.assertEqual(self.mapping.registerLeft, self.mapping.MaxRegister-2)

    def test_getAFreeWorkingRegister_will_return_the_next_number(self):
        self.mapping.registerFromLeft = 5
        result = self.mapping.getAFreeWorkingRegister()
        self.assertEqual(result,5)
        self.assertEqual(self.mapping.registerFromLeft, 6)

    def test_getALargestWorkingRegister_will_return_the_largest_value(self):
        result = self.mapping.getALargestWorkingRegister()
        self.assertEqual(result, self.mapping.MaxRegister-1)
        self.assertEqual(self.mapping.registerFromRight, self.mapping.MaxRegister-2)
if __name__ == '__main__':
    unittest.main()
