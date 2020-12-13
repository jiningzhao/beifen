from .tests import RunAllCase
from django.http import HttpResponse


def haha(request):
    RunAllCase().doc_list()
    return HttpResponse("成功！")


def nanshou(request):
    return HttpResponse("ehhex")
