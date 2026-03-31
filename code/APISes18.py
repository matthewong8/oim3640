import requests

response = requests.get('https://oim.108122.xyz/words/random', headers={'X-Token': 'matthewmatthew'},)

print(response.json())

# data = response.json()

# print(data['name'])
# print(data['governor'])

# print(len(data))
# print(data.keys())

# towns = data['data']
# print(type(towns))

# pprint(towns)
# print(len(towns))

# response = requests.get('https://oim.108122.xyz/words/random')
# print(response.json())