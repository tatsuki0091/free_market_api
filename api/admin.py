from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models
# Register your models here.



# 今回はユーザクラスをカスタマイズするのでUserAdminクラスをadminファイル内で
# のオーバーライドが必要
class UserAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('personal Info'), {'fields': ()}),
        (
            _('permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('important dates'), {'fields':('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')
        }),
    )

# djangoのダッシュボードにモデル構造を登録
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Comment)