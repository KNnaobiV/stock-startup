from django.core.mail import send_mail

def send_email_on_account_number_generation(user, account_number):
    subject = 'Your New Account Number'
    message = f'Hello {user.username},\n\nYour account number is: {account_number}'
    from_email = 'your@email.com'  # Replace with your email
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)