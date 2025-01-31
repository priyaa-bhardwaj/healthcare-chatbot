import requests 
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse,Http404
from .models import CustomUser,Question, Appointment
from .serializers import *
from django.utils.timezone import now
from django.conf import settings

def home(request):
    return HttpResponse("hello")

class UserDetails(APIView):
    def get(self,request):
        user=CustomUser.objects.all()
        serializer=UserSerializer(user, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
class UserEdit(APIView):
    def get_obj(self,pk):
        try:
            user=CustomUser.objects.get(pk=pk)
            return user
        except CustomUser.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        user=self.get_obj(pk)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    def put(self,request,pk):
        user=self.get_obj(pk)
        serializer=UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request,pk):
        user=self.get_obj(pk)
        user.delete()
        return Response('OK')
    
class ChatBot(APIView):
    def get(self, request):
        """Retrieve all chatbot interactions"""
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer=QuestionSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data["user"]
            question=serializer.validated_data["question"]
            response=self.get_response(question)
            chat=Question.objects.create(user=user,question=question,answer=response)
            return Response({"question":question,"response":response})
        return Response(serializer.errors)
        
    def get_response(self,question):
        url = "http://127.0.0.1:1234/v1/chat/completions"  # LM Studio's API endpoint
        headers = {"Content-Type": "application/json"}

        prompt = f"""
        You are a healthcare chatbot designed to provide possible cause and remedy for both physical and mental health symptoms.  
        Your responses should be short along with **medically safe, research-backed, and concise**.  
        In addition to identifying possible causes and remedies, consider the user's behavior, stress levels, and emotional well-being.  
        If a symptom is serious or suggests a mental health crisis, advise the user to consult a doctor or mental health professional.  

        User: {question}  
        AI: *Possible Cause:* [Identify potential medical, lifestyle, or psychological reasons]  
        AI: *Remedy:* [Provide safe treatments, self-care tips, and coping strategies]  

        - If symptoms suggest high stress, anxiety, or emotional distress, recommend mindfulness techniques, relaxation exercises, or seeking professional counseling.  
        - If symptoms indicate lifestyle-related issues (e.g., poor sleep, diet, exercise), guide the user toward healthy habits.  
        - If the condition is unclear or potentially serious, strongly advise consulting a doctor or therapist.  
        """

        payload = {
            "model": "llama-3.2-1b-instruct",  # Use the correct model identifier from LM Studio
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200  # Limit response length
        }

        try:
            response=requests.post(url,headers=headers,data=json.dumps(payload))
            response_data=response.json()
            return response_data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return "Error: Unable to connect to LLaMA model. Please check the server."
        
class CreateAppointment(APIView):
    def get(self,request):
        appointment=Appointment.objects.all()
        serializer=AppointmentSerializer(appointment, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class UserAppointment(APIView):
    def get_obj(self,pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        appointment=self.get_obj(pk)
        serializer=AppointmentSerializer(appointment)
        return Response(serializer.data)
    def put(self,request,pk):
        appointment=self.get_obj(pk)
        serializer=AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request,pk):
        appointment=self.get_obj(pk)
        appointment.delete()
        return Response("Appointment deleted")

class AllResponse(APIView):
    def get(self,request):
        question=Question.objects.all()
        serializer=QuestionSerializer(question, many=True)
        return Response(serializer.data)
class UserResponse(APIView):
    def get(self,request,pk):
        try:
            user=CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response("User not found")
        questions=Question.objects.filter(user=user)
        serializer=QuestionSerializer(questions, many=True)
        return Response(serializer.data)
