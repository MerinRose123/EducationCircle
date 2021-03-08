import datetime
import os
import random
import uuid

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from common.models import BaseModel

PAPER_TYPES = (
    ("mock_test", "Mock Test"),
    ("prev_year", "Previous Year"),
    ("quiz", "Category based quiz"),
)

QUESTION_TYPES = (
    ("MCQ", "Multiple Choice"),
    ("true_false", "True or False"),
    ("numeric", "Numerical"),
)

class Category(BaseModel):
    """
    The categories of the question. eg: maths, history etc
    """
    title = models.CharField(_('Title'), max_length=180, null=True, blank=True, default='')

    key = models.CharField(_('Key'), max_length=180, null=True, blank=True)

    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class ExamType(BaseModel):
    """
    The types of the question. eg: SSC, PSC etc
    """
    from users.models import User

    title = models.CharField(_('Title'), max_length=180, null=True, blank=True, default='')

    key = models.CharField(_('Key'), max_length=180, null=True, blank=True)

    site_link = models.CharField(_('Site Link'), max_length=1000, null=True, blank=True)

    community_leader = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='community_leader',
                                   null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Exam Types'

    def __str__(self):
        return self.title
    

class Question(BaseModel):
    """
    The questions
    """
    title = models.CharField(_('Title'), max_length=180, null=True, blank=True, default='')

    question_text = models.CharField(_('Question text'), max_length=2000, blank=True,null=True, default='')

    question_type = models.CharField(max_length=100, choices=QUESTION_TYPES,default="MCQ",)

    choice1 = models.CharField(_('choice1'), max_length=200, default='')
    choice2 = models.CharField(_('choice2'), max_length=200, default='')
    choice3 = models.CharField(_('choice3'),max_length=200, default='')
    choice4 = models.CharField(_('choice4'), max_length=200, default='')

    answer = models.CharField(max_length=200, default='choice1')

    # many to many Link to category
    categories = models.ManyToManyField('Category', blank=True, related_name='category')
    
    class Meta:
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title



class Test(BaseModel):
    """
    Test can be a mock test, a previous year question or a quiz
    """
    title = models.CharField(_('Title'), max_length=180, null=True, blank=True, default='')

    # Paper Type: mock_test, previous year question paper or quiz
    paper_type = models.CharField(max_length=100, choices=PAPER_TYPES,default="quiz")

    # The number of questions in the test
    no_questions = models.IntegerField(_('No of Questions'), null=True, blank=True, default=0)

    # If the test type is mock test or previous year question then exam type is filled
    exam_type = models.ForeignKey(ExamType, on_delete=models.SET_NULL, related_name='exam_type',
                                   null=True, blank=True)
    
    # If the test is a category based quiz like current affairs, aptitude etc
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='test_category',
                                   null=True, blank=True)

    # Year in the case of previous year question paper
    year = models.IntegerField(_('Test Year'), null=True, blank=True)

    # many to many Link to questions
    questions = models.ManyToManyField('Question', blank=True, related_name='question_test')
    
    class Meta:
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.title
    

class TestTaker(BaseModel):
    """
    To store the results of a user's attended tests
    """
    from users.models import User 

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='test_user',
                                   null=True, blank=True)

    test = models.ForeignKey(Test, on_delete=models.SET_NULL, related_name='test',
                                null=True, blank=True)
                            
    score = models.IntegerField(default=0)

    total_score = models.IntegerField(default=0)

    percentage = models.IntegerField(default=0)

    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Test Takers'

    def __str__(self):
        return self.user