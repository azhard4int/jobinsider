__author__ = 'azhar'
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

class EmailFunc():


    subject = {
        'activiation': 'Please verify your email address',
        'forgot_password': 'Recover Your Password',
        'welcome_email': 'Welcome to JobsInsider, Enjoy Your Stay Here',
        'schedule_interview': 'Your have been selected for interview!',
        'job_alert_email': 'Your New Job Alert Has Been Set!',
    }

    def __init__(self, template, **kwargs):
        """
        Constructor to get the details related to the email
        """

        self.template = template
        if 'tosend' in kwargs:
            self.tosend = kwargs['tosend']
        else:
            self.tosend = None
        if 'token' in kwargs:
            self.token = kwargs['token']
        else:
            self.token = None
        if 'username' in kwargs:
            self.username = kwargs['username']
        else:
            self.username= None

        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        else:
            self.first_name = None
        if 'message' in kwargs:
            self.message = kwargs['message']
        else:
            self.message = None

    def generic_email(self):
        """
        Generic function for sending email based on template structure.
        """
        print self.username, self.token
        plaintext = get_template(self.template + ".txt")
        htmlonly = get_template(self.template + ".html")


        c = Context(
            {
                'username': self.username if self.username is not None else None,
                'first_name': self.first_name if self.first_name is not None else None,
                'token': self.token if self.token is not None else None,
                'message': self.message if self.message is not None else None,
            }
        )
        text_content = plaintext.render(c)
        html_content = htmlonly.render(c)
        from_, send_to = 'info@jobsinsider.com', self.tosend

        if str(self.template).__contains__('forgotpassword'):

            subject = self.subject['forgot_password']

        elif str(self.template).__contains__('activateaccount'):

            subject = self.subject['activiation']

        elif str(self.template).__contains__('welcome'):

            subject = self.subject['welcome_email']
        elif str(self.template).__contains__('schedule_interview'):
            if self.first_name:
                subject = self.first_name +", "+ self.subject['schedule_interview']
        elif str(self.template).__contains__('job_alert_email'):
            if self.first_name:
                subject = self.first_name +", "+ self.subject['job_alert_email']

        msg = EmailMultiAlternatives(subject, text_content, from_, [send_to])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            return True
        else:
            return False