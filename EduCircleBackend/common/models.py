import datetime
import os
import random
import uuid

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):

    # Unique ID as the Primary Key instead of the default Integer Primary Key
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False,
                           verbose_name='unique id')

    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='creation date')
    modified_at = models.DateTimeField(db_index=True, auto_now=True, blank=True, null=True,
                                       verbose_name='last modified')


    description = models.CharField(_('Description'), max_length=1500, blank=True,null=True, default='')

    class Meta:
        # To prevent it's migration, we set it as abstract
        abstract = True


class FeedBack(BaseModel):
    from users.models import User 

    #: Created By
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='feedback_created_by',
                                   null=True, blank=True)

    rating = models.CharField(_('Rating'), max_length=100, blank=True,null=True, default='5')

    title = models.CharField(_('Title'), max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'FeedBacks'

    def __str__(self):
        return self.title    


class Complaint(BaseModel):

    from users.models import User 

    title = models.CharField(_('Title'), max_length=1000, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='complaint_created_by',
                                   null=True, blank=True)

    targeted_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='complaint_target_user',
                                   null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Complaints'

    def __str__(self):
        return self.title


class News(BaseModel):
    """
    Latest news about anything
    """
    from users.models import User 

    title = models.CharField(_('Title'), max_length=1000, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='news_created_by',
                                null=True, blank=True)

    site_link = models.CharField(_('Site Link'), max_length=1000, blank=True,null=True, default='')

    class Meta:
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


class DiscussionQuestion(BaseModel):
    """
    A Question that was submitted to the forum.
    """
    from users.models import User 
    from quiz.models import ExamType

    title = models.CharField(_('Title'), max_length=1000, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='question_created_by',
                                null=True, blank=True)

    question_text = models.CharField(_('Question text'), max_length=2000, blank=True,null=True, default='')

    exam_type = models.ForeignKey(ExamType, on_delete=models.SET_NULL, related_name='question_type',
                            null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Discussions'

    def __str__(self):
        return self.title


class Answer(BaseModel):
    """
    The answers on the discussion platform for a given question.
    """
    from users.models import User 

    title = models.CharField(_('Title'), max_length=1000, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='answer_created_by',
                                null=True, blank=True)

    text = models.CharField(_('Answer text'), max_length=2000, blank=True,null=True, default='')

    up_votes = models.IntegerField(_('Up votes'), default=0)
    down_votes = models.IntegerField(_('Down votes'), default=0)


    def __str__(self):
        return self.title

