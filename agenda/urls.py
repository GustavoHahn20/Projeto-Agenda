from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.home, name = 'home'),
    #path('contact/<int:contactId>', views.contact, name = 'contact'),
    path('search/', views.search, name = 'search'),
    

    path('login/', views.loginPage, name= 'login'),
    path('logout/', views.logoutPage, name= 'logout'),
    path('register/', views.registerPage, name= 'register'),
    
    #CRUD
    path('contact/<int:contactId>/detail', views.contact, name = 'contact'),
    path('contact/create', views.createContact, name = 'create'),
    path('contact/<int:contactId>/update', views.updateContact, name = 'update'),
    path('contact/<int:contactId>/delete', views.deleteContact, name = 'delete'),
]
