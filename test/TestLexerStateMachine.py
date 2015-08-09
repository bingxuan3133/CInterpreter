__author__ = 'Jing'
import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

import unittest
from LexerStateMachine import *
from Context import *
from ContextManager import *

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.manager.setCurrentContexts([self.context])
        self.context.addOperator('(')
        self.context.addOperator(')')
        self.context.addOperator('.')
        self.context.addOperator('+')
        self.context.addOperator('++')
        self.context.addOperator('-')
        self.context.addOperator('*')
        self.context.addOperator('=')
        self.context.addOperator('==')
        self.context.addOperator('&&')

    def testAdvance(self):
        lexer = LexerStateMachine(""" hi krizz
                          987 456 """, self.context)
        self.assertEqual(lexer.peep().data[0], 'hi')
        self.assertEqual(lexer.advance().data[0], 'krizz')
        self.assertEqual(lexer.advance().data[0], 987)
        self.assertEqual(lexer.advance().data[0], 456)

    def test_peep_should_raise_error_when_the_returned_symbol_is_not_equal_to_the_expected_symbol(self):
        lexer = LexerStateMachine('(', self.context)
        self.assertRaises(SyntaxError, lexer.peep, '*')

    def test_peep_should_not_raise_error_when_the_returned_symbol_is_equal_to_the_expected_symbol(self):
        lexer = LexerStateMachine('(', self.context)
        lexer.peep()
        #self.assertRaises(None, lexer.peep, '(')

    def test_peep_should_not_raise_error_when_the_expected_symbol_is_none(self):
        lexer = LexerStateMachine('(', self.context)
        lexer.peep()

    def test_advance_should_raise_error_when_the_returned_token_is_not_equal_to_the_expected_token(self):
        lexer = LexerStateMachine('( )', self.context)
        self.assertRaises(SyntaxError, lexer.advance, '*')

    def test_advance_should_not_raise_error_when_the_returned_token_is_equal_to_the_expected_token(self):

        lexer = LexerStateMachine('( )', self.context)
        lexer.advance()
        #self.assertRaises(None, lexer.advance, ')')

    def test_advance_should_not_raise_error_when_expected_symbol_is_none(self):
        lexer = LexerStateMachine('( )', self.context)
        lexer.advance()

    def test_the_lexer_will_contain_the_first_token_in_the_class(self):
        lexer = LexerStateMachine('12', self.context)
        testToken = lexer.currentToken
        self.assertEqual(testToken.data[0], 12)
        self.assertEqual(testToken.id, '(literal)')

    def test_peep_will_return_the_currentToken_inside_the_lexer(self):
        lexer = LexerStateMachine('151915354', self.context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 151915354)
        self.assertEqual(testToken.id, '(literal)')
        testToken1 = lexer.peep()
        self.assertEqual(testToken1.data[0], 151915354)
        self.assertEqual(testToken1.id, '(literal)')

    def test_the_lexer_will_make_a_token_for_the_number_with_e_and_E(self):
        lexer = LexerStateMachine('12E10', self.context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0],120000000000)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_get_the_second_word_in_the_string(self):
        lexer = LexerStateMachine('Price 12E10', self.context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 'Price')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],120000000000)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_get_the_number_with_eE_power_to_positive(self):
        lexer = LexerStateMachine('Price 12E+10', self.context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 'Price')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],120000000000)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_get_the_number_with_eE_power_to_negative(self):
        lexer = LexerStateMachine('Price 12E-10', self.context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 'Price')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 1.2e-09)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_throw_exception_for_two_notation_is_included_in_the_e_floating_point(self):
        lexer = LexerStateMachine('Price 12E--10', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][11]:Unexpected symbol \"-\" been found after -"+'\n'+
            'Price 12E--10'+'\n'+
            '          ^', e.msg)

    def test_advance_will_throw_exception_for_plus_plus_appear_inside_the_floating_point_e(self):
        lexer = LexerStateMachine('Price 12E++10', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][11]:Unexpected symbol \"+\" been found after +"+'\n'+
            'Price 12E++10'+'\n'+
            '          ^', e.msg)

    def test_advance_will_throw_exception_for_the_error_That_occurred_after_the_first_line(self):
        lexer = LexerStateMachine("Price"+"\n"+
                                  "12E++10", self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[2][5]:Unexpected symbol \"+\" been found after +"+'\n'+
            '12E++10'+'\n'+
            '    ^', e.msg)

        lexer = LexerStateMachine("Price"+"\n"+
                                "IsRising"+"\n"+
                                  "12E++10", self.context)
        try:
            lexer.advance()
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[3][5]:Unexpected symbol \"+\" been found after +"+'\n'+
            '12E++10'+'\n'+
            '    ^', e.msg)

    def test_advance_will_throw_exception_for_invalid_number_after_minus_sign(self):
        lexer = LexerStateMachine('Price 12E-/10', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][11]:Unexpected symbol \"/\" been found after -"+'\n'+
            'Price 12E-/10'+'\n'+
            '          ^', e.msg)


    def test_advance_will_throw_exception_for_unknown_symbol_inside_the_floating_point_e(self):
        lexer = LexerStateMachine('Price 12E*10', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][10]:Expecting a positive or negative number after E/e."+'\n'+
                             'Price 12E*10'+'\n'+
                             '         ^', e.msg)


    def test_advance_will_throw_exception_if_no_number_is_added_after_the_e_or_E(self):
        lexer = LexerStateMachine('Dummy 12E', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][10]:Expecting a positive or negative number after E/e."+'\n'+
                             'Dummy 12E'+'\n'+
                             '         ^', e.msg)

    def test_advance_will_throw_exception_if_alphabet_added_after_the_E(self):
        lexer = LexerStateMachine('Dummy 12EA', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][10]:Expecting a positive or negative number after E/e."+'\n'+
                             'Dummy 12EA'+'\n'+
                             '         ^', e.msg)

    def test_advance_will_accept_E_and_e_as_floating_point(self):
        lexer = LexerStateMachine('Dummy 12e-10', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 1.2e-09)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_throw_the_same_error_if_e_is_replace_E_in_the_floating_point(self):
        lexer = LexerStateMachine('Price 12e--10', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][11]:Unexpected symbol \"-\" been found after -"+'\n'+
            'Price 12e--10'+'\n'+
            '          ^', e.msg)

        lexer = LexerStateMachine('Price 12e++10', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][11]:Unexpected symbol \"+\" been found after +"+'\n'+
            'Price 12e++10'+'\n'+
            '          ^', e.msg)

        lexer = LexerStateMachine('Price 12e*10', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][10]:Expecting a positive or negative number after E/e."+'\n'+
                             'Price 12e*10'+'\n'+
                             '         ^', e.msg)

        lexer = LexerStateMachine('Dummy 12e', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][10]:Expecting a positive or negative number after E/e."+'\n'+
                             'Dummy 12e'+'\n'+
                             '         ^', e.msg)

        lexer = LexerStateMachine('Dummy 12eA', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][10]:Expecting a positive or negative number after E/e."+'\n'+
                             'Dummy 12eA'+'\n'+
                             '         ^', e.msg)

    def test_advance_will_return_the_actual_value_if_the_floating_point_with_bigger_number_on_both_sides(self):
        lexer = LexerStateMachine('Dummy 13123e151', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 1.3123e+155)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_return_a_floating_point_when_a_number_with_dot_is_found(self):
        lexer = LexerStateMachine('Dummy 123.456', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 123.456)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_return_a_floating_point_when_the_number_is_start_with_a_dot(self):
        lexer = LexerStateMachine('Dummy .456', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 0.456)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_return_a_floating_point_if_before_the_dot_will_have_a_zero(self):
        lexer = LexerStateMachine('Dummy 0.123456', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 0.123456)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_return_a_floating_point_if_the_number_is_end_with_a_dot(self):
        lexer = LexerStateMachine('Dummy 20.', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 20.0)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_return_a_floating_point_if_the_floating_point_is_in_the_begining_of_the_string(self):
        lexer = LexerStateMachine('.25', self.context)
        testToken = lexer.currentToken
        self.assertAlmostEqual(testToken.data[0], 0.25)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_return_a_floating_point_if_the_number_is_greater_than_1(self):
        lexer = LexerStateMachine('123456.25', self.context)
        testToken = lexer.currentToken
        self.assertAlmostEqual(testToken.data[0], 123456.25)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_throw_exception_when_there_is_only_a_dot_in_the_statement(self):
        lexer = LexerStateMachine('Dummy .', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][8]:Expecting number after ."+'\n'+
                             'Dummy .'+'\n'+
                             '       ^', e.msg)

    def test_advance_will_produce_a_token_which_carry_the_dot(self):
        lexer = LexerStateMachine('Dummy.', self.context)
        self.assertEqual(lexer.currentToken.id,'(identifier)')
        self.assertEqual(lexer.currentToken.data[0], 'Dummy')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '.')

    def test_advance_will_produce_a_token_for_dot_after_underscore(self):
        lexer = LexerStateMachine('Dummy_.', self.context)
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '.')

    def test_advance_will_produce_a_token_for_dot_after_number(self):
        lexer = LexerStateMachine('Dummy78.', self.context)
        self.assertEqual(lexer.currentToken.id,'(identifier)')
        self.assertEqual(lexer.currentToken.data[0], 'Dummy78')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '.')

    def test_advance_will_throw_an_error_if_the_expression_contain_dot_only(self):
        lexer = LexerStateMachine('Dummy .', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][8]:Expecting number after ."+'\n'+
                             'Dummy .'+'\n'+
                             '       ^', e.msg)

    def test_advance_will_throw_exception_if_the_dot_is_being_in_the_first_location(self):
        try:
            lexer = LexerStateMachine('.', self.context)
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][2]:Expecting number after ."+'\n'+
                             '.'+'\n'+
                             ' ^', e.msg)


    def test_advance_will_generate_a_token_for_hexadecimal_number(self):
        lexer = LexerStateMachine('Dummy 0X456', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 1110)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_generate_a_token_for_hexadecimal_that_contain_alphabet(self):
        lexer = LexerStateMachine('Dummy 0XABCDEF', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 11259375)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_generate_a_token_for_hexadecimal_that_contain_lower_alphabet(self):
        lexer = LexerStateMachine('Dummy 0Xfedcba', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 16702650)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_generate_a_token_for_hexamdecimal_that_mixed_with_number_and_valid_alphabet(self):
        lexer = LexerStateMachine('Dummy 0X1a2b3c4d5e6f', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 28772997619311)
        self.assertEqual(testToken.id, '(literal)')

    def test_advacne_will_generate_a_token_for_the_expression_with_0x(self):
        lexer = LexerStateMachine('Dummy 0x1a2b3c4d5e6f', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 28772997619311)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_generate_exception_for_no_number_or_valid_alphabet_appeared_after_the_0X(self):
        lexer = LexerStateMachine('Dummy 0X', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting hex number after 0X"+'\n'+
                             'Dummy 0X'+'\n'+
                             '        ^', e.msg)

        lexer = LexerStateMachine('Dummy 0x', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting hex number after 0x"+'\n'+
                             'Dummy 0x'+'\n'+
                             '        ^', e.msg)

        lexer = LexerStateMachine('Dummy 0xghi', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting hex number after 0x"+'\n'+
                             'Dummy 0xghi'+'\n'+
                             '        ^', e.msg)

        lexer = LexerStateMachine('Dummy 0xz', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting hex number after 0x"+'\n'+
                             'Dummy 0xz'+'\n'+
                             '        ^', e.msg)

        lexer = LexerStateMachine('Dummy 0x1234567989abcdefh', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][25]:Expecting hex number after f"+'\n'+
                             'Dummy 0x1234567989abcdefh'+'\n'+
                             '                        ^', e.msg)

        lexer = LexerStateMachine('Dummy 0x 123', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting hex number after 0x"+'\n'+
                             'Dummy 0x 123'+'\n'+
                             '        ^', e.msg)

    def test_advance_will_make_two_token_for_seperation_with_space(self):
        lexer = LexerStateMachine('0x123 Hello 0x456 0x789', self.context)
        testToken = lexer.currentToken
        self.assertAlmostEqual(testToken.data[0], 291)
        self.assertEqual(testToken.id, '(literal)')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0], "Hello")
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0], 1110)
        self.assertEqual(testToken.id, '(literal)')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0], 1929)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_generate_a_token_for_octal_number(self):
        lexer = LexerStateMachine('Dummy 012', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 10)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_generate_a_token_for_a_bigger_octal_number(self):
        lexer = LexerStateMachine('Dummy 01234567', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 342391)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_throw_exception_for_invalid_octal_number_been_found(self):
        lexer = LexerStateMachine('Dummy 08', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][8]:Expecting X/x, B/b, . or octal number after 0."+'\n'+
                             'Dummy 08'+'\n'+
                             '       ^', e.msg)

    def test_advance_will_throw_exception_for_invalid_number_after_some_valid_number(self):
        lexer = LexerStateMachine('Dummy 01238', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][11]:Expecting octal number after 3"+'\n'+
                             'Dummy 01238'+'\n'+
                             '          ^', e.msg)

    def test_advance_will_throw_exception_for_invalid_number_after_long_valid_number(self):
        lexer = LexerStateMachine('Dummy 012123456123457778', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][24]:Expecting octal number after 7"+'\n'+
                             'Dummy 012123456123457778'+'\n'+
                             '                       ^', e.msg)

    def test_advance_will_return_a_token_that_constructed_from_binary_number(self):
        lexer = LexerStateMachine('Dummy 0b1011', self.context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 11)
        self.assertEqual(testToken.id, '(literal)')

    def test_advance_will_throw_exception_for_invalid_number_appeared_after_0b(self):
        lexer = LexerStateMachine('Dummy 0b10115', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][13]:Expecting binary number after 1"+'\n'+
                             'Dummy 0b10115'+'\n'+
                             '            ^', e.msg)


    def test_advance_will_throw_exception_for_the_alphabet_after_0_is_not_x(self):
        lexer = LexerStateMachine('Dummy 0c1234', self.context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][8]:Expecting X/x, B/b, . or octal number after 0."+'\n'+
                             'Dummy 0c1234'+'\n'+
                             '       ^', e.msg)

    def test_advance_will_create_token_for_identifier(self):
        lexer = LexerStateMachine('var1', self.context)
        testToken = lexer.currentToken
        self.assertEqual(testToken.data[0], 'var1')
        self.assertEqual(testToken.id, '(identifier)')

    def test_advance_will_generate_token_for_identifier_that_contain_underscore(self):
        lexer = LexerStateMachine('_var1', self.context)
        testToken = lexer.currentToken
        self.assertEqual(testToken.data[0], '_var1')
        self.assertEqual(testToken.id, '(identifier)')

    def test_advance_will_recognize_a_long_identifier_with_mixture_of_underscore(self):
        lexer = LexerStateMachine('_var1_is_ready_to_read_and_edit_for_100_time_in_3_processor', self.context)
        testToken = lexer.currentToken
        self.assertEqual(testToken.data[0], '_var1_is_ready_to_read_and_edit_for_100_time_in_3_processor')
        self.assertEqual(testToken.id, '(identifier)')


    def test_advance_will_create_an_operator_token(self):
        lexer = LexerStateMachine('x+3', self.context)
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '+')

    def test_advance_will_create_token_for_prefix_and_postfix(self):
        lexer = LexerStateMachine('x++++3', self.context)
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '++')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '++')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '(literal)')
        self.assertEqual(testToken.data[0], 3)

    def test_advance_will_treat_the_zero_as_a_normal_number(self):
        lexer = LexerStateMachine('x = 0', self.context)
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '=')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '(literal)')
        self.assertEqual(testToken.data[0],0)

    def test_advance_will_get_equal_equal(self):
        lexer = LexerStateMachine('x == 0', self.context)
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '==')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '(literal)')
        self.assertEqual(testToken.data[0],0)

    def test_lexer_will_split_the_token_if_there_is_multiple_line_in_the_string(self):
        lexer = LexerStateMachine("""x =myVar +
                                  hisVar*oursVar
                                  -0X123F""", self.context)
        testToken = lexer.currentToken
        self.assertEqual(testToken.data[0],'x')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '=')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],'myVar')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '+')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],'hisVar')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '*')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],'oursVar')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '-')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],4671)
        self.assertEqual(testToken.id, '(literal)')

    def test_peep_will_throw_exception_for_unexpected_token(self):
        lexer = LexerStateMachine("""x =myVar +
                                  hisVar*oursVar
                                  -0X123F""", self.context)
        try:
            lexer.peep('(literal)')
            raise SyntaxError("Exception test failed!")
        except SyntaxError as e:
            self.assertEqual("Error[1][1]:Expecting (literal) before (identifier)"+'\n'+
                             'x =myVar +'+'\n'+
                             '^', e.msg)

    def test_lexer_will_recognize_logical_AND(self):
        lexer = LexerStateMachine('x && 0', self.context)
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '&&')
        testToken = lexer.advance()
        self.assertEqual(testToken.id, '(literal)')
        self.assertEqual(testToken.data[0],0)