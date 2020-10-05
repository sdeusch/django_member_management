from .filters import MemberFilter
from .models import Member, Account
from .parser import Parser
from .serializers import MemberSerializer
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from rest_framework.response import Response
from rest_framework.views import APIView


def Members(request, context={}):
    '''Loads Members applying the custom MemberFilter and a Paginator'''
    if request.method == 'GET' and 'account_id' in request.GET and request.GET['account_id'] != '':
        ac_id = request.GET['account_id']
        members = [account.member for account in Account.objects.filter(account_id=ac_id)]
        paginator = Paginator(members, 50)
        context['myFilter'] = MemberFilter(request.GET)
    else:
        members = Member.objects.all()
        myFilter = MemberFilter(request.GET, queryset=members)
        members = myFilter.qs
        paginator = Paginator(members, 50)
        context['myFilter'] = myFilter

    page = request.GET.get('page', 1)
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    context['members'] =  members
    template = loader.get_template('Members/Members.html')
    return HttpResponse(template.render(context, request))


def details(request, id):
    '''Loads the Detail view of a Member. This includes a list of all Accounts this user is a member of'''
    try:
        member=Member.objects.get(pk=id)
        accounts = Account.objects.filter(member = member)
    except Member.DoesNotExist:
        raise Http404("Member Not Available")
    return render(request, 'Members/detail.html', {'member': member, 'accounts': accounts})


def details_delete(request, id):
    '''Delete a member instance'''
    member=get_object_or_404(Member, pk=id)
    if request.method == 'POST':  # If method is POST,
        member.delete()           # delete the member
        return redirect('/')


def upload_list(request):
    '''Present the upload CSV file page'''
    return render(request, 'upload.html')


def upload_csv(request):
    '''Actual Uploads CSV file endpoint'''
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        parser = Parser(name)
        parser.process_csv(name)
        context['url'] = fs.url(name)
        print(f"Uploaded file {uploaded_file.name} of size {uploaded_file.size}")
    return render(request, 'upload_csv.html', context)



class memberList(APIView):
    '''Actual API view a GET request, with search filter MemberFilter and pagination, e.g. &size=N&page=2 '''
    def get(self, request):
        members = Member.objects.all()
        myFilter = MemberFilter(request.GET, queryset=members)
        members = myFilter.qs

        page_size = request.GET.get('size', 100)
        paginator = Paginator(members, page_size)
        page = request.GET.get('page', 1)
        try:
            members = paginator.page(page)
        except PageNotAnInteger:
            members = paginator.page(1)
        except EmptyPage:
            members = paginator.page(paginator.num_pages)

        serializer=MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self):
        pass