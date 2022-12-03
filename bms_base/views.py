import datetime

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Department
from .models import DepartmentModel
from .models import Member
from .models import MemberModel
from .models import Organization
from .models import OrganizationModel
from .models import User
from .models import UserModel

MAIL_VERIFICATION_CODES = []


def json_resp(resp_data):
    bms_base_json_response = {'backendResponse': resp_data}
    resp = JsonResponse(bms_base_json_response, safe=False)
    resp["Access-Control-Allow-Origin"] = "*"
    resp["Author"] = "adedefranklyne@gmail.com"
    return resp


@api_view(['POST'])
def create_org(request):
    # states (0, 1, 2)
    # 0=error
    # 1=organizationCreated
    # 2=organizationExists
    organization_details = request.data
    create_org_response = {

        'state': 0,
        'organizationName': '',
        'organizationDomain': '',
        'organizationMailServer': ''
    }
    org_user = User.objects.get(username=organization_details['orgUser'])

    try:

        current_org = Organization.objects.get(organization_domain=organization_details['organizationDomain'])
        create_org_response['state'] = 2
        create_org_response['organizationName'] = current_org.organization_name
        create_org_response['organizationDomain'] = current_org.organization_domain
        create_org_response['organizationMailServer'] = current_org.organization_mail_server

    except Organization.DoesNotExist:
        org_model = OrganizationModel()
        created_org: Organization = org_model.create_organization(organization_details, org_user)
        create_org_response['state'] = 1
        create_org_response['organizationName'] = created_org.organization_name
        create_org_response['organizationDomain'] = created_org.organization_domain
        create_org_response['organizationMailServer'] = created_org.organization_mail_server

    return json_resp(create_org_response)


@api_view(['POST'])
def create_department(request):
    # states (0, 1, 2)
    # 0=error
    # 1=departmentCreated
    # 2=departmentExists
    department_details = request.data
    create_department_response = {
        'state': 0,
        'departmentId': '',
        'departmentName': '',
        'departmentOrganizationId': ''
    }

    try:
        current_dept = Department.objects.get(department_id=department_details['departmentId'])
        create_department_response['state'] = 2
        create_department_response['departmentId'] = current_dept.department_id
        create_department_response['departmentName'] = current_dept.department_name
    except Department.DoesNotExist:
        dep_org = Organization.objects.get(organization_domain=department_details['orgDomain'])
        dep_model = DepartmentModel()
        department_details: Department = dep_model.create_department(department_details, dep_org)
        create_department_response['state'] = 1
        create_department_response['departmentId'] = department_details.department_id
        create_department_response['departmentName'] = department_details.department_name
        create_department_response[
            'departmentOrganizationId'] = department_details.department_organization.organization_domain

    return json_resp(create_department_response)


@api_view(['POST'])
def add_member(request):
    # states (0, 1, 2)
    # 0=error
    # 1=memberAdded
    # 2=memberExists
    member_details: dict = request.data
    add_member_response: dict = {
        'state': 0,
        'memberId': '',
        'memberUserId': '',
        'memberUserLastLogin': '',
        'memberDepartmentId': '',
        'memberDepartmentName': '',
        'memberOrganizationId': '',
        'memberOrganizationName': '',

    }
    member_user = User.objects.get_by_natural_key(member_details['memberUserId'])
    member_department = Department.objects.get(department_id=member_details['memberDepartmentId'])
    create_member_details = {
        'memberId': member_user.first_name.lower() + '.' + member_user.last_name.lower() + '@' +
                    member_department.department_organization.organization_domain
    }
    try:
        current_member = Member.objects.get(member_user__username=member_user.username)
        add_member_response['state'] = 2
        add_member_response['memberId'] = current_member.member_id
        add_member_response['memberUserId'] = current_member.member_user.username
        add_member_response['memberUserLastLogin'] = current_member.member_user.last_login
        add_member_response['memberDepartmentId'] = current_member.member_department.department_id
        add_member_response['memberDepartmentName'] = current_member.member_department.department_name
    except Member.DoesNotExist:
        member_model = MemberModel()
        created_member: Member = member_model.create_member(create_member_details, member_user, member_department)
        add_member_response['state'] = 1
        add_member_response['memberId'] = created_member.member_id
        add_member_response['memberUserId'] = created_member.member_user.username
        add_member_response['memberUserLastLogin'] = created_member.member_user.last_login
        add_member_response['memberDepartmentId'] = created_member.member_department.department_id
        add_member_response['memberDepartmentName'] = created_member.member_department.department_name
        add_member_response[
            'memberOrganizationId'] = created_member.member_department.department_organization.organization_domain
        add_member_response[
            'memberOrganizationName'
        ] = created_member.member_department.department_organization.organization_name

    return json_resp(add_member_response)


