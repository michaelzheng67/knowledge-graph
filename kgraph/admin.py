from django.contrib import admin

from .models import Question, Choice, Category, Info

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Category)
admin.site.register(Info)