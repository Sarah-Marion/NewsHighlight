import unittest
from app.models import Source

class Source_Test(unittest.TestCase):
    """
    Test class to test the behavior of the Article class
    """
    def setUp(self):
        """
        set up  method will run before every Test
        """
        self.new_source= Source("title","name","description","www.test.com","test.com/img","Sarah")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_source,Source))
