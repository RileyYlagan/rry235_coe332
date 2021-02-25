#!/usr/bin/env python3

import json
import random
import sys


def breed(parent1,parent2):
	print('First Parent:',parent1)
	print('Second Parent:',parent2)
	
	childHead = parent1['head'] + '-' + parent2['head']
	childBody = parent1['body'] + '-' + parent2['body']
	childArms = round((parent1['arms'] + parent2['arms'])/2.0)
	childLegs = round((parent1['legs'] + parent2['legs'])/2.0)
	childTails = round((parent1['tails'] + parent2['tails'])/2.0)
	
	Child = {'head':childHead,'body':childBody,'arms':childArms,'legs':childLegs,'tails':childTails}
	print('Child:',Child)
	return Child

def main():
	with open(sys.argv[1],'r') as f:
		data = json.load(f)

	parent1 = random.choice(data['animals'])
	parent2 = random.choice(data['animals'])
	breed(parent1,parent2)

if __name__ == "__main__":
	main()
	



