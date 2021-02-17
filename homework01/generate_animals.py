import json
import random
import petname

data = {}
data['animals'] = []
#need to generate 20 random animals each with the following attributes:
#head (animal) , body (animal-animal) , arms (rand[2-10]) , legs (rand[3-12]) , tail (sum of arms & legs)
heads = ['snake','bull','lion','raven','bunny']
for i in range(20):
	num_arms = random.randrange(2,14,2)
	num_legs = random.randrange(3,13,3)
	num_tails = num_arms + num_legs
	data['animals'].append({ 'head': heads[random.randrange(5)], 'body': petname.name()+'-'+petname.name(), 'arms' : num_arms, 'num_legs': num_legs, 'tails' : num_tails})

with open('animals.json', 'w') as out:
    json.dump(data, out, indent=2)

