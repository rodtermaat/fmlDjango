from django.shortcuts import render
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django import forms

#function pagination
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Check, Category

from django_addanother.widgets import AddAnotherWidgetWrapper
from django_addanother.views import CreatePopupMixin

from .calendar import CheckbookCalendar
from calendar import monthrange

from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from datetime import date, datetime

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_checks=Check.objects.all().count()
    tot_bal=Check.objects.all().aggregate(Sum('amount'))
    today_bal=Check.objects.filter(dater__lte=date.today()).aggregate(Sum('amount'))
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'checkbook/index.html',
        context={'num_checks':num_checks,'tot_bal':tot_bal, 'today_bal':today_bal,
            'num_visits':num_visits},
    )

def checkbookList(request):
    check_list = Check.objects.all()
    #checks = Check.objects.all()
    page = request.GET.get('page', 1)

    balance = 0
    #for chk in checks:
    for chk in check_list:
        balance += chk.amount
        chk.balance = balance

    paginator = Paginator(check_list, 20)
    try:
        checks = paginator.page(page)
    except PageNotAnInteger:
        checks = paginator.page(1)
    except EmptyPage:
        checks = paginator.page(paginator.num_pages)

    return render(request, 'checkbook/checkbook.html', {'checks': checks})


from django.views import generic

class CheckListView(generic.ListView):
    model = Check
    paginate_by = 10

class CheckDetailView(generic.DetailView):
    model = Check

class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ['dater', 'type', 'category', 'name', 'amount', 'cleared']
        widgets = {
            'dater': forms.TextInput(attrs={'class':'datepicker'}),
            'category': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('category-cpu'),)
        }

class CheckCreate(CreateView):
    form_class = CheckForm
    model = Check
    success_url = reverse_lazy('checkbook')

class CheckUpdate(UpdateView):
    model = Check
    success_url = reverse_lazy('checkbook')
    fields = ['dater', 'type', 'category', 'name', 'amount', 'cleared']
    #template_name_suffix = '_update_form'

class CheckDelete(DeleteView):
    model = Check
    success_url = reverse_lazy('checkbook')

# should be able to remove check-list from program now.

# Category views
# --------------------------------------------
class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10

class CategoryDetailView(generic.DetailView):
    model = Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'frequency', 'budget']

class CategoryPopUpForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'frequency', 'budget']


#class CategoryCreate(CreatePopupMixin, CreateView):
class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')

class CategoryPopUp(CreatePopupMixin, CreateView):
    model = Category
    form_class = CategoryPopUpForm
    template_name_suffix = '_popup_form'

class CategoryUpdate(UpdateView):
    model = Category
    success_url = reverse_lazy('category-list')
    fields = ['name', 'frequency', 'budget']
    template_name_suffix = '_update_form'

class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')

# calendar views
# - - - - - - - -
from django.http import HttpResponse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
import calendar

#def fmlCalendar(request):
#    c = calendar.HTMLCalendar(calendar.MONDAY)
#    y = date.today().year
#    m = date.today().month
#    myCal = c.formatmonth(y,m)
#    return render(request, 'checkbook/calendar.html', {'fmlCalendar': mark_safe(myCal)})

def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return date(1900, pMonthNumber, 1).strftime('%B')

def fmlCalendar(request, aYear=date.today().year , aMonth=date.today().month):
    #cal = calendar.HTMLCalendar(calendar.MONDAY)
    curYear = int(aYear)
    curMonth = int(aMonth)
    #fmlCal = cal.formatmonth(curYear,curMonth)

    CalendarFromMonth = datetime(aYear, aMonth, 1)
    CalendarToMonth = datetime(aYear, aMonth, monthrange(aYear, aMonth)[1])
    CheckEntries = Check.objects.filter(dater__gte=CalendarFromMonth, dater__lte=CalendarToMonth)
    fmlCal = CheckbookCalendar(CheckEntries).formatmonth(aYear, aMonth)

    PreviousYear = curYear
    PreviousMonth = curMonth - 1
    if PreviousMonth == 0:
        PreviousMonth = 12
        PreviousYear = curYear - 1
    NextYear = curYear
    NextMonth = curMonth + 1
    if NextMonth == 13:
        NextMonth = 1
        NextYear = curYear + 1

    return render(request, 'checkbook/calendar.html', {'fmlCalendar' : mark_safe(fmlCal),
                                                       'Month' : curMonth,
                                                       'MonthName' : named_month(curMonth),
                                                       'Year' : curYear,
                                                       'PreviousMonth' : PreviousMonth,
                                                       'PreviousMonthName' : named_month(PreviousMonth),
                                                       'PreviousYear' : PreviousYear,
                                                       'NextMonth' : NextMonth,
                                                       'NextMonthName' : named_month(NextMonth),
                                                       'NextYear' : NextYear,
                                                   })

# def fmlCalendarNav(request, aYear=date.today().year, aMonth=date.today().month):
#     cal = calendar.HTMLCalendar(calendar.MONDAY)
#     curYear = int(aYear)
#     curMonth = int(aMonth)
#     fmlCal = cal.formatmonth(curYear,curMonth)
#
#     PreviousYear = curYear
#     PreviousMonth = curMonth - 1
#     if PreviousMonth == 0:
#         PreviousMonth = 12
#         PreviousYear = curYear - 1
#     NextYear = curYear
#     NextMonth = curMonth + 1
#     if NextMonth == 13:
#         NextMonth = 1
#         NextYear = curYear + 1
#
#     return render(request, 'checkbook/calendar.html', {'fmlCalendar' : mark_safe(fmlCal),
#                                                        'Month' : curMonth,
#                                                        'MonthName' : named_month(curMonth),
#                                                        'Year' : curYear,
#                                                        'PreviousMonth' : PreviousMonth,
#                                                        'PreviousMonthName' : named_month(PreviousMonth),
#                                                        'PreviousYear' : PreviousYear,
#                                                        'NextMonth' : NextMonth,
#                                                        'NextMonthName' : named_month(NextMonth),
#                                                        'NextYear' : NextYear,
#                                                    })
