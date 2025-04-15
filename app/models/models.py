from sqlalchemy import Column, Integer, String, Float, Enum, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    cgpa = Column(Float)

    semesters = relationship("Semester", back_populates="user")
    courses = relationship("Course", back_populates="user")
    exams = relationship("Exam", back_populates="user")
    weeks = relationship("Week", back_populates="user")
    quizzes = relationship("Quiz", back_populates="user")
    questions = relationship("Questions", back_populates="user")


class Semester(Base):
    __tablename__ = "semester"
    semester_id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    gpa = Column(Float)

    user = relationship("User", back_populates="semesters")
    courses = relationship("Course", back_populates="semester")


class Course(Base):
    __tablename__ = "course"
    course_id = Column(Integer, primary_key=True)
    title = Column(String)
    code = Column(String)
    credit = Column(Integer)
    periods = Column(Integer)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum("Active", "Completed", "Dropped", name="course_status"))
    type = Column(Enum("Lab", "Theory", "Lab+Theory", name="course_type"))
    mark = Column(Float)
    attendance = Column(Float)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    semester_id = Column(Integer, ForeignKey("semester.semester_id"))

    user = relationship("User", back_populates="courses")
    semester = relationship("Semester", back_populates="courses")
    weeks = relationship("Week", back_populates="course")
    exams = relationship("Exam", back_populates="course")


class Book(Base):
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    edition = Column(String)

    topic_id = Column(Integer, ForeignKey("topic.topic_id"))
    topic = relationship("Topic", back_populates="books")


class Resource(Base):
    __tablename__ = "resource"
    resource_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    website_link = Column(String)

    topic_id = Column(Integer, ForeignKey("topic.topic_id"))
    topic = relationship("Topic", back_populates="resources")


class Exam(Base):
    __tablename__ = "exam"
    exam_id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(Enum("Assesment 1", "Assesment 2", "End Semester", name="exam_type"))
    rank = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum("Scheduled", "Completed", name="exam_status"))
    mark = Column(Float)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    course_id = Column(Integer, ForeignKey("course.course_id"))

    user = relationship("User", back_populates="exams")
    course = relationship("Course", back_populates="exams")


class Week(Base):
    __tablename__ = "week"
    week_id = Column(Integer, primary_key=True)
    title = Column(String)
    rank = Column(Integer)
    course_id = Column(Integer, ForeignKey("course.course_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    status = Column(Enum("Ongoing", "Completed", "Pending", name="weekly_status"))
    attendance = Column(Float)

    quiz = relationship(
        "Quiz", back_populates="week", uselist=False, foreign_keys="[Quiz.week_id]"
    )

    course = relationship("Course", back_populates="weeks")
    user = relationship("User", back_populates="weeks")
    topics = relationship("Topic", back_populates="week")


class Topic(Base):
    __tablename__ = "topic"
    topic_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(Enum("Pending", "Completed", "Ongoing", name="topic_status"))
    user_id = Column(Integer, ForeignKey("user.user_id"))

    week_id = Column(Integer, ForeignKey("week.week_id"))
    week = relationship("Week", back_populates="topics")

    # New relationships
    books = relationship("Book", back_populates="topic")
    resources = relationship("Resource", back_populates="topic")


class Quiz(Base):
    __tablename__ = "quiz"
    quiz_id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(Enum("Pending", "Completed", name="quiz_status"))
    score = Column(Float)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    week_id = Column(Integer, ForeignKey("week.week_id"), unique=True)
    week = relationship("Week", back_populates="quiz")
    user = relationship("User", back_populates="quizzes")
    questions = relationship("Questions", back_populates="quiz")


class Questions(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True)
    title = Column(String)
    options = Column(String)
    correct_answer = Column(String)
    chosen_answer = Column(String)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"))

    user = relationship("User", back_populates="questions")
    quiz = relationship("Quiz", back_populates="questions")
