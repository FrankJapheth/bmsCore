from django.contrib.auth.models import User

from .bms_base_models.organizations import Organization
from .bms_base_models.departments import Department
from .bms_base_models.members import Member


class OrganizationModel:
    ORGANIZATION = None

    def __init__(self):
        self.ORGANIZATION = Organization()

    def create_organization(self, organization_details: dict, org_user: User) -> Organization:
        self.ORGANIZATION.organization_domain = organization_details['organizationDomain']
        self.ORGANIZATION.organization_name = organization_details['organizationName']
        self.ORGANIZATION.organization_mail_server = organization_details['mailServer']
        self.ORGANIZATION.creator = org_user
        self.ORGANIZATION.save()

        return self.ORGANIZATION


class DepartmentModel:
    DEPARTMENT = None

    def __init__(self):
        self.DEPARTMENT = Department()

    def create_department(self, department_details: dict, department_organization: Organization) -> DEPARTMENT:
        self.DEPARTMENT.department_id = department_details['departmentId']
        self.DEPARTMENT.department_name = department_details['departmentName']
        self.DEPARTMENT.department_organization = department_organization
        self.DEPARTMENT.save()

        return self.DEPARTMENT


class MemberModel:
    MEMBER = None

    def __init__(self):
        self.MEMBER = Member()

    def create_member(self, member_details: dict, member_user: User, member_department: Department) -> Member:
        self.MEMBER.member_id = member_details['memberId']
        self.MEMBER.member_user = member_user
        self.MEMBER.member_department = member_department
        self.MEMBER.save()

        return self.MEMBER

    def get_members(self, member_details: dict) -> list:
        members: list = []

        if member_details['userId'] != '':
            members = Member.objects.filter(member_user__username=member_details['userId'],status='Activate')

        return members


class UserModel:
    USER = None

    def __init__(self):
        self.USER = User()

    def create_user(self, user_details: dict) -> User:
        self.USER.first_name = user_details['firstName']
        self.USER.last_name = user_details['lastName']
        self.USER.email = user_details['userEmail']
        self.USER.username = user_details['username']
        self.USER.set_password(user_details['password'])

        self.USER.save()

        return self.USER
