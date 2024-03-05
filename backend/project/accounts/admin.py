from django.contrib import admin
from accounts.models import User,Chats,Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
class UserModelAdmin(BaseUserAdmin):
   
    list_display = ["id", "email", "name", "tc", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []


class ChatsAdmin(admin.ModelAdmin):
    list_editable=['is_read']

    list_display=['sender','receiver','message','is_read']




class ProfileAdmin(admin.ModelAdmin):
    list_display= ['user','full_name','verified']
    search_fields = ['user__name','full_name']
    list_filter = ['verified']  # Corrected list_filter



admin.site.register(User, UserModelAdmin)
admin.site.register(Chats,ChatsAdmin)
admin.site.register(Profile,ProfileAdmin)