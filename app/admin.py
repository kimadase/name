from django.contrib import admin
from app import models


# Register your models here.
@admin.register(models.GPWBattle)
class GPWBattleadmin(admin.ModelAdmin):
    pass
