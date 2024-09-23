import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from PIL import Image
import plotly.express as px
import hashlib
import os

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a user database if it doesn't exist
def create_user_database():
    if not os.path.exists('users.csv'):
        df = pd.DataFrame(columns=['Username', 'Password'])
        df.to_csv('users.csv', index=False)

# Function to register a new user
def register_user(username, password):
    df = pd.read_csv('users.csv')
    if username in df['Username'].values:
        return False  # User already exists
    new_user = pd.DataFrame({'Username': [username], 'Password': [hash_password(password)]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv('users.csv', index=False)
    return True  # User registered successfully

# Function to verify user credentials
def verify_user(username, password):
    df = pd.read_csv('users.csv')
    return any((df['Username'] == username) & (df['Password'] == hash_password(password)))

# Custom CSS for styling
# Custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(to right, #e0eafc, #cfdef3);
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        h1 {
            color: white;
            margin-bottom: 20px;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 20px;
        }
        input {
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 300px;
            font-size: 16px;
        }
        .stButton {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        .stButton button {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            background-color: #007BFF;
            color: white;
            cursor: pointer;
            font-size: 18px;
            transition: background-color 0.3s, transform 0.3s;
            margin: 10px;
            min-width: 200px;
        }
        .stButton button:hover {
            background-color: #0056b3;
            transform: translateY(-2px);
        }
        .stButton button:focus {
            outline: none;
        }
        .success {
            background-color: green !important;
        }
        .error {
            background-color: red !important;
        }
        .link {
            margin-top: 10px;
            color: #007BFF;
            text-decoration: none;
        }
        .link:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# Function for the login page
def login_page():
    add_custom_css()
    st.markdown("<h1>Engineering Course Difficulty Index Calculator</h1>", unsafe_allow_html=True)
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        if verify_user(username, password):
            st.success("Login successful! Redirecting to the main page...")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "main"
            st.markdown('<style>button:focus { background-color: green !important; }</style>', unsafe_allow_html=True)
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")
            st.markdown('<style>button:focus { background-color: red !important; }</style>', unsafe_allow_html=True)

    register_button = st.button("Register")

    if register_button:
        st.session_state.page = "register"
        st.experimental_rerun()


   
# Function to register a new user
def register_user(username, email, password):
    df = pd.read_csv('users.csv')
    if username in df['Username'].values or email in df['Email'].values:
        return False  # User or email already exists
    new_user = pd.DataFrame({'Username': [username], 'Email': [email], 'Password': [hash_password(password)]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv('users.csv', index=False)
    return True  # User registered successfully

# Function for the register page
def register_page():
    add_custom_css()
    st.markdown("<h1>Engineering Course Difficulty Index Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<h1>Register Page</h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    register_button = st.button("Register")

    if register_button:
        if password != confirm_password:
            st.error("Passwords do not match.")
            st.markdown('<style>button:focus { background-color: red !important; }</style>', unsafe_allow_html=True)
        elif register_user(username, email, password):
            st.success("Registration successful! You can log in now.")
            st.session_state.page = "login"
            st.markdown('<style>button:focus { background-color: green !important; }</style>', unsafe_allow_html=True)
            st.experimental_rerun()
        else:
            st.error("Username or email already exists. Choose a different one.")
            st.markdown('<style>button:focus { background-color: red !important; }</style>', unsafe_allow_html=True)

    login_button = st.button("Login")

    if login_button:
        st.session_state.page = "login"
        st.experimental_rerun()

# Difficulty index calculation functions
def calculate_difficulty_index_simple(student_performance, feedback):
    performance_score = (sum(student_performance) / len(student_performance)) / 10
    feedback_score = sum(feedback) / len(feedback)
    difficulty_index = (performance_score + feedback_score) / 2
    return difficulty_index

def calculate_difficulty_index_weighted(student_performance, feedback, weight_performance=0.7, weight_feedback=0.3):
    performance_score = (sum(student_performance) / len(student_performance)) / 10
    feedback_score = sum(feedback) / len(feedback)
    difficulty_index = (weight_performance * performance_score) + (weight_feedback * feedback_score)
    return difficulty_index

def calculate_difficulty_index_harmonic(student_performance, feedback):
    performance_score = (sum(student_performance) / len(student_performance)) / 10
    feedback_score = sum(feedback) / len(feedback)
    if performance_score == 0 or feedback_score == 0:
        return 0
    difficulty_index = 2 * (performance_score * feedback_score) / (performance_score + feedback_score)
    return difficulty_index

# Map feedback categories to numerical values
feedback_mapping = {
    "More Difficult": 10,
    "Medium Difficult": 5,
    "Less Difficult": 2
}

# Function to visualize the data using Plotly
def visualize_data(course_data):
    fig = px.bar(course_data, x='Course', y='Difficulty Index', color='Difficulty Index',
                 title='Course Difficulty Index',
                 labels={'Difficulty Index': 'Difficulty Index'},
                 hover_data={'Difficulty Index': ':.2f'})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

def add_footer():
    st.markdown("---")
    st.subheader("Contact Us")
    st.write("Connect with us on social media:")
    st.markdown("[LinkedIn](https://www.linkedin.com/)")
    st.markdown("[Twitter](https://twitter.com/)")
    st.markdown("[Facebook](https://www.facebook.com/)")
    st.markdown("[Instagram](https://www.instagram.com/)")
  
def main_page():
    st.set_page_config(layout="wide")

    st.image("1485949524c5.webp", use_column_width=True)

    st.title("Engineering Course Difficulty Index Calculator")
    st.write(f"Welcome, {st.session_state.username}!")

    st.sidebar.image("images.jpeg", use_column_width=True)
    
    st.sidebar.markdown("## About Us")
    if st.sidebar.button("Meet the Team"):
        st.sidebar.image("images.png", caption="RenukaPrasad V G", use_column_width=True)
        st.sidebar.image("images (1).png", caption="Inchara Patel", use_column_width=True)
        st.sidebar.image("images (1).png", caption="Ranjitha ", use_column_width=True)
        st.sidebar.image("images.png", caption="Samrudh", use_column_width=True)

    # Algorithm selection
    st.sidebar.markdown("## Select Algorithm")
    algorithm = st.sidebar.selectbox(
        "Difficulty Index Calculation Algorithm",
        ("Simple Average", "Weighted Average", "Harmonic Mean")
    )

    # Select semester
    st.sidebar.markdown("## Select Semester")
    semester = st.sidebar.selectbox("Semester", range(1, 9))

    # Display courses for the selected semester
    st.sidebar.markdown("## Courses in Selected Semester")
    courses_by_semester = {
        1: ["Engineering Mathematics I", "Engineering Physics", "Engineering Chemistry", "Basic Electrical Engineering"],
        2: ["Engineering Mathematics II", "Engineering Graphics", "Computer Programming", "Basic Electronics"],
        3: ["Engineering Mathematics III", "Data Structures", "Digital Logic Design", "Analog Electronics"],
        4: ["Computer Organization", "Software Engineering", "Operating Systems", "Microprocessors"],
        5: ["Database Management Systems", "Computer Networks", "Theory of Computation", "Design and Analysis of Algorithms"],
        6: ["Compiler Design", "Computer Graphics", "Artificial Intelligence", "Embedded Systems"],
        7: ["Machine Learning", "Big Data Analytics", "Cyber Security", "Cloud Computing"],
        8: ["Project Work", "Internship", "Elective I", "Elective II"]
    }
    courses = courses_by_semester[semester]
    # Display courses in a formatted way
    for course in courses:
        st.sidebar.write(f"- {course}")

    # Display available courses with resources and guides
    st.header("Available Courses with Resources and Guides")
    st.write("Click the button below to view available courses with their resources and guides.")
    if st.button("View Available Courses and Resources"):
        st.session_state.page = "courses_resources"
        st.experimental_rerun()

    # Upload CSV file
    st.sidebar.markdown("## Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if all(column in df.columns for column in ["Course", "Performance", "Feedback"]):
            course_data = []

            for course in courses:
                course_df = df[df['Course'] == course]
                performance_list = course_df['Performance'].tolist()
                feedback_list = course_df['Feedback'].map(feedback_mapping).tolist()
                
                if algorithm == "Simple Average":
                    difficulty_index = calculate_difficulty_index_simple(performance_list, feedback_list)
                elif algorithm == "Weighted Average":
                    difficulty_index = calculate_difficulty_index_weighted(performance_list, feedback_list)
                elif algorithm == "Harmonic Mean":
                    difficulty_index = calculate_difficulty_index_harmonic(performance_list, feedback_list)
                
                course_data.append({
                    "Course": course,
                    "Student Performance": performance_list,
                    "Feedback": feedback_list,
                    "Difficulty Index": difficulty_index
                })

            course_df = pd.DataFrame(course_data)
            course_df.sort_values(by='Difficulty Index', ascending=False, inplace=True)
            
            # Display the difficulty index table
            st.header("Course Difficulty Index")
            st.dataframe(course_df.style.format({'Difficulty Index': "{:.2f}"}))

            # Create a new table to display the difficulty index
            st.header("New Difficulty Index Table")
            st.table(course_df[['Course', 'Difficulty Index']].style.format({'Difficulty Index': "{:.2f}"}))

            # Visualization
            st.header("Course Difficulty Index Visualization")
            visualize_data(course_df)

            # Comparison Tool
            st.header("Compare Courses")
            course_selection = st.multiselect("Select courses to compare:", course_df['Course'])
            if course_selection:
                comparison_data = course_df[course_df['Course'].isin(course_selection)]
                st.dataframe(comparison_data.style.format({'Difficulty Index': "{:.2f}"}))
                visualize_data(comparison_data)

            # Additional Metrics
            st.header("Additional Metrics")
            avg_grade = course_df["Student Performance"].apply(lambda x: sum(x) / len(x)).mean()
            st.metric(label="Average Grade", value=avg_grade)

            # Interest-based Course Suggestion
            st.header("Personalized Course Suggestions")
            st.write("Please answer the following questions to help us suggest the best courses for you.")

            col1, col2 = st.columns(2)
            with col1:
                q1 = st.radio("Do you prefer theoretical or practical courses?", ("Theoretical", "Practical"))
                st.image("TERVSPAR.jpg", caption="Theoretical vs Practical", use_column_width=True)
                q2 = st.radio("Do you enjoy programming?", ("Yes", "No"))
                st.image("PROGRAMING11.jpg", caption="Programming", use_column_width=True)
                q3 = st.radio("Do you like working with hardware?", ("Yes", "No"))
                st.image("HARDWARE.jpeg", caption="Working with Hardware", use_column_width=True)
                q4 = st.radio("Do you prefer individual or group projects?", ("Individual", "Group"))
                st.image("individual-vs-group-decision.jpg", caption="Individual vs Group Projects", use_column_width=True)
                q5 = st.radio("Do you enjoy problem-solving?", ("Yes", "No"))
                st.image("PROBLEMSOLVING.jpeg", caption="Problem Solving", use_column_width=True)
            with col2:
                q6 = st.radio("Are you interested in AI and Machine Learning?", ("Yes", "No"))
                st.image("AIML.jpg", caption="AI and Machine Learning", use_column_width=True)
                q7 = st.radio("Do you prefer working on theoretical frameworks?", ("Yes", "No"))
                st.image("THERFRAME.jpeg", caption="Theoretical Frameworks", use_column_width=True)
                q8 = st.radio("Are you interested in developing software applications?", ("Yes", "No"))
                st.image("SOFTWARE.jpeg", caption="Software Development", use_column_width=True)
                q9 = st.radio("Do you prefer coursework with heavy lab work?", ("Yes", "No"))
                st.image("LAB.webp", caption="Lab Work", use_column_width=True)
                q10 = st.radio("Are you interested in data analysis and statistics?", ("Yes", "No"))
                st.image("DATA.jpeg", caption="Data Analysis and Statistics", use_column_width=True)

            if st.button("Get Course Suggestions"):
                suggestions = []
                if semester == 1:
                    if q1 == "Theoretical":
                        suggestions.append("Engineering Mathematics I")
                    else:
                        suggestions.append("Engineering Physics")
                    if q3 == "Yes":
                        suggestions.append("Basic Electrical Engineering")
                    if q5 == "Yes":
                        suggestions.append("Engineering Chemistry")
                elif semester == 2:
                    if q1 == "Theoretical":
                        suggestions.append("Engineering Mathematics II")
                    else:
                        suggestions.append("Engineering Graphics")
                    if q2 == "Yes":
                        suggestions.append("Computer Programming")
                    if q3 == "Yes":
                        suggestions.append("Basic Electronics")
                elif semester == 3:
                    if q1 == "Theoretical":
                        suggestions.append("Engineering Mathematics III")
                    else:
                        suggestions.append("Analog Electronics")
                    if q2 == "Yes":
                        suggestions.append("Data Structures")
                    if q5 == "Yes":
                        suggestions.append("Digital Logic Design")
                elif semester == 4:
                    if q1 == "Theoretical":
                        suggestions.append("Operating Systems")
                    else:
                        suggestions.append("Microprocessors")
                    if q2 == "Yes":
                        suggestions.append("Software Engineering")
                    if q5 == "Yes":
                        suggestions.append("Computer Organization")
                elif semester == 5:
                    if q1 == "Theoretical":
                        suggestions.append("Theory of Computation")
                    else:
                        suggestions.append("Database Management Systems")
                    if q2 == "Yes":
                        suggestions.append("Design and Analysis of Algorithms")
                    if q5 == "Yes":
                        suggestions.append("Computer Networks")
                elif semester == 6:
                    if q1 == "Theoretical":
                        suggestions.append("Artificial Intelligence")
                    else:
                        suggestions.append("Embedded Systems")
                    if q3 == "Yes":
                        suggestions.append("Computer Graphics")
                    if q5 == "Yes":
                        suggestions.append("Compiler Design")
                elif semester == 7:
                    if q1 == "Theoretical":
                        suggestions.append("Machine Learning")
                    else:
                        suggestions.append("Big Data Analytics")
                    if q2 == "Yes":
                        suggestions.append("Cyber Security")
                    if q5 == "Yes":
                        suggestions.append("Cloud Computing")
                elif semester == 8:
                    if q1 == "Theoretical":
                        suggestions.append("Project Work")
                    else:
                        suggestions.append("Internship")
                    if q2 == "Yes":
                        suggestions.append("Elective I")
                    if q5 == "Yes":
                        suggestions.append("Elective II")
                st.write("Recommended Courses based on your interests:")
                st.write(suggestions)
        else:
            st.error("CSV file must contain 'Course', 'Performance', and 'Feedback' columns.")
 # New Feature: Enter Performance and Feedback
    st.header("Enter Your Performance and Feedback")
    st.write("Use the form below to enter your performance and feedback for courses you have completed.")

    with st.form(key='feedback_form'):
        course_name = st.selectbox("Select Course", courses)
        performance = st.slider("Performance (1-100)", 1, 100)
        feedback = st.selectbox("Feedback", ["Excellent", "Good", "Average", "Poor", "Very Poor"])
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Read or initialize the CSV file for saving feedback
            feedback_file = "course_feedback.csv"
            if not os.path.isfile(feedback_file):
                # Create the file if it does not exist
                with open(feedback_file, 'w') as f:
                    f.write("Username,Course,Performance,Feedback\n")

            # Append new feedback with username
            with open(feedback_file, 'a') as f:
                f.write(f"{st.session_state.username},{course_name},{performance},{feedback}\n")

            st.success("Your feedback has been submitted successfully!")
# Function for the courses and resources page
def courses_resources_page():
    st.title("Available Courses with Resources and Guides")

    # Dropdown menu to select the semester
    semester = st.selectbox("Select Semester", range(1, 9))

    # Define the course resources including profile pictures and contact details
    course_resources = {
        1: {
            "Engineering Mathematics I": {
                "resources": ["Textbook: Engineering Mathematics I", "Guide: Basic Math Principles"],
                "guide": {
                    "name": "Dr. John Doe",
                    "profile_pic": "images.png",
                    "contact": "john.doe@example.com"
                }
            },
            "Engineering Physics": {
                "resources": ["Textbook: Engineering Physics", "Guide: Physics Experiments"],
                "guide": {
                    "name": "Dr. Jane Smith",
                    "profile_pic": "images (1).png",
                    "contact": "jane.smith@example.com"
                }
            },
            "Engineering Chemistry": {
                "resources": ["Textbook: Engineering Chemistry", "Guide: Chemical Reactions"],
                "guide": {
                    "name": "Dr. Alan Brown",
                    "profile_pic": "images (1).png",
                    "contact": "alan.brown@example.com"
                }
            },
            "Basic Electrical Engineering": {
                "resources": ["Textbook: Basic Electrical Engineering", "Guide: Electrical Circuits"],
                "guide": {
                    "name": "Dr. Emily White",
                    "profile_pic": "images.png",
                    "contact": "emily.white@example.com"
                }
            }
        },
        2: {
            "Engineering Mathematics II": {
                "resources": ["Textbook: Engineering Mathematics II", "Guide: Advanced Math Principles"],
                "guide": {
                    "name": "Dr. Michael Green",
                    "profile_pic": "images (1).png",
                    "contact": "michael.green@example.com"
                }
            },
            "Engineering Graphics": {
                "resources": ["Textbook: Engineering Graphics", "Guide: Graphic Design Techniques"],
                "guide": {
                    "name": "Dr. Lisa Gray",
                    "profile_pic": "images.png",
                    "contact": "lisa.gray@example.com"
                }
            },
            "Computer Programming": {
                "resources": ["Textbook: Computer Programming", "Guide: Coding Fundamentals"],
                "guide": {
                    "name": "Dr. Robert Black",
                    "profile_pic": "images (1).png",
                    "contact": "robert.black@example.com"
                }
            },
            "Basic Electronics": {
                "resources": ["Textbook: Basic Electronics", "Guide: Electronic Components"],
                "guide": {
                    "name": "Dr. Susan Blue",
                    "profile_pic": "images.png",
                    "contact": "susan.blue@example.com"
                }
            }
        },
        3: {
            "Engineering Mathematics III": {
                "resources": ["Textbook: Engineering Mathematics III", "Guide: Multivariable Calculus"],
                "guide": {
                    "name": "Dr. Sarah Miller",
                    "profile_pic": "images.png",
                    "contact": "sarah.miller@example.com"
                }
            },
            "Data Structures": {
                "resources": ["Textbook: Data Structures", "Guide: Data Structure Algorithms"],
                "guide": {
                    "name": "Dr. David Wilson",
                    "profile_pic": "images (1).png",
                    "contact": "david.wilson@example.com"
                }
            },
            "Digital Logic Design": {
                "resources": ["Textbook: Digital Logic Design", "Guide: Logic Circuit Design"],
                "guide": {
                    "name": "Dr. Laura Taylor",
                    "profile_pic": "images.png",
                    "contact": "laura.taylor@example.com"
                }
            },
            "Analog Electronics": {
                "resources": ["Textbook: Analog Electronics", "Guide: Analog Circuit Design"],
                "guide": {
                    "name": "Dr. Daniel Harris",
                    "profile_pic": "images (1).png",
                    "contact": "daniel.harris@example.com"
                }
            }
        },
        4: {
            "Computer Organization": {
                "resources": ["Textbook: Computer Organization", "Guide: Computer Architecture"],
                "guide": {
                    "name": "Dr. Emily Johnson",
                    "profile_pic": "images.png",
                    "contact": "emily.johnson@example.com"
                }
            },
            "Software Engineering": {
                "resources": ["Textbook: Software Engineering", "Guide: Software Development Lifecycle"],
                "guide": {
                    "name": "Dr. James Anderson",
                    "profile_pic": "images (1).png",
                    "contact": "james.anderson@example.com"
                }
            },
            "Operating Systems": {
                "resources": ["Textbook: Operating Systems", "Guide: OS Principles"],
                "guide": {
                    "name": "Dr. Olivia Martinez",
                    "profile_pic": "images.png",
                    "contact": "olivia.martinez@example.com"
                }
            },
            "Microprocessors": {
                "resources": ["Textbook: Microprocessors", "Guide: Microprocessor Architecture"],
                "guide": {
                    "name": "Dr. William Thompson",
                    "profile_pic": "images (1).png",
                    "contact": "william.thompson@example.com"
                }
            }
        },
        5: {
            "Database Management Systems": {
                "resources": ["Textbook: Database Management Systems", "Guide: SQL and Database Design"],
                "guide": {
                    "name": "Dr. Ava Robinson",
                    "profile_pic": "images.png",
                    "contact": "ava.robinson@example.com"
                }
            },
            "Computer Networks": {
                "resources": ["Textbook: Computer Networks", "Guide: Network Protocols"],
                "guide": {
                    "name": "Dr. Ethan Clark",
                    "profile_pic": "images (1).png",
                    "contact": "ethan.clark@example.com"
                }
            },
            "Theory of Computation": {
                "resources": ["Textbook: Theory of Computation", "Guide: Computational Theory"],
                "guide": {
                    "name": "Dr. Sophia Lewis",
                    "profile_pic": "images.png",
                    "contact": "sophia.lewis@example.com"
                }
            },
            "Design and Analysis of Algorithms": {
                "resources": ["Textbook: Design and Analysis of Algorithms", "Guide: Algorithm Design Techniques"],
                "guide": {
                    "name": "Dr. Alexander Walker",
                    "profile_pic": "images.png",
                    "contact": "alexander.walker@example.com"
                }
            }
        },
        6: {
            "Compiler Design": {
                "resources": ["Textbook: Compiler Design", "Guide: Compiler Construction"],
                "guide": {
                    "name": "Dr. Isabella Hall",
                    "profile_pic": "images (1).png",
                    "contact": "isabella.hall@example.com"
                }
            },
            "Computer Graphics": {
                "resources": ["Textbook: Computer Graphics", "Guide: Graphics Programming"],
                "guide": {
                    "name": "Dr. Mason Allen",
                    "profile_pic": "images.png",
                    "contact": "mason.allen@example.com"
                }
            },
            "Artificial Intelligence": {
                "resources": ["Textbook: Artificial Intelligence", "Guide: AI Concepts"],
                "guide": {
                    "name": "Dr. Mia Young",
                    "profile_pic": "images (1).png",
                    "contact": "mia.young@example.com"
                }
            },
            "Embedded Systems": {
                "resources": ["Textbook: Embedded Systems", "Guide: Embedded Programming"],
                "guide": {
                    "name": "Dr. Lucas Hernandez",
                    "profile_pic": "images (1).png",
                    "contact": "lucas.hernandez@example.com"
                }
            }
        },
        7: {
            "Machine Learning": {
                "resources": ["Textbook: Machine Learning", "Guide: Machine Learning Algorithms"],
                "guide": {
                    "name": "Dr. Noah King",
                    "profile_pic": "images.png",
                    "contact": "noah.king@example.com"
                }
            },
            "Big Data Analytics": {
                "resources": ["Textbook: Big Data Analytics", "Guide: Data Analysis Techniques"],
                "guide": {
                    "name": "Dr. Emma Scott",
                    "profile_pic": "images (1).png",
                    "contact": "emma.scott@example.com"
                }
            },
            "Cyber Security": {
                "resources": ["Textbook: Cyber Security", "Guide: Security Protocols"],
                "guide": {
                    "name": "Dr. Liam Wright",
                    "profile_pic": "images.png",
                    "contact": "liam.wright@example.com"
                }
            },
            "Cloud Computing": {
                "resources": ["Textbook: Cloud Computing", "Guide: Cloud Architecture"],
                "guide": {
                    "name": "Dr. Olivia Adams",
                    "profile_pic": "images (1).png",
                    "contact": "olivia.adams@example.com"
                }
            }
        },
        8: {
            "Project Work": {
                "resources": ["Guide: Project Planning", "Guide: Project Execution"],
                "guide": {
                    "name": "Dr. Amelia Nelson",
                    "profile_pic": "images (1).png",
                    "contact": "amelia.nelson@example.com"
                }
            },
            "Internship": {
                "resources": ["Guide: Internship Preparation", "Guide: Professional Development"],
                "guide": {
                    "name": "Dr. William Harris",
                    "profile_pic": "images.png",
                    "contact": "william.harris@example.com"
                }
            },
            "Elective I": {
                "resources": ["Guide: Elective I Preparation", "Guide: Elective I Resources"],
                "guide": {
                    "name": "Dr. Harper Lewis",
                    "profile_pic": "images (1).png",
                    "contact": "harper.lewis@example.com"
                }
            },
            "Elective II": {
                "resources": ["Guide: Elective II Preparation", "Guide: Elective II Resources"],
                "guide": {
                    "name": "Dr. Ava Martinez",
                    "profile_pic": "images.png",
                    "contact": "ava.martinez@example.com"
                }
            }
        }
    }

    if semester in course_resources:
        for course, details in course_resources[semester].items():
            st.header(course)
            st.write("**Resources:**")
            for resource in details["resources"]:
                st.write(f"- {resource}")

            st.write("**Guide:**")
            guide = details["guide"]
            st.write(f"Name: {guide['name']}")
            st.image(guide["profile_pic"], caption=guide["name"], width=100)
            st.write(f"Contact: {guide['contact']}")
    else:
        st.write("Resources for the selected semester are not available yet.")

    # Add a button to go back to the main page
    if st.button("Back to Main Page"):
        st.session_state.page = "main"
        st.experimental_rerun()

def main():
    create_user_database()

    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        if st.session_state.page == "main":
            main_page()
        elif st.session_state.page == "courses_resources":
            courses_resources_page()
    elif st.session_state.page == "register":
        register_page()
    else:
        login_page()


if __name__ == "__main__":
    main()
