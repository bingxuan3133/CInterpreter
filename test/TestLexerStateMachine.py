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
        pass



    def test_lexer_will_split_the_string_accordingly(self):
        manager = ContextManager()
        context = Context(manager)
        lexerSM = LexerStateMachine("""hi krizz""",context)

        self.assertEqual("hi", lexerSM.lists[0])

    def test_createCharGenerator_will_return_the_word_in_sequence(self):
        manager = ContextManager()
        context = Context(manager)
        lexerSM = LexerStateMachine("""hi krizz
                        987 456 """, context)
        self.assertEqual('h',lexerSM.getNextChar())
        self.assertEqual('i',lexerSM.getNextChar())
        self.assertEqual(' ',lexerSM.getNextChar())
        self.assertEqual('k',lexerSM.getNextChar())
        self.assertEqual('r',lexerSM.getNextChar())
        self.assertEqual('i',lexerSM.getNextChar())
        self.assertEqual('z',lexerSM.getNextChar())
        self.assertEqual('z',lexerSM.getNextChar())
        self.assertEqual(' ',lexerSM.getNextChar())
        self.assertEqual('9',lexerSM.getNextChar())
        self.assertEqual('8',lexerSM.getNextChar())
        self.assertEqual('7',lexerSM.getNextChar())
        self.assertEqual(' ',lexerSM.getNextChar())
        self.assertEqual('4',lexerSM.getNextChar())
        self.assertEqual('5',lexerSM.getNextChar())
        self.assertEqual('6',lexerSM.getNextChar())
        self.assertEqual(None,lexerSM.getNextChar())
        
    
    def test_advance_will_