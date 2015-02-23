'''SMTP email backend class.'''
import base64
import json
import smtplib
import socket
import threading
import urllib.request, urllib.parse, urllib.error

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.utils import DNS_NAME
from django.core.mail.message import sanitize_address


class GmailBackend(BaseEmailBackend):
    '''
    A wrapper that manages the SMTP network connection.
    '''
    def __init__(self, host=None, port=None, username=None, password=None, use_tls=None, fail_silently=False, **kwargs):
        super(GmailBackend, self).__init__(fail_silently=fail_silently)
        self.__param = {
            'client_id': settings.GOOGLE_API_CLIENT_ID,
            'client_secret': settings.GOOGLE_API_CLIENT_SECRET,
            'refresh_token': settings.EMAIL_HOST_PASSWORD,
            'grant_type': 'refresh_token',
        }
        self.__request_url = 'https://accounts.google.com/o/oauth2/token'
        self.__host = host or settings.EMAIL_HOST
        self.__port = port or settings.EMAIL_PORT
        self.__usrname = username or settings.EMAIL_HOST_USER
        self.__use_tls = use_tls or settings.EMAIL_USE_TLS
        self.__connection = None
        self.__lock = threading.RLock()

    def open(self):
        '''
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        '''
        if self.__connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            # Refresh access token by the refresh token
            gauth = urllib.request.urlopen(self.__request_url, urllib.parse.urlencode(self.__param))
            response = gauth.read()
            gauth.close()
            response = json.loads(response)
            access_token = response['access_token']
            access_token = 'user={0}\1auth=Bearer {1}\1\1'.format(self.__usrname, access_token.encode('utf-8'))

            # If local_hostname is not specified, socket.getfqdn() gets used.
            # For performance, we use the cached FQDN for local_hostname.
            self.__connection = smtplib.SMTP(self.__host, self.__port, local_hostname=DNS_NAME.get_fqdn())
            if self.__use_tls:
                self.__connection.ehlo()
                self.__connection.starttls()
                self.__connection.ehlo()
            self.__connection.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(access_token))
            return True
        except:
            if not self.fail_silently:
                raise
            return False

    def close(self):
        '''Closes the connection to the email server.'''
        try:
            try:
                self.__connection.quit()
            except socket.sslerror:
                # This happens when calling quit() on a TLS connection
                # sometimes.
                self.__connection.close()
            except:
                if self.fail_silently:
                    return
                raise
        finally:
            self.__connection = None

    def send_messages(self, email_messages):
        '''
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        '''
        if not email_messages:
            return
        self.__lock.acquire()
        try:
            new_conn_created = self.open()
            if not self.__connection:
                # We failed silently on open().
                # Trying to send would be pointless.
                return
            num_sent = 0
            for message in email_messages:
                sent = self.__send(message)
                if sent:
                    num_sent += 1
            if new_conn_created:
                self.close()
        finally:
            self.__lock.release()
        return num_sent

    def __send(self, email_message):
        '''A helper method that does the actual sending.'''
        if not email_message.recipients():
            return False
        from_email = sanitize_address(email_message.from_email, email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding) for addr in email_message.recipients()]
        try:
            self.__connection.sendmail(from_email, recipients, email_message.message().as_string())
        except:
            if not self.fail_silently:
                raise
            return False
        return True
