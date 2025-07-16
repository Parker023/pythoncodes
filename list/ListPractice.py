list=['Anirudh','Hrushi','Revanth','Vishnu','Anirudh']
"""
multi line string test
"""
print(list[2:])
print(len(list[0]))
print(list[::-1])
print(list.count('Anirudh'))

print(list.extend(['sresta','thrisha']))
print(list)


nums=[4,8,1,9,2]
print(sorted(nums)[::-1])

print(nums.index(8))
print(min(nums))
print(max(nums))

for num in nums:
    print(num ,end=' ')

print()

for i in range(len(nums)):
    print(nums[i],end=' ')
# iterating in reverse
print()
for i in range(len(nums)-1,-1,-1):
    print(nums[i],end=' ')




