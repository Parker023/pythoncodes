# nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

even = [i for i in range(1, 21) if i % 2 == 0]
print(even)
even = [i ** 2 for i in range(1, 21) if i % 2 == 0]
print('-' * 40)
print(even)
print('-' * 40)
print([[i for i in range(1, 6)] for i in range(3)])
print('-' * 40)

mlst=[[1,2,3],[4,5,6],[7,8,9]]
print([j for i in mlst for j in i] )
