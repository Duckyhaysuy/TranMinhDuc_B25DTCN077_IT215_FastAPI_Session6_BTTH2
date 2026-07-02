from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class Student(BaseModel):
    code: str
    name: str
    email: str
    age: int


@app.post("/students")
def create_student(student: Student):
    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Tên không được để trống")

    if student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email không được để trống")

    if student.age <= 0:
        raise HTTPException(status_code=400, detail="Tuổi phải lớn hơn 0")

    for student in students:
        if student["code"] == student.code:
            raise HTTPException(status_code=400, detail="Mã học viên đã tồn tại")

    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Thêm học viên thành công",
        "data": new_student
    }


@app.get("/students")
def get_students(keyword: str = None, min_age: int = None, max_age: int = None):

    result = students

    if keyword:
        keyword = keyword.lower()
        result = [
            student for student in result
            if keyword in student["name"].lower()
            or keyword in student["code"].lower()
            or keyword in student["email"].lower()
        ]

    if min_age is not None:
        result = [student for student in result if student["age"] >= min_age]

    if max_age is not None:
        result = [student for student in result if student["age"] <= max_age]

    return result


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Tên không được để trống")

    if student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email không được để trống")

    if student.age <= 0:
        raise HTTPException(status_code=400, detail="Tuổi phải lớn hơn 0")

    for s in students:
        if s["code"] == student.code and s["id"] != student_id:
            raise HTTPException(status_code=400, detail="Mã học viên đã tồn tại")

    for student in students:
        if student["id"] == student_id:
            student["code"] = student.code
            student["name"] = student.name
            student["email"] = student.email
            student["age"] = student.age

            return {
                "message": "Cập nhật học viên thành công",
                "data": student
            }

    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {
                "message": "Xóa học viên thành công"
            }

    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")