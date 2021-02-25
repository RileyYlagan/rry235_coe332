import unittest
from read_animals import breed

class TestBreedMethod(unittest.TestCase):
	
	def test_breed(self):
		#two example inputs simulating parents
		dict1 = {'head':'snake' ,'body':'sheep-bunny' ,'arms': 4,'legs': 6,'tails': 10 }
		dict2 = {'head':'bull' ,'body':'parrot-bream' ,'arms': 6 ,'legs': 12 ,'tails': 18}
		
		self.assertEqual(breed(dict1,dict2),{'head':'snake-bull' ,'body':'sheep-bunny-parrot-bream' ,'arms': 5,'legs': 9,'tails': 14})			
		self.assertEqual(type(breed(dict1,dict2)),dict)
		self.assertRaises(TypeError,breed,'test1','test2')
		self.assertRaises(TypeError,breed,1,2)
		self.assertRaises(TypeError,breed, True, False)

if __name__ == '__main__':
	unittest.main()
	
