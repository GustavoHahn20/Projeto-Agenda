from django.shortcuts import get_object_or_404, redirect, render
from . import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib import messages

# Create your views here.

def home(request):
    contacts = models.Contact.objects.filter(show=True).order_by('id')
    paginator = Paginator( contacts, 5 )
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj' : page_obj,
        'contacts': contacts
    }
    return render(request, ('agenda/home.html'), context)


def contact(request, contactId):
    Singlecontacts = get_object_or_404(models.Contact, id=contactId, show = True)
    Singlecontacts = models.Contact.objects.get(id=contactId)
    context = {
        'contact': Singlecontacts
    }
    return render(request, ('agenda/contact.html'), context)


def search(request):
    searchValue = request.GET.get('q','').strip()
    if searchValue == '':
        return redirect('agenda:home')
    contacts = models.Contact.objects.filter(
            Q(firstName__icontains = searchValue)|
            Q(lastName__icontains = searchValue)|
            Q(phone__icontains = searchValue)|
            Q(email__icontains = searchValue),
            show=True
        )
    paginator = Paginator( contacts, 5 )
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj' : page_obj,
        'contacts': contacts,
        'searchValue' : searchValue
    }
    return render(request, 'agenda/home.html', context)


def createContact(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Somente usuário podem cadastrar contatos')
        return redirect('agenda:home')

    if request.method == 'POST':
        models.Contact.objects.create(
            firstName=request.POST.get('firstName'),
            lastName=request.POST.get('lastName'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            description=request.POST.get('description'),
            show=True,
            category= models.Category.objects.get(id=request.POST.get('category')),
        )
        return redirect('agenda:home')
    categorias = models.Category.objects.all()
    context = {
        'categories': categorias
    }
    return render(request, 'agenda/createContact.html', context)

def updateContact(request, contactId):
    Singlecontacts = get_object_or_404(models.Contact, id=contactId, show = True)
    Singlecontacts = models.Contact.objects.get(id=contactId)
    if request.method == 'POST':
        contact = models.Contact.objects.get(id=contactId)
        contact.phone = request.POST.get('phone')
        contact.email = request.POST.get('email')
        contact.description = request.POST.get('description')
        contact.category = models.Category.objects.get(id=request.POST.get('category'))
        contact.save()
        return redirect('agenda:home')
    categorias = models.Category.objects.all()
    context = {
        'contact': Singlecontacts,
        'categories': categorias
    }
    return render(request, 'agenda/updateContact.html', context)

def deleteContact(request, ContactId):
    contact = get_object_or_404(models.Contact, id=ContactId)
    contact.delete()
    return redirect('agenda:home')

def loginPage(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(request, username=user, password=password)
        if user is not None:
            login_user(request, user)
            messages.success(request, 'Login efetuado com sucesso')
            return redirect("agenda:home")
        else:
            messages.error(request, 'Usuario ou senha invalidos')
            return redirect("agenda:login")
    return render(request, 'agenda/login.html')

def logoutPage(request):
    logout(request)
    messages.success(request, 'Usuario deslogado com sucesso')
    return redirect('agenda:home')

def registerPage(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if password != password2:
            messages.error(request, 'As senhas não são iguais')
            return redirect("agenda:register")
        if User.objects.filter(user=user).exists():
            messages.error(request, 'Usuário já existe')
            return redirect("agenda:register")
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email já existe')
            return redirect("agenda:register")
        user = User.objects.create_user(user, email, password)
        login_user(request, user)
        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect("agenda:home")
    return render(request, 'agenda/register.html')