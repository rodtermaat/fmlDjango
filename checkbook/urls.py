from django.urls import path
from .views import CheckCreate, CheckDelete, CheckUpdate, CategoryPopUp, CategoryCreate, CategoryDelete, CategoryUpdate
from . import views
#from . import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar', views.fmlCalendar, name='calendar'),
    path('calendar/<int:aYear>/<int:aMonth>/', views.fmlCalendar, name='calendarNav'),
    path('checkbookList', views.checkbookList, name='checkbook'),
    path('checks/', views.CheckListView.as_view(), name='check-list'),
    path('check/add/', views.CheckCreate.as_view(), name='check-add'),
    path('check/<int:pk>/', views.CheckUpdate.as_view(), name='check-detail'),
    path('check/<int:pk>/delete/', CheckDelete.as_view(), name='check-delete'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    #path('category/addcpu/', views.CategoryCreate.as_view(), name='category-cpu'),
    path('category/addcpu/', views.CategoryPopUp.as_view(), name='category-cpu'),
    path('category/add/', views.CategoryCreate.as_view(), name='category-add'),
    path('category/<int:pk>/', views.CategoryUpdate.as_view(), name='category-detail'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='category-delete'),
]
