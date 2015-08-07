__author__ = 'azhar'
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

class EmailFunc():


    subject = {
        'activiation': 'Activate Your Account',
        'forgot_password': 'Recover Your Password',
        'welcome_email': 'Welcome to JobsInsider, Enjoy Your Stay Here',
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
        if 'username' in kwargs:
            self.username = kwargs['username']
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']

    def generic_email(self):
        """
        Generic function for sending email based on template structure.
        """

        plaintext = get_template(self.template + ".txt")
        htmlonly = get_template(self.template + ".html")

        if self.username is not None:
            c = Context({'username': self.username})
        elif self.first_name is not None:
            c = Context({'first_name': self.first_name})

        text_content = plaintext.render(c)
        html_content = htmlonly.render(c)
        from_, send_to = 'info@jobsinsider.com', self.tosend

        if str(self.template).__contains__('forgotpassword'):

            subject = self.subject['forgot_password']

        elif str(self.template).__contains__('activateaccount'):

            subject = self.subject['forgot_password']

        elif str(self.template).__contains__('welcome'):

            subject = self.subject['welcome_email']


        msg = EmailMultiAlternatives(subject, text_content, from_, [send_to])
        msg.attach_alternative(html_content, "text/html")


        if msg.send():
            return True
        else:
            return False