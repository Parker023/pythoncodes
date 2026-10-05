
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

from courses import courses

app = FastAPI()

@app.get("/")
def get_welcome_msg():
    return {"message": "Welcome to FastAPI!"}

@app.get("/courses/{course_id}")
def get_course_details(course_id: int):
   course_details=courses.get(course_id)

   if course_details is None:
       raise HTTPException(status_code=404, detail="Course not found")
   return course_details

@app.get("/courses")
def get_courses():
    # print(type(courses.keys()))
    # print(type(courses.values()))
    return list(courses.values())

@app.get("/course-search")
def search_courses(query: str):

    results = []
    for course_id,course_details in courses.items():
        if query.lower() in course_details["name"].lower():
            results.append(
                {"course_id":course_id,
                  **course_details
                 }
            )

    return results


class Course(BaseModel):
    name: str
    description: str
    Fee: int


@app.post("/save-course",status_code=201)
def create_course(course: Course):
    #logic to insert course into database
    return {
        "message":"Course created successfully",
        "course":course
    }

