import matplotlib.pyplot as plt


# x=[1,2,3,4,5]
# y=[10,20,30,40,50]
# plt.plot(x,y)
#
# plt.title("Simple Graph")
# plt.xlabel("X-axis")
# plt.ylabel("Y-axis")
# plt.show()


students=["Harry", "Ron", "Hermione", "Draco", "Neville"]
marks=[85, 92, 78, 67, 99]


plt.bar(students, marks)
plt.xlabel("Students")
plt.ylabel("Marks")
plt.title("Student Marks")
plt.show()