from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.conf import settings

# Configure API key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.ANYMAIL["BREVO_API_KEY"]

def send_email(subject, to_email, html_content):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {"name": "OrderFood", "email": settings.DEFAULT_FROM_EMAIL}
    to = [{"email": to_email, "name": "Recipient Name"}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content,
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
        return True
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return False
