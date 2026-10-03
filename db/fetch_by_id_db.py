import sqlite3

connection=sqlite3.connect('students.db')

cursor=connection.cursor()

student_id=int(input("Enter student id: "))

sql="select * from students where student_id=?"

cursor.execute(sql,(student_id,))

student=cursor.fetchone()
print(student)
connection.close()