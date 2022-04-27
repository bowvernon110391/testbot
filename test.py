""" 
data = [
    { 'name' : 'name', 'value' : 'Bowie' },
    { 'name' : 'age', 'value' : '31' }
]

name = list(filter(lambda x: x['name'] == 'age', data))

if len(name):
    print(name[0]['value'])
else:
    print("Filter returns null") """

m = {
    'name' : 'Bowie',
    'age' : 31
}

for k, v in enumerate(m):
    print(f"{k}, {v}")