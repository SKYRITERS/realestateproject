from django.contrib import admin

from .models import Inquery

class InqueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','listing', 'email', 'contact_date') #The fields that will be displayed in the admin area  
    list_display_links = ('id', 'name') #The fields that will have links  
    search_fields = ('name', 'listing', 'email')
    list_per_page = 25

admin.site.register(Inquery, InqueryAdmin)