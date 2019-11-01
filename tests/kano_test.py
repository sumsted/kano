from kano import Kano
import unittest

class KanoTest(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def test_init(self):
        try:
            kano = Kano()
        except Exception as e:
            self.assertFalse('Kano device not found' in str(e))
            self.assertTrue(True, 'Unexpected exception raised: '+str(e))
        
    def test_read_proximity(self):
        try:
            kano = Kano()
            result = kano.read_proximity()
            self.assertTrue(0 <= result <= 255)
        except Exception as e:
            self.assertFalse('Kano device not found' in str(e))
            self.assertTrue(True, 'Unexpected exception raised: '+str(e))

    def test_exec_command(self):
        try:
            kano = Kano()
            kano.exec_command('echo hello')
        except Exception as e:
            self.assertFalse('Kano device not found' in str(e))
            self.assertFalse('Unable to execute command' in str(e))
            self.assertTrue(True, 'Unexpected exception raised: '+str(e))

    def test_do_commands(self):
        pass # need test

if __name__ == '__main__':
    unittest.main()