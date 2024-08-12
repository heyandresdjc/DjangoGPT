from django.contrib import admin
from app.models import TrainingFile


@admin.register(TrainingFile)
class UserAdmin(admin.ModelAdmin):
    pass
