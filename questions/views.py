"""
from django.shortcuts import render      #Imports Django’s render function, so the HTML file can be loaded, and then it combines it with Django, and sends it to browser.
from django.http import JsonResponse

import json

def home(request):  #so that what it sent to the browser can be viewed, this line creates a view function named home. The view function takes a request object as an argument, which contains information about the incoming HTTP request.
    

    return render(request, "index.html")    #This makes a request - find index.html, render it and send to browser
def generate_questions(request):            #This is acting like an API endpoint.

    if request.method == "POST":            #This line indicates that this view function will only handle POST requests (Post requests sends data). When a POST request is made to this endpoint, the code inside this block will be executed.

        data = json.loads(request.body)     #The body there means the raw data sent in the POST request. This line takes the raw data from the request body, which is expected to be in JSON format, and converts it into a Python dictionary using json.loads().

        job_title = data.get("job_title")   #This line retrieves the value associated with the key "job_title" from the data dictionary. This value is expected to be provided in the POST request and represents the job title for which interview questions will be generated.


        questions = [

            f"What interests you about this {job_title} role?",

            f"What skills makes you a good fit for the role of a {job_title}?",

            f"How would you handle challenges in a {job_title} position?"
        ]


        return JsonResponse({
            "questions": questions
        })
"""

from django.shortcuts import render
from django.http import JsonResponse
import json
from openai import OpenAI
import os
from dotenv import load_dotenv



load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def home(request):

    return render(request, "index.html")



def generate_questions(request):

    if request.method == "POST":

        data = json.loads(request.body)

        job_title = data.get("job_title")


        prompt = f"""
        Generate 3 thoughtful interview questions
        for a {job_title} role. 
        
        Return only the questions, without any numbering or bullet points on a new line
       
        """
        
        try:
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content


            questions = [

                question.strip()

                for question in answer.split("\n")

                if question.strip()
            ]


            return JsonResponse({
                "questions": questions
            })
           

        except Exception as e:
            return JsonResponse({
            "error": str(e)
            }, status=500)
    
    return JsonResponse({
    "error": "Invalid request method"
}, status=400)