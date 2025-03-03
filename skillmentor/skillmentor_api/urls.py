from django.urls import path

from skillmentor import settings

from . import views
from django.conf.urls.static import static



urlpatterns=[
   path("AdminAddInstructor",views.AdminAddInstructor.as_view()),
   path("login",views.LoginView.as_view()),

   path("ListEndUsers",views.ListEndUsers.as_view()),
   path("InstructorAddsStudent/",views.InstructorAddStudent.as_view()),


   path("AdminRegistration/",views.AdminRegistration.as_view()),




   ## institute
   path("add_institute/",views.AddInstituteAPIView.as_view()),
   path("update_institute/",views.UpdateInstitute.as_view()),



   ## DEPARTMENTS ##
   path("add_Department/",views.AddDepartmentAPIView.as_view()),
   path("update_Department/",views.UpdateDepartment.as_view()),
   path('institutes/<int:institute_id>/departments/', views.InstituteDepartmentsView.as_view(), name='institute-departments'),
   
   ##subjects##
   path('subjects/', views.SubjectListCreateView.as_view(), name='subject-list-create'),
   path('subjects/<int:pk>/', views.SubjectRetrieveUpdateDestroyView.as_view(), name='subject-detail'),

   ## PROFILES ##
   path("StudentUpdateProfile/",views.StudentUpdateProfile.as_view()),



   ## MATERIALS ##
   path("add_materials/",views.AddMaterialsAPIView.as_view()),
   path("update_materials/",views.UpdateMaterials.as_view()),



   ## QuizQuestionPaper ##
   path("AddQuizQuestionPaper/",views.AddQuizQuestionPaperAPIView.as_view()),
   path("add_questions/",views.AddQuestionsAPIView.as_view()),
   path("update_QuizQuestionPaper/",views.UpdateQuizQuestionPaper.as_view()),


   ## Student Notes ##
   path("StudentNotesAPIView/",views.StudentNotesAPIView.as_view()),
   path("UpdateStudentNotes/",views.UpdateStudentNotes.as_view()),


      ## Chat bot ##
   path("chatbot_api/",views.chatbot_api),


   ## ADD PROGRESS ##
   path("AddMaterialProgress/",views.AddProgressForMaterial.as_view()),  
   path("ViewMyProgress/",views.AddProgressForMaterial.as_view()),  


   ## PDF CHAT ##
   path("doc_upload/",views.PDFUploadView.as_view()),
   path("doc_chatbot/",views.DocChatbotAPIView.as_view()),

]  
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
  