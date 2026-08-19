
from rest_framework import generics, status
from django.db import transaction

from .tasks import send_urgent_ticket_notification
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from .paginations import CustomPagination
from .serializers import RegisterSerializer, ProfileSerializer,CategorySerializer

from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_ticket_statistics

from .models import Category

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import TicketFilter
from .models import Ticket
from .permissions import (
    IsAdminOrAssignedOperator,
    IsTicketOwner,
)
from .serializers import TicketSerializer
from .permissions import IsAdminOrReadOnly
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi."},
            status=status.HTTP_201_CREATED
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):

        return self.request.user





class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer


    permission_classes = [IsAdminOrReadOnly]





class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = TicketFilter

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "priority",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        user = self.request.user

        if self.action == "list":
            if user.role == "admin":
                return Ticket.objects.all()

            if user.role == "operator":
                return Ticket.objects.filter(
                    operator=user
                )

            if user.role == "client":
                return Ticket.objects.filter(
                    client=user
                )

            return Ticket.objects.none()

        return Ticket.objects.all()

    def get_permissions(self):
        if self.action in ["create", "list"]:
            permission_classes = [
                IsAuthenticated,
            ]

        elif self.action in [
            "retrieve",
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [
                IsAuthenticated,
                IsTicketOwner | IsAdminOrAssignedOperator,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        ticket = serializer.save(
            client=self.request.user,
            status=Ticket.StatusChoices.NEW,
        )

        if ticket.priority == Ticket.PriorityChoices.URGENT:
            transaction.on_commit(
                lambda: send_urgent_ticket_notification.delay(
                    ticket.id
                )
            )





class TicketStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    CACHE_KEY = "ticket_statistics"
    CACHE_TIMEOUT = 300

    def get(self, request):
        statistics = cache.get(self.CACHE_KEY)

        if statistics is not None:
            return Response(statistics)

        statistics = get_ticket_statistics()

        cache.set(
            self.CACHE_KEY,
            statistics,
            self.CACHE_TIMEOUT,
        )

        return Response(statistics)