from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from loguru import  logger
# Load environment variables
load_dotenv()

gemini_api_key=os.getenv('gemini_api_key')
if gemini_api_key:
    logger.info('API KEY IS AVAILABLE')
else:
    logger.error('API KEY IS NOT AVAILABLE')

# Initialize the model 
try:

    model = ChatGoogleGenerativeAI(model='gemini-1.5-pro',api_key=gemini_api_key,temperature=0.7)
except Exception as e:
    logger.error(f'MODEL INITIALIZATION ERROR: {str(e)}' ,"error")
                 
# Define the workout plan  prompt template 
workout_plan_template = PromptTemplate(
    template=('Create a personlized workout plan for a {fitness_level} individual, whose  goal is {goal}. The workout should be last {duration} minutes.And use {equipment} equipments  .Give step by step exercise.'),
    input_variables=['fitness_level','goal','duration','equipment']

)
#  function to generate  a workout  plan

def  generate_workout(fitness_level,goal,duration ,equipment):
    prompt=workout_plan_template.invoke({
        'fitness_level':fitness_level,
        'goal':goal,
        'duration':duration ,
        'equipment':equipment
    }
    )
    try:
        response=model.invoke(prompt)
        logger.info('Workout plan successfully generated')
        return response.content # Extract Content
    except Exception as e:
        logger.error(f' Error Generating Workout: {str(e)}' ,"error")
        return f'An Error Occured:{str(e)}'
    

    # Test the function
if __name__=='__main__':
    test_workout=generate_workout('Beginner','Weight gain','23','Bodyweight')
    print(test_workout)





