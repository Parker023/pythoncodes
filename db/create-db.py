import sqlite3

# create a connection
connection=sqlite3.connect('students.db')

# create a cursor
cursor=connection.cursor()

cursor.execute(

    """
    create table IF NOT EXISTS students(
    student_id integer primary key autoincrement,
    student_name text,
    student_email text unique,
    student_course text,
    student_fee real
    )
    
    """
)

connection.commit()
connection.close()

print("Table created successfully")