import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Ticket, User


logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_urgent_ticket_notification(
    self,
    ticket_id,
):
    logger.info(
        "Urgent ticket notification task started. "
        "ticket_id=%s",
        ticket_id,
    )

    try:
        ticket = Ticket.objects.select_related(
            "client",
            "category",
        ).get(pk=ticket_id)
    except Ticket.DoesNotExist:
        logger.warning(
            "Ticket not found. ticket_id=%s",
            ticket_id,
        )
        return

    recipients = list(
        User.objects.filter(
            role__in=["operator", "admin"],
        )
        .exclude(email="")
        .values_list("email", flat=True)
    )

    if not recipients:
        logger.warning(
            "No operator/admin email found. "
            "ticket_id=%s",
            ticket_id,
        )
        return

    send_mail(
        subject=f"URGENT ticket: {ticket.title}",
        message=(
            f"Yangi urgent ticket yaratildi.\n\n"
            f"Ticket ID: {ticket.id}\n"
            f"Title: {ticket.title}\n"
            f"Description: {ticket.description}\n"
            f"Client: {ticket.client.username}\n"
        ),
        from_email=None,
        recipient_list=recipients,
        fail_silently=False,
    )

    logger.info(
        "Urgent ticket notification sent. "
        "ticket_id=%s recipients=%s",
        ticket_id,
        recipients,
    )

@shared_task
def find_old_new_tickets():
    logger.info(
        "Old new tickets task started."
    )

    limit = timezone.now() - timedelta(hours=24)

    tickets = Ticket.objects.filter(
        status=Ticket.StatusChoices.NEW,
        created_at__lt=limit,
    ).select_related(
        "client",
        "operator",
    )

    count = tickets.count()

    logger.info(
        "Found %s old new tickets.",
        count,
    )

    for ticket in tickets:
        logger.warning(
            "Ticket has been NEW for more than 24 hours: "
            "ticket_id=%s client=%s operator=%s "
            "created_at=%s",
            ticket.id,
            ticket.client.username,
            (
                ticket.operator.username
                if ticket.operator
                else None
            ),
            ticket.created_at,
        )

    logger.info(
        "Old new tickets task finished."
    )

    return count