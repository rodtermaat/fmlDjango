from django.urls import path
from .views import CheckCreate, CheckDelete, CheckUpdate, CategoryPopUp
from .views import CategoryCreate, CategoryDelete, CategoryUpdate, cat_pie, CatData
from . import views
#from . import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('api/data', cat_pie, name='api-data'),
    path('api/chart/data', CatData.as_view()),

    path('calendar', views.fmlCalendar, name='calendar'),
    path('calendar/<int:aYear>/<int:aMonth>/', views.fmlCalendar, name='calendarNav'),

    path('checkbookList', views.checkbookList, name='checkbook'),
    path('checkbookMonth', views.checkbookMonth, name='checkbook-month'),
    path('checkbookMonth/<int:aYear>/<int:aMonth>/', views.checkbookMonth, name='checkbook-monthNav'),

    path('checks/', views.CheckListView.as_view(), name='check-list'),
    path('check/add/', views.CheckCreate.as_view(), name='check-add'),
    path('check/<int:pk>/', views.CheckUpdate.as_view(), name='check-detail'),
    path('check/<int:pk>/delete/', CheckDelete.as_view(), name='check-delete'),
    path('check/addbill/', views.addCheckBills, name='add-bill'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    #path('category/addcpu/', views.CategoryCreate.as_view(), name='category-cpu'),
    path('category/addcpu/', views.CategoryPopUp.as_view(), name='category-cpu'),
    path('category/add/', views.CategoryCreate.as_view(), name='category-add'),
    path('category/<int:pk>/', views.CategoryUpdate.as_view(), name='category-detail'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='category-delete'),
]

#this is a comment to test git update
