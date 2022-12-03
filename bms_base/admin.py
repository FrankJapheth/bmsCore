from django.contrib import admin

from .bms_base_models.organizations import Organization
from .bms_base_models.departments import Department
from .bms_base_models.members import Member

# Register your models here.

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Member)
