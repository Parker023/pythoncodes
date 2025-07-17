dict = {1: 'Anirudh', 2: 'Vishnu', 42: 'Revanth'}

print(dict.get(3))

# or
map = {1: [1, 2, 3], 2: [4, 5, 6], 22: [7, 8, 9]}
print(dict[42])
print(dict.pop(2))
print(dict)
print(map)
if map.__contains__(2):
    print(map.pop(2))
# del map[1]
print(map)
print(map.keys())
print(map.values())
for k in map.keys():
    print(k, map[k])
print(map.items())

# check contains
print(22 in map)

dct_1 = {1: 'Anirudh', 2: 'Vishnu', 42: 'Revanth'}
dct_2 = {4: 'Hrushi', 23: 'Girish'}
dct_1.update(dct_2)
print(dct_1)

lst = {'Anirudh', 'Vishnu', 'Revanth', 'Girish'}

dct_3 = {len(i):i for i in lst}
print(dct_3)
