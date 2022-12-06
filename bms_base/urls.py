from django.urls import path
from . import views

urlpatterns = [
    path('authenticate', views.authenticate_user, name='authenticate'),
    path('checkUserExists', views.check_user_exists, name='checkUserExists'),
    path('verifyUser', views.verify_email, name='verifyUser'),
    path('editOrganization', views.create_org, name='editOrganization'),
    path('editDepartment', views.create_department, name='editDepartment'),
    path('editMember', views.add_member, name='editMember'),
    path('getDepartmentDetails', views.get_department_details, name='getDepartmentDetails'),
    path('changeOrgOwner', views.change_org_owner, name='changeOrgOwner'),
    path('searchMembers', views.get_system_user, name='searchMembers'),
    path('searchOrgs', views.search_organizations, name='searchOrgs'),
    path('changeMemberStatus', views.change_user_status, name='changeMemberStatus')
]
