from django.contrib import admin
from .models import Chama, ChamaMembership

@admin.register(Chama)
class ChamaAdmin(admin.ModelAdmin):
    list_display = ('name', 'goal_amount', 'invite_code', 'created_at')
    search_fields = ('name', 'invite_code')
    readonly = ('invite_code', 'created_at')

@admin.register(ChamaMembership)
class ChamaMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'chama', 'role', 'joined_at')
    list_filter = ('role', 'chama')
    search_fields = ('user__username', 'chama__name')
    readonly_fields = ('joined_at',)
