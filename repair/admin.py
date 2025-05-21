from django.contrib import admin
from .models import RepairRequest

@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('car', 'user__username', 'problem')

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != 'new':
            return False
        return super().has_change_permission(request, obj)
