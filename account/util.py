from django.core.mail import send_mail

def sent(email, body):
     send_mail(
         'Reset Your Password',
          body,
         'foodorder650@gmail.com',
         [email],
         fail_silently=False,    
        )
     
     return None 