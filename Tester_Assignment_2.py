from database import *
# database.py:
'''movie_info = {'year':[1991, 1992, 1993, 1994], 'movie':['swag', 'yolo', 'wagwan', 'waste yute']}
random = {'s':[1,2,3,4], 'y':[5,6,7,8]}

my_dict = {}
my_dict.update(movie_info)

print(my_dict)

my_dict2 = {}
my_dict2['movie_info'] = movie_info
my_dict2['random'] = random

print(my_dict2)'''


# reading.py:
headers = '      swag,yolo       '
columns = ['    hi,earth   ', '   hello,world   ']
    
new_columns = []
headers = headers.strip()
headers = headers.split(',')

for counter in range(0, len(columns)):
    new_columns += columns[counter].split(',')

for counter in range (len(new_columns)):
    new_columns[counter] = new_columns[counter].strip()

print('headers =',headers)
print(new_columns)

table = {}
header_values = []
start = 0
all_header_values = []

for counter in range(len(headers)):
    for count in range(start, len(new_columns), len(headers)):
        header_values.append(new_columns[count])
    start += 1
    all_header_values.append(header_values)
    header_values = []

for counter in range(len(headers)):
    table[headers[counter]] = all_header_values[counter]

print(table)


# squeal.py:
table1 = {'swag': ['hi', 'hello'], 'yolo': ['earth', 'world']}
table2 = {'waste': ['wagwan', 'popcon'], 'yute': ['bod', 'mon']}


table1_keys = []
for element in table1:
    table1_keys.append(element)
print('keys =',table1_keys)


for element in table2:
    table2[element] *= 2
print("table2 =", table2)

for element in table1:
    print('element =', table1[element])

new_table1 = {}
for bitch in table1_keys:
    new_table1[bitch] = []
    for counter in range(2):
        for count in range(2):
            new_table1[bitch].append(table1[bitch][counter])
            
tatti = ['blah=blah', 'bah=bah']
masala = []

#for element in tatti:
    #equal_index = tatti[element].index('=')
    #print('euqal_index =', equal_index)
    #masala.append(tatti[element].split(equal_index))

print(new_table1)

table = {}

table.update(new_table1)
table.update(table2)

a = Table(table)
a.print_csv()

print(masala)

x = 'nkjskldf=hinlsdf'
index = x.index('=')
print(index)