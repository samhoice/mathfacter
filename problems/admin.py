from django.contrib import admin

from .models import Rule, Question, Answer

# Register your models here.

admin.site.register(Rule)
admin.site.register(Question)
admin.site.register(Answer)
