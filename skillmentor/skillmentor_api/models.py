from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    INSTRUCTOR = 'Instructor', 'Instructor'
    USER = 'User', 'User'


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Institute(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    institute = models.ForeignKey(
        'Institute', on_delete=models.CASCADE, null=True, blank=True, related_name='institute_departments'
    )

    def __str__(self):
        return self.name


class Profile(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    role = models.CharField(max_length=50, choices=RoleChoices.choices)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.email} -- {self.role}'


class Subject(BaseModel):
    subject_name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=True, blank=True, related_name='subjects'
    )

    def __str__(self):
        return self.subject_name


class InstructorDetails(BaseModel):
    profile = models.OneToOneField(
        'Profile', on_delete=models.CASCADE, null=True, blank=True, related_name="instructor_profile"
    )
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE, null=True, blank=True, related_name="instructor_subjects"
    )
    qualification = models.CharField(max_length=100)
    institute= models.ForeignKey('Institute', on_delete=models.CASCADE, null=True, blank=True, related_name='institute_profiles')

    def __str__(self):
        return self.profile.email if self.profile else "No Profile"


class StudentDetails(BaseModel):
    profile = models.OneToOneField(
        'Profile', on_delete=models.CASCADE, null=True, blank=True, related_name="student_profile"
    )
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE, null=True, blank=True, related_name="student_subjects"
    )
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.profile.email if self.profile else "No Profile"


class Materials(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50)
    file = models.FileField(null=True, blank=True)
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE, null=True, blank=True, related_name='materials'
    )

    def __str__(self):
        return self.name


class QuizQuestionPaper(BaseModel):
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE, null=True, blank=True, related_name='question_papers'
    )
    paper_name = models.CharField(max_length=50)
    total_marks = models.FloatField(default=0)
    time_duration = models.DurationField(null=True)
    questions = models.ManyToManyField('QuizQuestions', blank=True)

    def __str__(self):
        return self.paper_name


class QuizQuestions(BaseModel):
    class AnswerChoices(models.TextChoices):
        OPTION_A = "A", "Option A"
        OPTION_B = "B", "Option B"
        OPTION_C = "C", "Option C"
        OPTION_D = "D", "Option D"

    question = models.CharField(max_length=255)
    mark = models.IntegerField(default=1)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=1,
        choices=AnswerChoices.choices,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.question


class StudentAnswerPaper(BaseModel):
    question_paper = models.ForeignKey(
        'QuizQuestionPaper', on_delete=models.CASCADE, null=True, blank=True, related_name='answer_papers'
    )

    def __str__(self):
        return f"Answer Paper for {self.question_paper}"
    



class Flashcards(BaseModel):
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE, null=True, blank=True, related_name='flashcards'
    )
    question= models.CharField(max_length=255)
    answer = models.CharField(max_length=255)



class StudentNotes(BaseModel):
    student = models.ForeignKey(
        'StudentDetails', on_delete=models.CASCADE, null=True, blank=True, related_name='StudentNotes'
    )
    category= models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    title = models.CharField(null=True,max_length = 250)
    whiteboard=models.FileField(null=True,blank=True)


    def __str__(self):
        return f"notes  {self.title}"
    

class Progress(BaseModel):
    student = models.ForeignKey(
        'StudentDetails', on_delete=models.CASCADE, null=True, blank=True, related_name='progress'
    )
    materials = models.ForeignKey(
        'Materials', on_delete=models.CASCADE, null=True, blank=True, related_name='progress'
    )
    marks = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
  
    def __str__(self):
        return f"progress for {self.student}"