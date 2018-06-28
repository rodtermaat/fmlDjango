from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange
from datetime import datetime,date

class CheckbookCalendar(HTMLCalendar):

    def __init__(self, pCheckEntries):
        super(CheckbookCalendar, self).__init__()
        self.checks = self.group_by_day(pCheckEntries)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.checks:
                cssclass += ' filled'
                body = []
                for check in self.checks[day]:
                    body.append('<a href="%s">' % check.get_absolute_url())
                    body.append(esc(check.name))
                    body.append(': ')
                    #body.append(esc(check.category))
                    body.append(esc(check.amount))
                    #body.append(esc(check.cleared))
                    body.append('</a><br/>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(CheckbookCalendar, self).formatmonth(year, month)

    def group_by_day(self, pCheckEntries):
        field = lambda check: check.dater.day
        return dict(
            [(day, list(items)) for day, items in groupby(pCheckEntries, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
