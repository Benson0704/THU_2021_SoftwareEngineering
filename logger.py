"""
this file is used as a middleware to collect responses
"""
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('router')


class resapp_middleware(MiddlewareMixin):

    def process_request(self, request):
        logger.info("resapp_middleware.process_request")
        logger.info(request.path)
        logger.info(request.method)
        logger.info(request.get_host())
        logger.info(request.GET)
        if request.method in ("POST", "PUT", "GET"):
            logger.info(request.body)

    def process_response(self, request, response):
        logger.info("resapp_middleware.process_response")
        logger.info('response:')
        logger.info(response)
        return response