"""
this file is used as a middleware to collect responses
"""
# from datetime import datetime
# from django.utils.deprecation import MiddlewareMixin
#
# import app.times
# from app.models import Request
#
#
# class AppMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         request.start_time = datetime.now()
#
#     def process_response(self, request, response):
#         execute_time = (datetime.now() - request.start_time).microseconds // 1000
#         now_time = app.times.datetime2string(request.start_time)
#         path = request.path
#         data = Request.objects.create(
#             create_time=now_time,
#             timecost=execute_time,
#             request_type=path)
#         data.save()
#         return response
