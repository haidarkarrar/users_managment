from django.contrib import admin
from manage_users.models import Company, Profile, User

# Register your models here.

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Profile)
