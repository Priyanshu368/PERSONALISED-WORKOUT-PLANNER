# Problem Statement

Many people struggle to stay fit because they don’t have a personal trainer or a workout plan that fits their needs. Hiring a coach is expensive, and most online workout plans are too general.

This project, AI-Powered Fitness Coach, solves this problem by using AI (GEMINI), Python, Streamlit, and LangChain to:
- Create personalized workout plans based on user details (age, weight, fitness level, goals).
- Provide AI-powered coaching with real-time advice and fitness tips.
- Let users chat with an AI fitness coach to ask workout-related questions.
- Offer a simple, interactive web app (built with Streamlit) for easy access.

With this project, anyone can get a custom fitness plan and coaching for free using AI! 



### Installation Steps



**2. Create a virtual environment**
```bash
conda create -p env python=3.10 -y
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run application**
```bash
streamlit run app.py
```

## Data Flow

1. User inputs workout preferences through the Streamlit UI
2. Application processes these inputs using the workout generator
3. Workout generator creates a prompt and sends it to LangChain
4. LangChain communicates with OpenAI API to generate a personalized workout plan
5. Generated plan is returned and displayed to the user
6. Optional PDF creation for downloading the workout plan
6. Plan is stored in session history for future reference




