from django.contrib import admin

from quiz.models import Category, ExamType, Question, Test, TestTaker

admin.site.register(Category)
admin.site.register(ExamType)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(TestTaker)
