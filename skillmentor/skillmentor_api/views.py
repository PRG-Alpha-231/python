from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

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


from rest_framework.decorators import api_view
import google.generativeai as genai  # Google Gemini AI SDK

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        print(password)

        if not email or not password:
            return Response({"detail": "email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        print(user)
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


class AdminRegistration(APIView):
    def post (self,request):
        data=request.data.copy()
        data['role']=RoleChoices.ADMIN
        serializer=ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'admin registered successfully','admin':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ProfileSerializer, InstructorRegisterSerializer
from .utils import generate_password  # Ensure this function exists

User = get_user_model()  # Correct user model import

class AdminAddInstructor(APIView):
    def post(self, request):
        print("Received data:", request.data)  # Debugging

        data = request.data.copy()  # Create a mutable copy of request data
        email = data.get("email")

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate password if not provided
        if not data.get("password"):  # Check if password is missing or empty
            data["password"] = generate_password()

        serializer = ProfileSerializer(data=data)
        serializer_details = InstructorRegisterSerializer(data=data)

        profile_valid = serializer.is_valid()
        instructor_valid = serializer_details.is_valid()

        if profile_valid and instructor_valid:
            obj = serializer.save()
            obj.set_password(data["password"])  # Set password properly
            obj.save()

            ins = serializer_details.save()
            ins.profile = obj
            ins.save()

            print(f"Instructor {obj.email} added successfully!")  # Debugging
            return Response({'msg': 'Instructor added successfully'}, status=status.HTTP_201_CREATED)

        # Print validation errors safely
        if not profile_valid:
            print("Profile Serializer Errors:", serializer.errors)  
        if not instructor_valid:
            print("Instructor Serializer Errors:", serializer_details.errors)  

        return Response({
            'profile_errors': serializer.errors if not profile_valid else None,
            'instructor_errors': serializer_details.errors if not instructor_valid else None
        }, status=status.HTTP_400_BAD_REQUEST)



import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Example usage
password = generate_password(16)  # Generates a 16-character password
print("Generated Password:", password)


class InstructorAddStudent(APIView):
    def post (self,request):
        data=request.data
        user=request.user
        serializer=ProfileSerializer(data=data)
        serializer_details=StudentDetailsSerializer(data=data)
        if serializer.is_valid() and serializer_details.is_valid():
            obj=serializer.save(institute=user.institute)
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
        data=request.data
        admin_id=data.get('admin_id')
        if not admin_id:
            return Response({'msg':'admin id required'},status=status.HTTP_400_BAD_REQUEST)
     
        user=get_object_or_404(Profile,id=admin_id)
        serializer=InstituteSerializer(data=request.data)
        if serializer.is_valid():
            institute=serializer.save()
            user.institute=institute
            user.save()
            return Response({'msg':'institute addedd successfully','data':serializer.data},status=status.HTTP_201_CREATED)
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
    


## Subject APIS###

class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectListCreateView(generics.ListCreateAPIView):
    """ View to list all subjects and create a new subject """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ View to retrieve, update, or delete a specific subject """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer



## DEPARTMENT APIS ##
class AddDepartmentAPIView(APIView):
    def post(self,request):
        serializer=DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'department addedd successfully','data':serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class InstituteDepartmentsView(APIView):
    
    def get(self, request, institute_id):
        print(institute_id)
        try:
            institute = Institute.objects.get(id=institute_id)
        except Institute.DoesNotExist:
            return Response({"error": "Institute not found"}, status=404)

        departments = Department.objects.filter(institute=institute)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)     


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
        
class AddQuestionsAPIView(APIView):
    def post(self,request):
        paper_id=request.data.get('paper_id')
        if not paper_id:
            return Response({'msg':'paper_id is required'},status=status.HTTP_400_BAD_REQUEST)
        
        paper=get_object_or_404(QuizQuestionPaper,id=paper_id)
        serializer=QuizQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            question=serializer.save()
            paper.questions.add(question)
            paper.save()
            return Response({'msg':'Questions addedd successfully'},status=status.HTTP_201_CREATED)
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


class AddProgressForMaterial(APIView):
    def post(self,request):
        material_id=request.data.get('material_id')
        marks=request.data.get('marks')
        total_marks=request.data.get('total_marks')
        student=get_object_or_404(StudentDetails,profile=request.user)
        material=get_object_or_404(Materials,id=material_id)
        progress=Progress.objects.create(student=student,materials=material,marks=marks,total_marks=total_marks,percentage=(marks/total_marks)*100,completed=True)
        return Response({'msg':'Progress status changed successfully'},status=status.HTTP_201_CREATED)
    

class ViewMyProgress(APIView):
    def get(self, request):
        student_id = request.GET.get('student_id')
        subject=request.GET.get('subject')
        student = get_object_or_404(StudentDetails, id=student_id)
        progress_records = Progress.objects.filter(student=student)

        total_progress = Materials.objects.filter(subject=subject).count()
        completed_progress = progress_records.filter(completed=True).count()

        progress_percentage = (completed_progress / total_progress * 100) if total_progress > 0 else 0
        serializer = ProgressSerializer(progress_records, many=True)

        return Response({
            "progress_details": serializer.data,
            "total_progress": total_progress,
            "completed_progress": completed_progress,
            "progress_percentage": round(progress_percentage, 2)
        }, status=status.HTTP_200_OK)




## chatbot using document data ##

from rest_framework.parsers import MultiPartParser, FormParser
import fitz  # PyMuPDF
from .models import PDFDocument
from .serializers import PDFDocumentSerializer
import google.generativeai as genai

class PDFUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PDFDocumentSerializer(data=request.data)
        if serializer.is_valid():
            pdf_document = serializer.save()
            self.extract_text_from_pdf(pdf_document)
            return Response(PDFDocumentSerializer(pdf_document).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_pdf(self, pdf_document):
        pdf_file_path = pdf_document.uploaded_pdf.path
        document = fitz.open(pdf_file_path)
        
        text = ""
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text += page.get_text()

        pdf_document.extracted_text = text
        pdf_document.save()



class DocChatbotAPIView(APIView):
    def post(self, request):
        data = request.data
        document_id=request.data.get('document_id')
        doc = get_object_or_404(PDFDocument,id=document_id)
        question = data.get('question')

        prompt = f"""
        Please analyze the following document and answer the question.
        
        Question: {question}
        
        Document Content:
        {doc.extracted_text}
        
        Please provide a clear and concise answer based on the document content above.
        """
        
        # Using Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        try:
            response = model.generate_content(prompt)
            answer = response.text.strip()
            print(answer)
            
            return Response({
                'answer': answer,
                'status': 'success'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Error processing your request',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

