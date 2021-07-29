from django.test import TestCase

class SmokeTest(TestCase):
    '''Тест на токсичность'''
    def test_bad_math(self):
        '''тест на неправильные математические рассчеты'''
        self.assertEqual(1, 1+1)