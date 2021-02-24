from django.contrib import admin

from common.models import FeedBack, Complaint, News, DiscussionQuestion, Answer

# Registering models for admin page
admin.site.register(FeedBack)
admin.site.register(Complaint)
admin.site.register(News)
admin.site.register(DiscussionQuestion)
admin.site.register(Answer)