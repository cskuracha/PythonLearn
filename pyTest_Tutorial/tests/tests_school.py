import pytest
from  source.school import Classroom, Teacher, Student, TooManyStudents

@pytest.fixture
def Shiva():
    return Teacher("Shiva")

@pytest.fixture
def Agastya():
    return Student("Agastya")

@pytest.fixture
def Atri():
    return Student("Atri")

@pytest.fixture
def Bhardwaja():
    return Student("Bhardwaja")

@pytest.fixture
def Gautama():
    return Student("Gautama")

@pytest.fixture
def Jamadagni():
    return Student("Jamadagni")

@pytest.fixture
def Vashista():
    return Student("Vashista")

@pytest.fixture
def Vishwamitra():
    return Student("Vishwamitra")

@pytest.fixture
def saptarshi_classroom(Shiva):
    students = []
    return Classroom(Shiva, students, "Enlightenment")

# Test cases
def test_create_classroom(saptarshi_classroom):
    assert saptarshi_classroom.teacher.name == "Shiva"
    assert saptarshi_classroom.course_title == "Enlightenment"
    assert len(saptarshi_classroom.students) == 0

def test_add_students(saptarshi_classroom, Agastya, Atri, Bhardwaja, Gautama, Jamadagni, Vashista, Vishwamitra):
    saptarshi_classroom.add_student(Agastya)
    saptarshi_classroom.add_student(Atri)
    saptarshi_classroom.add_student(Bhardwaja)
    saptarshi_classroom.add_student(Gautama)
    saptarshi_classroom.add_student(Jamadagni)
    saptarshi_classroom.add_student(Vashista)
    saptarshi_classroom.add_student(Vishwamitra)
    assert len(saptarshi_classroom.students) == 7

def test_add_Too_many_students(saptarshi_classroom, Agastya, Atri, Bhardwaja, Gautama, Jamadagni, Vashista, Vishwamitra):
    for _ in range(11):
        saptarshi_classroom.add_student(Student("Student"))

    with pytest.raises(TooManyStudents):
        saptarshi_classroom.add_student(Agastya)

def test_remove_student(saptarshi_classroom, Agastya, Atri, Bhardwaja, Gautama, Jamadagni, Vashista, Vishwamitra):
    saptarshi_classroom.add_student(Agastya)
    saptarshi_classroom.add_student(Atri)
    saptarshi_classroom.add_student(Bhardwaja)
    saptarshi_classroom.add_student(Gautama)
    saptarshi_classroom.add_student(Jamadagni)
    saptarshi_classroom.add_student(Vashista)
    saptarshi_classroom.add_student(Vishwamitra)
    saptarshi_classroom.add_student(Student("Kashyapa"))
    saptarshi_classroom.remove_student("Kashyapa")

    assert len(saptarshi_classroom.students) == 7

def test_change_teacher(saptarshi_classroom):
    new_teacher = Teacher("Adi Yogi")
    saptarshi_classroom.change_teacher(new_teacher)
    assert saptarshi_classroom.teacher.name == "Adi Yogi"
