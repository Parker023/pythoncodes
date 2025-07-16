lst=[[1,2,3],[4,5,6],[7,8,9]]

print(lst)
print(lst[0])
print(lst[0][2])
print(lst[1][1])
lst.append([10,20,30])
lst.append([40,50])
print(lst)

# delete the index
del lst[0]
print(lst)

for i in lst:
    for j in i:
        print(j,end=' ')