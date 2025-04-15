from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from app.utils.llm import getCourseRoadmap, getResourceForTopic, getQuizQuestions
from app.dependencies import get_db
from app.models.models import (
    Course,
    Semester,
    Exam,
    Week,
    Topic,
    Quiz,
    Book,
    Resource,
    Questions,
)
from app.schemas.startSemester import (
    StartSemesterData,
)
import json


router = APIRouter()


# Mark topic as completed
@router.put("/updateTopicStatus")
def update_topic_status(topic_id: int = Query(...), db: Session = Depends(get_db)):
    # Step 1: Fetch the topic
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Step 2: Mark the topic as completed
    topic.status = "Completed"
    db.commit()

    # Step 3: Get the week the topic belongs to
    week_id = topic.week_id
    if not week_id:
        raise HTTPException(status_code=400, detail="Topic does not belong to any week")

    # Step 4: Check if all topics in that week are completed
    all_topics = db.query(Topic).filter(Topic.week_id == week_id).all()
    if all(topic.status == "Completed" for topic in all_topics):
        week = db.query(Week).filter(Week.week_id == week_id).first()
        if week:
            week.status = "Completed"
            db.commit()

    return {"message": "Topic status updated successfully."}


# Update the Attendance for a Course
@router.put("/updateAttendance")
def updateAttendance(
    course_id: int = Query(...),
    attendance: int = Body(...),
    db: Session = Depends(get_db),
):
    # Fetch the course
    course = db.query(Course).filter(Course.course_id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Update attendance value
    course.attendance = attendance

    db.commit()

    return {
        "status": 200,
        "message": "Attendance updated successfully",
        "course_id": course_id,
        "updated_attendance": attendance,
    }


# Update the Marks for an Exam
@router.put("/updateMarks")
def updateMarks(
    exam_id: int = Query(...), mark: int = Body(...), db: Session = Depends(get_db)
):
    # Fetch the exam by exam_id
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    # Update the mark and status
    exam.mark = mark
    exam.status = "Completed"  # Set status to Completed
    db.commit()

    return {
        "status": 200,
        "message": "Mark updated successfully",
        "exam_id": exam_id,
        "updated_mark": mark,
    }


# Get Attendance Records
@router.get("/attendanceRecords")
def getAttendanceRecord(user_id: int = Query(...), db: Session = Depends(get_db)):
    semesters = db.query(Semester).filter(Semester.user_id == user_id).all()

    if not semesters:
        raise HTTPException(status_code=404, detail="No semesters found")

    # Sort semesters by number in title (e.g., "Semester 1", "Semester 2", etc.)
    semesters.sort(key=lambda x: int(x.title.split()[-1]))

    for semester in semesters:
        courses = (
            db.query(Course).filter(Course.semester_id == semester.semester_id).all()
        )

        for course in courses:
            # Determine total_classes_needed
            if course.type == "Lab" and course.periods == 2:
                total_classes_needed = 60
            elif course.periods == 3:
                total_classes_needed = 45
            elif course.periods == 4:
                total_classes_needed = 60
            elif course.periods == 5:
                total_classes_needed = 75
            else:
                total_classes_needed = 0  # fallback/default

            # Ensure attendance is treated as integer (handle None)
            classes_missed = (
                int(course.attendance) if course.attendance is not None else 0
            )
            classes_attended = max(total_classes_needed - classes_missed, 0)

            # Calculate percentage attended
            percentage_classes_attended = (
                (classes_attended / total_classes_needed) * 100
                if total_classes_needed > 0
                else 0
            )

            # Set computed attributes for each course
            course.total_classes_needed = total_classes_needed
            course.percentage_classes_attended = round(percentage_classes_attended, 2)

        semester.courses = courses  # Attach course list to semester

    return {
        "status": 200,
        "message": "Attendance records fetched successfully",
        "semesters": semesters,
    }


# Get Academics Records
@router.get("/academicsRecords")
def getAcademicsRecords(user_id: int = Query(...), db: Session = Depends(get_db)):
    semesters = db.query(Semester).filter(Semester.user_id == user_id).all()

    if not semesters:
        raise HTTPException(status_code=404, detail="No semesters found")

    # Sort semesters by title number (e.g., "Semester 1", "Semester 2", etc.)
    semesters.sort(key=lambda x: int(x.title.split()[-1]))

    cumulative_grade_points = 0
    cumulative_credits = 0

    for semester in semesters:
        courses = (
            db.query(Course).filter(Course.semester_id == semester.semester_id).all()
        )
        total_weighted_grade_points = 0
        total_credits = 0

        for course in courses:
            exams = db.query(Exam).filter(Exam.course_id == course.course_id).all()

            # Safely extract marks with fallback to 0
            a1 = next(
                (
                    e.mark
                    for e in exams
                    if e.type == "Assesment 1" and e.mark is not None
                ),
                0,
            )
            a2 = next(
                (
                    e.mark
                    for e in exams
                    if e.type == "Assesment 2" and e.mark is not None
                ),
                0,
            )
            end = next(
                (
                    e.mark
                    for e in exams
                    if e.type == "End Semester" and e.mark is not None
                ),
                0,
            )

            # Calculate total mark
            total_mark = ((a1 + a2) * 0.4) + (end * 0.6)
            course.mark = round(total_mark, 2)

            # Convert mark to grade point
            if total_mark >= 91:
                grade_point = 10
            elif total_mark >= 81:
                grade_point = 9
            elif total_mark >= 71:
                grade_point = 8
            elif total_mark >= 61:
                grade_point = 7
            elif total_mark >= 51:
                grade_point = 6
            else:
                grade_point = 0  # U grade

            # Add weighted grade points
            total_weighted_grade_points += course.credit * grade_point
            total_credits += course.credit

        # GPA for the semester
        gpa = (
            round(total_weighted_grade_points / total_credits, 2)
            if total_credits
            else 0
        )
        semester.gpa = gpa

        # Cumulative values for CGPA
        cumulative_grade_points += total_weighted_grade_points
        cumulative_credits += total_credits

        # CGPA up to this semester
        cgpa = (
            round(cumulative_grade_points / cumulative_credits, 2)
            if cumulative_credits
            else 0
        )
        semester.cgpa = cgpa

        # Attach courses
        semester.courses = courses

    return {
        "status": 200,
        "message": "Academic records fetched successfully",
        "semesters": semesters,
    }


# Submit Quiz Answers
@router.put("/submitQuiz")
def submitQuiz(
    answers: list[dict] = Body(...),
    quiz_id: int = Query(...),
    db: Session = Depends(get_db),
):
    correct_count = 0

    for item in answers:
        question_id = item.get("question_id")
        chosen_ans = item.get("chosen_answer")

        if question_id is None or chosen_ans is None:
            continue  # skip incomplete entries

        question = (
            db.query(Questions).filter(Questions.question_id == question_id).first()
        )
        if question:
            if int(question.correct_answer) == chosen_ans:
                correct_count += 1

    # Update the score and status in the Quiz table
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if quiz:
        quiz.score = correct_count
        quiz.status = "Completed"  # Mark as completed

    db.commit()

    return {
        "status": 200,
        "message": "Answers submitted successfully",
        "score": correct_count,
    }


# Get Questions for a Quiz
@router.post("/startQuiz")
def startQuiz(quiz_id: int = Query(...), db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Step 1: Get the associated week
    week = db.query(Week).filter(Week.week_id == quiz.week_id).first()
    if not week:
        raise HTTPException(status_code=404, detail="Associated week not found")

    # Step 2: Get all topics for that week
    topics = db.query(Topic).filter(Topic.week_id == week.week_id).all()
    topic_list = [{"title": t.title, "description": t.description} for t in topics]

    # Step 3: Check if questions already exist for this quiz
    existing_questions = db.query(Questions).filter(Questions.quiz_id == quiz_id).all()
    if existing_questions:
        return {
            "status": 200,
            "quiz": quiz,
            "topics": topic_list,
            "message": "Quiz questions already exist",
            "questions": existing_questions,
        }

    # Step 4: Generate questions
    question_data = getQuizQuestions(
        topic_list
    )  # Make sure this is a list of dictionaries

    # Step 5: Insert new questions into the database
    for q in question_data:
        if (
            isinstance(q, dict)
            and "title" in q
            and "options" in q
            and "correct_answer" in q
        ):
            question = Questions(
                quiz_id=quiz.quiz_id,
                user_id=quiz.user_id,
                title=q["title"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                chosen_answer=None,
            )
            db.add(question)
        else:
            print(f"Invalid question data: {q}")  # Log invalid data

    db.commit()

    # ✅ Step 6: Refetch the quiz and questions from DB
    refreshed_quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    created_questions = db.query(Questions).filter(Questions.quiz_id == quiz_id).all()

    return {
        "status": 200,
        "quiz": refreshed_quiz,
        "topics": topic_list,
        "message": "Quiz started and questions generated",
        "questions": created_questions,
    }


# Get or Create Topic Resources and Books
@router.post("/getTopicResource")
def getTopicResource(topic_id: int = Query(...), db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    books = db.query(Book).filter(Book.topic_id == topic_id).all()
    resources = db.query(Resource).filter(Resource.topic_id == topic_id).all()

    # If no existing books or resources, populate from external data
    if not books and not resources:
        data = getResourceForTopic(topic)
        print(data)

        # Update topic description
        topic.description = data.get("description")
        db.commit()
        db.refresh(topic)

        # Insert books
        for book in data.get("books", []):
            new_book = Book(
                title=book["title"],
                author=book["author"],
                edition=book["edition"],
                topic_id=topic_id,
                description=book.get(
                    "description"
                ),  # Optional if you’ve added this column
            )
            db.add(new_book)

        # Insert resources
        for res in data.get("resources", []):
            new_res = Resource(
                title=res["title"],
                description=res["description"],
                website_link=res["website_link"],
                topic_id=topic_id,
            )
            db.add(new_res)

        db.commit()

        # Re-fetch updated values
        books = db.query(Book).filter(Book.topic_id == topic_id).all()
        resources = db.query(Resource).filter(Resource.topic_id == topic_id).all()

    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()

    return {
        "topic": topic,
        "books": books,
        "resources": resources,
    }


# Get All Topics, Weeks, Quizzes, Exams for a Course
@router.get("/getAllTopics")
def getAllTopics(course_id: int = Query(...), db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Get and sort weeks and exams
    weeks = db.query(Week).filter(Week.course_id == course.course_id).all()
    exams = db.query(Exam).filter(Exam.course_id == course.course_id).all()

    # Annotate with type for sorting and identification
    combined = [{"type": "week", "data": week, "rank": week.rank} for week in weeks] + [
        {"type": "exam", "data": exam, "rank": exam.rank} for exam in exams
    ]

    # Sort based on rank
    combined.sort(key=lambda x: x["rank"])

    result = []

    for item in combined:
        if item["type"] == "week":
            week = item["data"]

            # Get topics for the week
            topics = (
                db.query(Topic)
                .filter(Topic.week_id == week.week_id)
                .order_by(Topic.title)
                .all()
            )

            # Add the week itself
            result.append({"type": "week", "week": week})

            # Add topics of the week
            for topic in topics:
                result.append({"type": "topic", "topic": topic})

            # ✅ Add quiz of the week
            quiz = db.query(Quiz).filter(Quiz.week_id == week.week_id).first()
            if quiz:
                result.append({"type": "quiz", "quiz": quiz})

        elif item["type"] == "exam":
            # Add the exam directly
            result.append({"type": "exam", "exam": item["data"]})

    return result


@router.get("/getCourseStatistics")
def getCourseStatistics(course_id: int = Query(...), db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Get exams and weeks
    exams = (
        db.query(Exam)
        .filter(Exam.course_id == course.course_id)
        .order_by(Exam.rank)
        .all()
    )
    weeks = (
        db.query(Week)
        .filter(Week.course_id == course.course_id)
        .order_by(Week.rank)
        .all()
    )

    # Set next_topic
    next_week = next((week for week in weeks if week.status == "Pending"), None)
    course.next_topic = next_week

    # Stats
    total_quizzes = 0
    completed_quizzes = 0
    quiz_score = 0
    total_topics = 0
    completed_topics = 0
    quiz_performance = []

    for week in weeks:
        topics = (
            db.query(Topic)
            .filter(Topic.week_id == week.week_id)
            .order_by(Topic.title)
            .all()
        )
        quizzes = db.query(Quiz).filter(Quiz.week_id == week.week_id).all()

        week.quizzes = quizzes
        week.topics = topics

        for quiz in quizzes:
            if quiz.status == "Completed":
                quiz_performance.append(quiz.score)
                quiz_score += quiz.score
                completed_quizzes += 1

        total_quizzes += len(quizzes)
        total_topics += len(topics)
        completed_topics += sum(1 for topic in topics if topic.status == "Completed")

    # Attendance logic
    classes_missed = course.attendance or 0
    if course.periods == 45 or course.periods in [2, 4]:
        total_required = 60
    elif course.periods == 5:
        total_required = 75
    else:
        total_required = 0

    classes_attended = max(total_required - classes_missed, 0)

    # Attach calculated values
    course.quiz_performance = quiz_performance
    course.total_quizzes = total_quizzes
    course.completed_quizzes = completed_quizzes
    course.avg_quiz_score = (
        round(quiz_score / total_quizzes, 2) if total_quizzes > 0 else 0
    )
    course.total_topics = total_topics
    course.completed_topics = completed_topics
    course.progress = (
        round((completed_topics / total_topics) * 100, 2) if total_topics > 0 else 0
    )
    course.classes_attended = classes_attended
    course.exams = exams

    return course


# Get All Courses
@router.get("/getAllCourses")
def getAllCourses(
    user_id: int = Query(...),
    semester_id: int = Query(...),
    db: Session = Depends(get_db),
):
    courses = (
        db.query(Course)
        .filter(
            Course.user_id == user_id,
            Course.semester_id == semester_id,
        )
        .all()
    )

    # Setting next topic and progress for each course
    for course in courses:
        weeks = (
            db.query(Week)
            .filter(Week.course_id == course.course_id)
            .order_by(Week.rank)
            .all()
        )

        # Set next_topic
        next_week = next((week for week in weeks if week.status == "Pending"), None)
        course.next_topic = next_week

        # Progress calculation
        total_weeks = len(weeks)
        completed_weeks = sum(1 for week in weeks if week.status == "Completed")

        course.progress = (
            round((completed_weeks / total_weeks) * 100, 2) if total_weeks > 0 else 0
        )

    return courses


# Get All Semesters
@router.get("/getAllSemesters")
def getAllSemesters(user_id: str = Query(...), db: Session = Depends(get_db)):
    semesters = db.query(Semester).filter(Semester.user_id == user_id).all()

    for semester in semesters:
        courses = (
            db.query(Course)
            .filter(
                Course.semester_id == semester.semester_id, Course.user_id == user_id
            )
            .all()
        )

        total_credits = 0
        weighted_score = 0
        is_ongoing = False

        for course in courses:
            total_credits += course.credit or 0
            if course.status == "Active":
                is_ongoing = True
            if course.mark is not None:
                weighted_score += course.credit * course.mark

        semester.course_count = len(courses)
        semester.credits = total_credits
        semester.status = "OnGoing" if is_ongoing else "Completed"

    # Sort semesters based on the number in the title (e.g., "Semester 1", "Semester 2")
    semesters.sort(key=lambda x: int(x.title.split()[-1]))

    # Load next semester data from file
    with open(
        "C:/Users/tvaru/Desktop/AI-ASULP/app/data/semester_course_details.json", "r"
    ) as file:
        next_semester_data = json.load(file)[len(semesters)]

    electives = [
        {"title": course["title"], "choices": course["choices"]}
        for course in next_semester_data["courses"]
        if course["code"] == ""
    ]

    nxt_semester = {
        "title": next_semester_data["title"],
        "status": "Not Started",
        "gpa": 0.0,
        "electives": electives,
    }

    semesters.append(nxt_semester)
    return semesters


# Initiate A Semester
@router.post("/startSemester")
def startSemester(
    payload: StartSemesterData,
    db: Session = Depends(get_db),
):
    # Step 1: Load all semester data from your JSON file
    with open(
        "C:/Users/tvaru/Desktop/AI-ASULP/app/data/semester_course_details.json", "r"
    ) as file:
        data = json.load(file)

    # Step 2: Find the semester matching the input title
    matched_semester = next(
        (s for s in data if s.get("title") == payload.semester_title),
        None,
    )

    if not matched_semester:
        raise HTTPException(status_code=404, detail="Semester not found in roadmap")

    # Step 3: Create the Semester in DB
    semester = Semester(
        title=matched_semester.get("title"),
        user_id=payload.user_id,
        gpa=0.0,
    )

    db.add(semester)
    db.commit()
    db.refresh(semester)

    semester_data = {
        "title": semester.title,
        "start_date": payload.start_date,
        "end_date": payload.end_date,
    }

    # Filling the Elective Course Options from users input
    for item in matched_semester.get("courses", []):

        if item.get("code") == "":
            option = next(
                (x for x in payload.electives if x.title == item["title"]), None
            )
            if option:
                item["code"] = option.code
                item["title"] = option.option
                item.pop("choices", None)  # ✅ remove choices if it exists

    # Step 4: Loop through each course and insert it
    for course_item in matched_semester.get("courses", []):
        courseRoadmap = getCourseRoadmap(semester_data, course_item)

        course = Course(
            title=courseRoadmap.get("title"),
            code=courseRoadmap.get("code"),
            description=courseRoadmap.get("description"),
            credit=courseRoadmap.get("credit"),
            periods=courseRoadmap.get("periods"),
            start_date=courseRoadmap.get("start_date"),
            end_date=courseRoadmap.get("end_date"),
            status=courseRoadmap.get("status"),
            user_id=payload.user_id,
            semester_id=semester.semester_id,
            type=courseRoadmap.get("type"),
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        # Step 5: Create Exams for each course
        for exam_data in courseRoadmap.get("Exams", []):
            exam = Exam(
                title=exam_data.get("title"),
                type=exam_data.get("type"),
                rank=exam_data.get("rank"),
                start_date=exam_data.get("start_date"),
                end_date=exam_data.get("end_date"),
                status=exam_data.get("status"),
                course_id=course.course_id,
                user_id=payload.user_id,
            )
            db.add(exam)
            db.commit()
            db.refresh(exam)

        # Step 6: Create Weeks & Topics for each course
        for week_data in courseRoadmap.get("Weeks", []):
            week = Week(
                title=week_data.get("title"),
                rank=week_data.get("rank"),
                status=week_data.get("status"),
                course_id=course.course_id,
                user_id=payload.user_id,
            )
            db.add(week)
            db.commit()
            db.refresh(week)

            # Step 6.1: Create Quiz for the week
            quiz = Quiz(
                title=f"{week.title} - Quiz",
                status="Pending",
                score=0.0,
                user_id=payload.user_id,
                week_id=week.week_id,
            )
            db.add(quiz)
            db.commit()
            db.refresh(quiz)

            # Step 6.2: Create Topics under this week
            for topic_data in week_data.get("Topics", []):
                topic = Topic(
                    title=topic_data.get("title"),
                    description=topic_data.get("description"),
                    week_id=week.week_id,
                    user_id=payload.user_id,
                    status="Pending",
                )
                db.add(topic)
                db.commit()
                db.refresh(topic)

    return {"status": 200, "message": "Semester and all courses successfully created"}
