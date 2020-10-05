import django_filters

from .models import *

class MemberFilter(django_filters.FilterSet):
    '''Custom filter for Members'''
    first_name = django_filters.CharFilter(label="First Name", field_name="first_name", lookup_expr='icontains')
    last_name = django_filters.CharFilter(label="Last Name", field_name="last_name", lookup_expr='icontains')
    phone_number = django_filters.NumberFilter(label="Phone", field_name="phone_number")
    client_member_id = django_filters.NumberFilter(label="Member ID", field_name="client_member_id")
    account_id = django_filters.NumberFilter(label='Account ID')

    class Meta:
        model= Member
        fields = ['first_name', 'last_name', 'phone_number', 'client_member_id','account_id']

