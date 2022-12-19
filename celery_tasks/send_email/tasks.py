from django.core.mail import send_mail
from django.conf import settings
from celery_tasks import celery_app


@celery_app.task
def send_code(code, to_email):
    send_mail(
        subject="酷猫社区验证码",
        message=f"您的验证码是：{code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email]
    )
