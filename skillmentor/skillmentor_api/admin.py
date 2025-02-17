from django.contrib import admin
from.models import Profile
from.models import *


admin.site.register(Profile)
admin.site.register(InstructorDetails)
admin.site.register(StudentDetails)
admin.site.register(Subject)
admin.site.register(Institute)
admin.site.register(Materials)
admin.site.register(QuizQuestionPaper)
admin.site.register(StudentNotes)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'institute', 'created_at', 'updated_at')  # Columns to display
    list_filter = ('institute',)  # Filter by institute
    search_fields = ('name', 'description')  # Search by name and description
    ordering = ('created_at',)  # Order by creation date


admin.site.register(Department, DepartmentAdmin)