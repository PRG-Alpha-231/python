from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InstructorRegisterSerializer

from .serializers import ListEndUsersSerializer
from rest_framework import status
from.models import Profile
from . serializers import *
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                "refresh": str(refresh),
                "access": str(access_token),
                'role':user.role
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class AdminAddInstructor(APIView):
    def post (self,request):
        data=request.data
        serializer=InstructorRegisterSerializer(data=data)
        serializer_details=InstructorRegisterSerializer(data=data)
        if serializer.is_valid() and serializer_details.is_valid():
            obj=serializer.save()
            ins=serializer_details.save()
            ins.profile=obj
            ins.save()
            obj.set_password(data.get("password"))
            obj.save()
            return Response({'msg':'Instructor added successfuly'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class InstructorAddStudent(APIView):
    def post (self,request):
        data=request.data
        serializer=ProfileSerializer(data=data)
        serializer_details=StudentDetailsSerializer(data=data)
        if serializer.is_valid() and serializer_details.is_valid():
            obj=serializer.save()
            student=serializer_details.save()
            student.profile=obj
            student.save()
            obj.set_password(data.get("password"))
            obj.save()
            return Response({'msg':'Student added successfuly'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class ListEndUsers(APIView):
    def get(self,request):
        role=request.GET.get("role")
        data=Profile.objects.all()
        if role:
            data=data.filter(role=role)
            
        serializer=ListEndUsersSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    


## INSTITUTES APIS ##

class AddInstituteAPIView(APIView):
    def post(self,request):
        serializer=InstituteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'institute addedd successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class UpdateInstitute(APIView):
    def get(self,request):
        institute_id=request.GET.get('institute_id')
        institute=get_object_or_404(Institute,id=institute_id)
        serializer=InstituteSerializer(institute)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def post(self,request):
        institute_id=request.GET.get('institute_id')
        institute=get_object_or_404(Institute,id=institute_id)
        serializer=InstituteSerializer(institute,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'institute edited successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        institute_id=request.GET.get('institute_id')
        institute=get_object_or_404(Institute,id=institute_id)
        institute.delete()
        return Response({'msg':'institute deleted successfully'},status=status.HTTP_200_OK)
    


## DEPARTMENT APIS ##

class AddDepartmentAPIView(APIView):
    def post(self,request):
        serializer=DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'department addedd successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        




class UpdateDepartment(APIView):
    def get(self,request):
        Department_id=request.GET.get('Department_id')
        Department=get_object_or_404(Department,id=Department_id)
        serializer=DepartmentSerializer(Department)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def post(self,request):
        Department_id=request.GET.get('Department_id')
        Department=get_object_or_404(Department,id=Department_id)
        serializer=DepartmentSerializer(Department,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Department edited successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        Department_id=request.GET.get('Department_id')
        Department=get_object_or_404(Department,id=Department_id)
        Department.delete()
        return Response({'msg':'Department deleted successfully'},status=status.HTTP_200_OK)



##  PROFILE APIS ##
class StudentUpdateProfile(APIView):
    def get(self,request):
        student_id=request.GET.get('student_id')
        student=get_object_or_404(StudentDetails,id=student_id)
        serializer=StudentProfileDetailsSerializer(student)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def post(self,request):
        student_id=request.GET.get('student_id')
        student=get_object_or_404(StudentDetails,id=student_id)
        profile_serializer=ProfileSerializer(student.profile,data=request.data,partial=True)
        serializer=StudentProfileDetailsSerializer(student,data=request.data,partial=True)
        if profile_serializer.is_valid() and serializer.is_valid():
            serializer.save()
            profile_serializer.save()
            return Response({'msg':'Profile edited successfully'},status=status.HTTP_200_OK)
        else:
            return Response(profile_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        profile_id=request.GET.get('Profile_id')
        profile=get_object_or_404(Profile,id=profile_id)
        profile.delete()
        return Response({'msg':'Profile deleted successfully'},status=status.HTTP_200_OK)
    



## MATERIALS APIS ##
class AddMaterialsAPIView(APIView):
    def post(self,request):
        file=request.FILES.get('file')
        print(file)
        serializer=MaterialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(file=file)
            return Response({'msg':'Materials addedd successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class UpdateMaterials(APIView):##IS ALSO USED FOR QUESTION PAPER## ##USE DROPDOWN IN CATOGORY TO SPLIT MATERIALS AND QUESTION PAPERS##
    def get(self,request):
        materials_id=request.GET.get('materials_id')
        materials=get_object_or_404(Materials,id=materials_id)
        serializer=MaterialsSerializer(materials)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def post(self,request):
        materials_id=request.GET.get('materials_id')
        materials=get_object_or_404(Materials,id=materials_id)
        serializer=MaterialsSerializer(materials,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Materials edited successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        materials_id=request.GET.get('materials_id')
        materials=get_object_or_404(Materials,id=materials_id)
        materials.delete()
        return Response({'msg':'Materials deleted successfully'},status=status.HTTP_200_OK)



## QuizQuestionPaper APIS ##
class AddQuizQuestionPaperAPIView(APIView):
    def post(self,request):
        serializer=QuizQuestionPaperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'QuizQuestionPaper addedd successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        




class UpdateQuizQuestionPaper(APIView):
    def get(self,request):
        QuizQuestionPaper_id=request.GET.get('paper_id')
        paper=get_object_or_404(QuizQuestionPaper,id=QuizQuestionPaper_id)
        serializer=QuizQuestionPaperSerializer(paper)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def post(self,request):
        QuizQuestionPaper_id=request.GET.get('paper_id')
        paper=get_object_or_404(QuizQuestionPaper,id=QuizQuestionPaper_id)
        serializer=QuizQuestionPaperSerializer(paper,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'QuizQuestionPaper edited successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        QuizQuestionPaper_id=request.GET.get('paper_id')
        quizQuestionPaper=get_object_or_404(QuizQuestionPaper,id=QuizQuestionPaper_id)
        quizQuestionPaper.delete()
        return Response({'msg':'QuizQuestionPaper deleted successfully'},status=status.HTTP_200_OK)



## StudentNotes APIS ##   ## Whiteboard ##
class StudentNotesAPIView(APIView):
    def post(self,request):
        serializer=StudentNotesSerializer(data=request.data)
        student=get_object_or_404(StudentDetails,profile=request.user)
        if serializer.is_valid():
            serializer.save(student=student)
            return Response({'msg':'Addedd successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        




class UpdateStudentNotes(APIView):
    def get(self,request):
        StudentNotes_id=request.GET.get('note_id')
        note=get_object_or_404(StudentNotes,id=StudentNotes_id)
        serializer=StudentNotesSerializer(note)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def post(self,request):
        StudentNotes_id=request.GET.get('note_id')
        note=get_object_or_404(StudentNotes,id=StudentNotes_id)
        serializer=StudentNotesSerializer(note,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Edited successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        StudentNotes_id=request.GET.get('note_id')
        note=get_object_or_404(StudentNotes,id=StudentNotes_id)
        StudentNotes.delete()
        return Response({'msg':'Deleted successfully'},status=status.HTTP_200_OK)
    



    ## CHAT BOT##
    

import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai  # Google Gemini AI SDK

# Load API key securely from environment variables
GOOGLE_API_KEY = "AIzaSyDObz6hewixFs3Hg1v0uMS3JVwToAn2rfs"

# Ensure API key is set
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is missing. Set it in environment variables.")

# Configure Gemini API once
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@api_view(['POST'])
def chatbot_api(request):
    """
    Chatbot API using Google Gemini AI
    """
    user_message = request.data.get('message', '').strip()

    if not user_message:
        return Response({'error': 'Message cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

    response_data = get_answer(user_message)

    if response_data:
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Chatbot is currently unavailable. Please try again later.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


def get_answer(question):
    """
    Fetches chatbot data and generates a response using Gemini AI.
    """
    prompt = f"""
    Please analyze the following text and answer the question concisely:

    Question: {question}

    Provide a direct answer without repeating the question.

    Additionally, respond in a friendly way if the message is casual, like 'hi' or 'hello'. and act like skillmentor chatbot 
    """

    try:
        response = model.generate_content(prompt)
        if response and response.candidates:
            answer = response.candidates[0].content.parts[0].text.strip()
            return {'response': answer}
        else:
            return False
    except Exception as e:
        print(f"Error in AI response: {e}")
        return False
