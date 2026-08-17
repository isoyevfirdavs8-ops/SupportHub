from django.db.models import Count, Q

from .models import Ticket


def get_ticket_statistics():
    result = Ticket.objects.aggregate(
        total=Count("id"),

        new=Count(
            "id",
            filter=Q(status=Ticket.StatusChoices.NEW),
        ),

        in_progress=Count(
            "id",
            filter=Q(
                status=Ticket.StatusChoices.IN_PROGRESS
            ),
        ),

        resolved=Count(
            "id",
            filter=Q(
                status=Ticket.StatusChoices.RESOLVED
            ),
        ),

        closed=Count(
            "id",
            filter=Q(
                status=Ticket.StatusChoices.CLOSED
            ),
        ),

        urgent=Count(
            "id",
            filter=Q(
                priority=Ticket.PriorityChoices.URGENT
            ),
        ),
    )

    return result