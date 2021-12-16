from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['subject'], body=data['body'], to=[data['to']])
        email.send()

    @staticmethod
    def email_data(request, token, user, reverse_msg):
        current_site = get_current_site(request).domain
        relative_link = reverse_msg
        absolute_url = 'http://' + current_site + relative_link + '?token=' + str(token)
        email_body = 'Hi ' + user.username + ' Use link bellow to verify your email. \n' + absolute_url
        data = {'body': email_body, 'to': user.email, 'subject': 'Verify Your Email', }
        Util.send_email(data)

    @staticmethod
    def email_data_serializer(request, token, user, reverse_msg):
        current = get_current_site(request).domain
        relative = reverse_msg
        absolute_url = 'http://' + current + relative
        email_body = 'Hi \n Use link bellow to reset your password. \n' + absolute_url
        data = {'body': email_body, 'to': user.email, 'subject': 'Reset Your Password', }
        Util.send_email(data)
