"""
this is a module for getting the information of videos and labels
"""
from django.http import JsonResponse


def gen_response(code: int, data: str):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def video(request):
    """
    this function should respond to the get video request
    """


def label(request):
    """
    this function should respond to the requests relating to labels
    """