@api_view(['POST'])
def authenticate_user(request):
    # states (0, 1, 2)
    # 0=error
    # 1=signIn
    # 2=signUp
    # 3=member
    # 4=notMember
    # 5=exists
    user_details = request.data
    sign_up_response = {
        'state': 0,
        'userFirstName': '',
        'userLastName': '',
        'dateJoined': '',
        'lastLogin': '',
        'memberShips': [],
        'emailAddress': '',
        'username': ''
    }

    user: User = authenticate(username=user_details['username'], password=user_details['password'])

    if user is not None:
        user.save()
        sign_up_response['userFirstName'] = user.first_name
        sign_up_response['userLastName'] = user.last_name
        sign_up_response['lastLogin'] = user.last_login
        sign_up_response['dateJoined'] = user.date_joined
        sign_up_response['emailAddress'] = user.email
        sign_up_response['username'] = user.username
        sign_up_response['state'] = 1
        member_model = MemberModel()
        member_details = {'userId': user_details['username']}
        memberships = member_model.get_members(member_details)

        if len(memberships) <= 0:
            sign_up_response['state'] = 4

        else:
            for membership in memberships:
                org_members_departments: list = []
                org_departments = Department.objects.filter(
                    department_organization__organization_domain=
                    membership.member_department.department_organization.organization_domain)

                for org_department in org_departments:
                    department_members = Member.objects.filter(
                        member_department__department_id=membership.member_department.department_id
                    )
                    department_members_to_send = []

                    for department_member in department_members:
                        department_member_details = {
                            'memberId': department_member.member_id,
                            'memberName': department_member.member_user.first_name + ' ' +
                                          department_member.member_user.last_name
                        }
                        department_members_to_send.append(department_member_details)

                    org_members_department = {
                        'departmentId': org_department.department_id,
                        'departmentOrgId': membership.member_department.department_organization.organization_domain,
                        'name': org_department.department_name
                    }
                    org_members_departments.append(org_members_department)

                membership_details = {
                    'memberId': membership.member_id,
                    'memberUserId': membership.member_user.username,
                    'memberDateJoined': membership.member_date_joined,
                    'departmentId': membership.member_department.department_id,
                    'departmentName': membership.member_department.department_name,
                    'departmentMail': membership.member_department.department_mail_account,
                    'departmentMembers': department_members_to_send,
                    'organizationId': membership.member_department.department_organization.organization_domain,
                    'organizationMailServer':
                        membership.member_department.department_organization.organization_mail_server,
                    'organizationCreator':
                        membership.member_department.department_organization.creator.username,
                    'organizationName': membership.member_department.department_organization.organization_name,
                    'organizationDepartments': org_members_departments
                }

                sign_up_response['memberShips'].append(membership_details)

            sign_up_response['state'] = 3
        user.last_login = datetime.datetime.now()
    else:

        try:
            User.objects.get(username=user_details['username'])
            sign_up_response['state'] = 5
        except User.DoesNotExist:
            user_model = UserModel()
            created_user: User = user_model.create_user(user_details)
            sign_up_response['userFirstName'] = created_user.first_name
            sign_up_response['userLastName'] = created_user.last_name
            sign_up_response['lastLogin'] = created_user.last_login
            sign_up_response['dateJoined'] = created_user.date_joined
            sign_up_response['emailAddress'] = created_user.email
            sign_up_response['username'] = created_user.username
            sign_up_response['state'] = 2
            created_user.save()

    return json_resp(sign_up_response)


@api_view(['POST'])
def check_user_exists(request):
    username = request.data['username']

    check_user_exists_response = {
        'exists': False
    }

    try:
        User.objects.get(username=username)
        check_user_exists_response['exists'] = True
    except User.DoesNotExist:
        check_user_exists_response['exists'] = False

    return json_resp(check_user_exists_response)


@api_view(['POST'])
def verify_email(request):
    user_id = request.data['userId']
    code = request.data['code']

    verify_email_response = {
        'state': 0,
        'verified': False
    }

    user_verification_credentials = {}

    current_time = datetime.datetime.now()
    idx = 0
    for user_credential in MAIL_VERIFICATION_CODES:

        if user_credential['userId'] == user_id:
            user_verification_credentials = user_credential
        else:
            delta = current_time - user_credential['time']
            time_in_minutes = delta.total_seconds() / 60
            print(time_in_minutes)
            if time_in_minutes > 30:
                MAIL_VERIFICATION_CODES.pop(idx)

        idx += 1

    if user_verification_credentials['code'] == code:
        verify_email_response['state'] = 1
        verify_email_response['verified'] = True

    return json_resp(verify_email_response)


@api_view(['POST'])
def get_department_details(request):
    department_id = request.data['departmentId']

    org_department = Department.objects.get(department_id=department_id)

    org_dep_members = Member.objects.filter(member_department__department_id=department_id)

    org_members_to_send = []

    for org_dep_member in org_dep_members:
        org_dept_member_to_send = {
            'memberId': org_dep_member.member_id,
            'memberName': org_dep_member.member_user.first_name + ' ' + org_dep_member.member_user.last_name
        }
        org_members_to_send.append(org_dept_member_to_send)

    dep_details = {
        'organization': org_department.department_organization.organization_domain,
        'departmentMembers': org_members_to_send,
        'departmentMail': org_department.department_mail_account,
    }

    return json_resp(dep_details)


@api_view(['POST'])
def change_org_owner(request):
    user_id = request.data['username']
    org_id = request.data['OrgDomain']

    new_org_owner = User.objects.get_by_natural_key(user_id)
    org_to_change = Organization.objects.get(organization_domain=org_id)

    org_to_change.creator = new_org_owner

    org_to_change.save()

    return json_resp(True)


@api_view(['POST'])
def get_system_user(request):
    user_identity = request.data['username']
    organization_domain = request.data['organizationDomain']

    system_user_members = Member.objects.filter(
        member_department__department_organization__organization_domain=organization_domain,
        member_user__username__icontains=user_identity
    )

    searched_users_to_send = []

    for user_member in system_user_members:
        searched_member = {
            'username': user_member.member_user.username,
            'firstName': user_member.member_user.first_name,
            'lastName': user_member.member_user.last_name,
            'emailAddress': user_member.member_user.email
        }
        searched_users_to_send.append(searched_member)

    return json_resp(searched_users_to_send)
