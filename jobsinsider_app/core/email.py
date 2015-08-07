__author__ = 'azhar'
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

class EmailFunc():

    def __init__(self, template, **kwargs):
        '''

        :param template:
        :param kwargs:
        :return:
        '''

