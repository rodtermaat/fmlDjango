from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Check(models.Model):

    """
    Model representing a checkbook transaction.
    """
    check_type = (('CR', 'credit'),('DR', 'debit'),('SV', 'savings'),('DT', 'debt reduction'),)
    #theuser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dater = models.DateField(help_text=' .the date of the transaction')
    type = models.CharField(max_length=2, choices=check_type, help_text=' .credit or debit')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, help_text=' .description')
    amount = models.IntegerField(default=0, help_text=' .amount')
    cleared = models.BooleanField(help_text=' .cleared with the bank?')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["dater"]

    def __str__(self):
        return f'{self.dater} {self.name} {self.amount}'

    def short_description(self):
        return self.name[:25]

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this transaction.
        """
        return reverse('check-detail', kwargs={'pk': self.pk})

class Category(models.Model):

    """
    Model representing a Category.
    """
    name = models.CharField(max_length=100, help_text=' .category name')
    frequency = models.CharField(max_length=10, null=True, blank=True, help_text=' .M(monthly) or W(weekly)')
    budget = models.IntegerField(default=0, help_text=' .budgeted amount by frequency' )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular category instance.
        """
        #return reverse('category-detail', args=[str(self.id)])
        return reverse('category-detail', kwargs={'pk': self.pk})

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}'.format(self.name)
