from django.conf import settings
from django.core.mail import send_mail


def send_conf_code(email, conf_code):
    "Функция-шорткат для отправки письма."
    send_mail(
        subject='[YaMDB] Код подтверждения',
        message=('Добрый день!\n'
                 f'Ваш код подтверждения - {conf_code}'),
        from_email=settings.EMAIL_SENDER_ADRESS,
        recipient_list=[email],
        fail_silently=True,
    )
