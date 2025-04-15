import os
import json
from dotenv import load_dotenv
from google import genai

# Load .env variables
load_dotenv()
client = genai.Client(api_key=os.getenv("AI_API_KEY"))


# AI Call to get the Course Roadmap
def getCourseRoadmap(semester, course):
    # A: Read and stringify JSON from file
    with open(
        "C:/Users/tvaru/Desktop/AI-ASULP/app/data/semester_course_details.json", "r"
    ) as f:
        json_data = json.load(f)
    A = json.dumps(json_data, indent=2)  # Pretty-printed for readability

    # B: Placeholder text (you can replace this later)
    B = """
            i am developing application that helps a university student by creating roadmaps for him, each course to help him prepare through out the semester. i have this syllabus for our entire program above. This is how it works, each time a student starts a semester by clicking a button in our semester, you will have the start and end of semester, also the Exams in between. You need to prepare a roadmap for each Course in that Semester, including all the Exams in Between, plan the roadmap has Weeks, within each Weeks there will be many Topics, There is a Quiz after each Week. the Roadmap must be within the Semester Period. Now i will give the database schema for the models in my application i have set.

            Just read it and follow that to create functions.

            User :
            user_id
            first_name - string
            last_name - string
            email - string
            password - string
            cgpa - float

            Semester :
            semester_id
            title - string
            user_id - int
            Courses []
            gpa - float

            Course :
            course_id
            title - string
            code - string
            credit - int
            periods - int
            description - string
            start_date (yyyy-mm-dd) - date
            end_date (yyyy-mm-dd) - date
            type ("Lab", "Theory", "Lab+Theory")
            Exams [] 
            Books []
            Weeks []
            user_id 
            semester_id
            status ("Active", "Completed", "Dropped")
            mark - float
            attendance - float

            Exams :
            exam_id
            title - string
            type  ("Assesment 1", "Assesment 2", "End Semester")
            rank - int
            start date (yyyy-mm-dd) - date
            end date (yyyy-mm-dd) - date
            status ("Scheduled", "Completed")
            mark - float
            user_id
            semester_id

            Weeks :
            week_id
            title - string
            rank - int
            Topics []
            course_id
            quiz_id
            user_id
            status ("Ongoing", "Completed", "Pending")
            attendance - float

            Quiz :
            quiz_id
            title - string
            Questions []
            status ("Pending", "Completed")
            score

            Question :
            question_id
            title - string 
            options - string
            correct ans
            chosen ans
            user_id
            quiz_id

            Topic :
            topic_id
            title - string
            description - string
            resources - string
            status ("Pending", "Completed", "Ongoing")

            Book :
            book_id
            title - string
            author - string
            edition - string
            description - string

            now if a user starts a semester, you need to give me the roadmap for all courses in the semester as a json file, also the weeks, exams in the courses, also the topics in each weeks. The rank attribute in week and exam helps to depict the order in which they will be ordered when combined, the three exams - Assessment I and Assessment II and Final End Semester, the Assessment II and End Semester should be at the final, the Assessment I should be in the middle of the weeks. The rank attribute helps to determine where to place an exam in between weeks, no two weeks or exams can have the same rank.

            Make sure the spelling are followed just as i gave for exam types, course types, and all enum attributes
            
        """  # Placeholder for B

    # C: Placeholder text (you can replace this later)
    C = f"""
        Just return the roadmap for the course {course} which is in {semester["title"]} and the semester lies between the period semester start data : {semester["start_date"]} and end date : {semester["end_date"]}, I clearly only want a json data, no other extra texts content should be present, just json data that depicts the roadmap for the course i gave
    """

    # Final prompt = A + B + C
    prompt = A + B + C

    # Call Gemini
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    try:
        return json.loads(
            response.text.strip().removeprefix("```json").removesuffix("```").strip()
        )
    except json.JSONDecodeError:
        print("Could not parse JSON. Raw response:")
        print(response.text)
        return {}


# AI Call to get the Resources for a Topic
def getResourceForTopic(topic):
    A = """
                Book :
                title
                description
                author
                edition

                Resource :
                title
                description
                website_link

                i have two tables which will store the resources and books to refer to study about a topic for a university student. Given a topic, provide me the resources and books for the student to refer, the description of book table denotes which chapter in the book i need to refer. Also i need a two paragraph summary of the topic. Give the final resultant data in the form a json, only json is what is need :

                {
                topic : "",
                description : "", 
                books : [],
                resources : []
                }   

            """

    B = f"""just now, give me json for the topic \"{topic.title + " - " + topic.description}\""""

    prompt = A + B

    # Call Gemini
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    try:
        return json.loads(
            response.text.strip().removeprefix("```json").removesuffix("```").strip()
        )
    except json.JSONDecodeError:
        print("Could not parse JSON. Raw response:")
        print(response.text)
        return {}


# AI Call to get the Questions for a Topic
def getQuizQuestions(topics):
    A = """
        Question :
            title
            options
            correct_answer
            chosen_answer

        I have to design quiz in my university student AI partner application, given a set of topics, i want you to provide exactly 20 MCQ questions for that quiz, the resultant should be a json data with the 20 questions. For the attribute 'option' store the four options of MCQ questions as a string separated by a delimiter "<I>", And the correct answer should be the number of the option (1/2/3/4). Just give me a json data, no other extra data should be present. The data must be a list json of objects, nothing other

        Here are the topics

        """

    B = ""
    for topic in topics:
        B += f"Topic : {topic['title']}\nDescription : {topic['description']}\n\n"

    B = B.strip()  # Remove the trailing newline

    prompt = A + B

    # Call Gemini
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    try:
        return json.loads(
            response.text.strip().removeprefix("```json").removesuffix("```").strip()
        )
    except json.JSONDecodeError:
        print("Could not parse JSON. Raw response:")
        print(response.text)
        return {}
