from django.urls import path
from . import views


urlpatterns=[
   path("AdminAddInstructor",views.AdminAddInstructor.as_view()),
   path("login",views.LoginView.as_view()),

   path("ListEndUsers",views.ListEndUsers.as_view()),
   path("InstructorAddsStudent/",views.InstructorAddStudent.as_view()),

   ## institute
   path("add_institute/",views.AddInstituteAPIView.as_view()),
   path("update_institute/",views.UpdateInstitute.as_view()),



   ## DEPARTMENTS ##
   path("add_Department/",views.AddDepartmentAPIView.as_view()),
   path("update_Department/",views.UpdateDepartment.as_view()),



   ## PROFILES ##
   path("StudentUpdateProfile/",views.StudentUpdateProfile.as_view()),



   ## MATERIALS ##
   path("add_materials/",views.AddMaterialsAPIView.as_view()),
   path("update_materials/",views.UpdateMaterials.as_view()),




   ## QuizQuestionPaper ##
   path("AddQuizQuestionPaper/",views.AddQuizQuestionPaperAPIView.as_view()),
   path("update_QuizQuestionPaper/",views.UpdateQuizQuestionPaper.as_view()),


   ## Student Notes ##
   path("StudentNotesAPIView/",views.StudentNotesAPIView.as_view()),
   path("UpdateStudentNotes/",views.UpdateStudentNotes.as_view()),

      ## Chat bot ##
   path("chatbot_api/",views.chatbot_api),

]  

 
  