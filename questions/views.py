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