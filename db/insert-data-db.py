import  sqlite3

connection = sqlite3.connect('students.db')


cursor = connection.cursor()

# take values from the user

student_name = input("Enter student name: ")
student_fees = int(input("Enter student fees: "))
student_course = input("Enter student course: ")
student_email = input("Enter student email: ")


sql="insert into students(student_name,student_email,student_course,student_fee) values(?,?,?,?)"

cursor.execute(sql,(student_name,student_email,student_course,student_fees))

connection.commit()
print("Data inserted successfully")

connection.close()
