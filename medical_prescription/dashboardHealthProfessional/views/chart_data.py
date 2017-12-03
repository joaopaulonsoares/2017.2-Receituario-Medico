# standard library
import json
from datetime import datetime, timedelta

# django
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# local django
from user.decorators import is_health_professional
from prescription.models import Prescription


class ChartData(View):
    """
    Responsible for obtaining suggested prescriptions to the CID.
    """

    @method_decorator(login_required)
    @method_decorator(is_health_professional)
    def dispatch(self, *args, **kwargs):
        return super(ChartData, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            list_date = []
            for count in range(7, -1, -1):
                chart_item = {}
                date_ago = datetime.today() - timedelta(days=count)
                actual_date = datetime(date_ago.year, date_ago.month, date_ago.day)
                prescription_count = Prescription.objects.filter(date__year=actual_date.year,
                                                                 date__month=actual_date.month,
                                                                 date__day=actual_date.day).count()
                if count:
                    chart_item['name'] = actual_date.strftime('%A')
                else:
                    chart_item['name'] = 'Today'

                chart_item['quantity'] = prescription_count
                list_date.append(chart_item)

            result = json.dumps(list_date)
            mimetype = 'application/json'
            return HttpResponse(result, mimetype)
