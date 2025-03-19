from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.conf import settings

# Configure API key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.ANYMAIL["BREVO_API_KEY"]

def send_email(to_email, typeofemail, **kwargs):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {"name": "OrderFood", "email": settings.DEFAULT_FROM_EMAIL}
    to = [{"email": to_email, "name": "Recipient Name"}]

    html_content = ""
    subject = ""

    if typeofemail == "password_reset":
        subject = "Password Reset Confirmation"
        html_content = f"""
            <h1>Password Reset</h1>
            <p>Click <a href='http://{settings.BREVO_API_URL}/password-reset/{kwargs['uid']}/{kwargs['token']}'>here</a> to reset your password.</p>
        """
    
    elif typeofemail == "request_activate_seller_account":
        subject = "Activate Seller Account"
        html_content = f"""
            <h1>Activate Seller Account</h1>
            <p>Click <a href='http://{settings.BREVO_API_URL}/activate-seller-account/{kwargs['uid']}/{kwargs['token']}'>here</a> to activate your seller account.</p>
        """

    elif typeofemail == "seller_approval":
        subject = "Your Seller Account Has Been Approved!"
        html_content = f"""
            <h1>Congratulations, {kwargs['username']}!</h1>
            <p>Your request to become a seller has been approved.</p>
            <p>You can now start selling on <strong>OrderFood</strong>.</p>
            <p>Login and update your store: <a href="http://{settings.BREVO_API_URL}/seller-dashboard">Seller Dashboard</a></p>
        """

    elif typeofemail == "seller_denial":
        subject = "Your Seller Account Request Was Denied"
        html_content = f"""
            <h1>Dear {kwargs['username']},</h1>
            <p>We regret to inform you that your request to become a seller has been denied.</p>
            <p>If you have any questions, feel free to contact us.</p>
        """

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
