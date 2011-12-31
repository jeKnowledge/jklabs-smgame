from gamecore.models import Company, Investment, GEvent, MenuItem, Proposal, EventComment
from django.contrib import admin

class MenuItemList(admin.ModelAdmin):
    list_display = ('menu_name', 'link_url')

admin.site.register(Company)
admin.site.register(Investment)
admin.site.register(GEvent)
admin.site.register(MenuItem,MenuItemList)
admin.site.register(Proposal)
admin.site.register(EventComment)
