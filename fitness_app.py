from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from loguru import logger
import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')

if gemini_api_key:
    logger.info('API KEY IS AVAILABLE')
else:
    logger.error('API KEY IS NOT AVAILABLE')

# Initialize the model
try:
    model = ChatGoogleGenerativeAI(model='gemini-1.5-pro', api_key=gemini_api_key, temperature=0.7)
except Exception as e:
    logger.error(f'MODEL INITIALIZATION ERROR: {str(e)}')

# Define the workout plan prompt template
workout_plan_template = PromptTemplate(
    template=(
        "Create a personalized workout plan for a {fitness_level} individual. "
        "Their goal is {goal}. The workout should last {duration} minutes and "
        "use {equipment}. Provide a step-by-step exercise plan."
    ),
    input_variables=['fitness_level', 'goal', 'duration', 'equipment']
)

# Function to generate a workout plan
def generate_workout(fitness_level, goal, duration, equipment):
    prompt = workout_plan_template.invoke({
        'fitness_level': fitness_level,
        'goal': goal,
        'duration': duration,
        'equipment': equipment
    })

    try:
        response = model.invoke(prompt)
        logger.info('Workout plan successfully generated')
        return response.content  # Extract content
    except Exception as e:
        logger.error(f'Error Generating Workout: {str(e)}')
        return f'An Error Occurred: {str(e)}'

# Function to create a PDF
def create_pdf(workout_plan, fitness_level, goal, duration, equipment):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Personalized Workout Plan", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Fitness Level: {fitness_level}", ln=True)
    pdf.cell(200, 10, txt=f"Goal: {goal}", ln=True)
    pdf.cell(200, 10, txt=f"Duration: {duration} minutes", ln=True)
    pdf.cell(200, 10, txt=f"Equipment: {equipment}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, workout_plan)

    filename = f"Workout_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Streamlit App
def main():
    st.set_page_config(page_title="Workout Planner", layout="centered")
    
    st.markdown("""
    <style>
        .main { background-color: green; padding: 20px; border-radius: 10px; }
        .stButton>button { background-color:white; color: black; border-radius: 5px; }
        .stSelectbox, .stNumberInput {  border-radius: 2px; }
        h1 { color: yellow; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.title("Personalized Workout Planner")
    st.markdown("Generate a custom workout plan tailored to your needs!")

    # Sidebar for inputs
    with st.sidebar:
        st.header('Workout Preferences')
        fitness_level = st.selectbox('Fitness Level', ['Beginner', 'Intermediate', 'Advanced'])
        goal = st.selectbox('Goal', ['Weight Loss', 'Muscle Gain', 'Endurance', 'General Fitness'])
        duration = st.number_input('Duration (in minutes)', min_value=30, max_value=120, value=30, step=5)
        equipment = st.selectbox('Equipment Available', ['Bodyweight', 'Dumbbells', 'Gym Equipment', 'Resistance Bands'])

        generate_button = st.button('Generate Workout Plan')

    if 'workout_history' not in st.session_state:
        st.session_state.workout_history = []

    if generate_button:
        with st.spinner('Generating Workout Plan...'):
            workout_plan = generate_workout(fitness_level, goal, duration, equipment)
            st.session_state.workout_history.append({
                'plan': workout_plan,
                'fitness_level': fitness_level,
                'goal': goal,
                'duration': duration,
                'equipment': equipment,
                'date': datetime.now().strftime('%Y-%m-%d')
            })

            st.success('Workout Plan Generated Successfully!')
            st.subheader('Your Workout Plan')
            st.write(workout_plan)

            # Download as PDF
            pdf_file = create_pdf(workout_plan, fitness_level, goal, duration, equipment)
            with open(pdf_file, 'rb') as file:
                st.download_button(label="Download as PDF", data=file, file_name=pdf_file, mime='application/pdf')

            # Workout History
            if st.session_state.workout_history:
                st.subheader('Workout History')
                for i, history in enumerate(st.session_state.workout_history):
                    with st.expander(f"Workout {i+1} - {history['date']}"):
                        st.write(f"**Fitness Level:** {history['fitness_level']}")
                        st.write(f"**Goal:** {history['goal']}")
                        st.write(f"**Duration:** {history['duration']} minutes")
                        st.write(f"**Equipment:** {history['equipment']}")
                        st.write(f"**Workout Plan:** {history['plan']}")

if __name__ == '__main__':
    main()
