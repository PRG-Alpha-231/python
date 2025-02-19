from rest_framework import serializers
from . models import Profile
from . models import InstructorDetails
from . models import *


class InstructorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=InstructorDetails
        fields='__all__'

from .models import PDFDocument

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['id','uploaded_pdf', 'extracted_text']


class ListEndUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        exclude=["password","user_permissions","groups","username","is_active","is_staff","is_superuser"]



class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Institute
        fields="__all__"



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields="__all__"



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"


class StudentProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentDetails
        fields='__all__'
        depth=1



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"








class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentDetails
        fields="__all__"




class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Materials
        fields="__all__"





class QuizQuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuizQuestionPaper
        fields="__all__"






class QuizQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuizQuestions
        fields="__all__"


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Progress
        fields="__all__"





class StudentAnswerPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentAnswerPaper
        fields="__all__"



class StudentNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentNotes
        fields="__all__"

        





