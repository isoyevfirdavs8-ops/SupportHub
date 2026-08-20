# SupportHub

SupportHub — mijozlar murojaatlarini (Ticket) boshqarish uchun yaratilgan REST API tizimi.

Loyiha orqali mijozlar murojaat yaratishi, operatorlar o‘zlariga biriktirilgan murojaatlarni boshqarishi, administrator esa barcha murojaatlarni nazorat qilishi mumkin.

Loyihada REST API, JWT authentication, role-based permissions, filtering, searching, pagination, Redis cache, WebSocket va Celery texnologiyalaridan foydalanilgan.

---

## Texnologiyalar

- Python 3.12+
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Django Channels
- WebSocket
- JWT Authentication
- django-filter
- drf-spectacular
- pytest
- pytest-django

---

# Asosiy imkoniyatlar

## Authentication

- Foydalanuvchini ro‘yxatdan o‘tkazish
- JWT orqali login
- Access token
- Refresh token
- JWT orqali himoyalangan endpointlar

## Ticket

- Ticket yaratish
- Ticketni ko‘rish
- Ticketni yangilash
- Ticketni o‘chirish
- Ticket statusini boshqarish
- Ticket priority boshqaruvi
- Ticket kategoriyasi
- Operatorga biriktirish

Ticket yaratilganda:

- `client` avtomatik ravishda JWT token orqali aniqlanadi
- `status` avtomatik `new` bo‘ladi
- client boshqa foydalanuvchi nomidan ticket yarata olmaydi

---

# Rollar

Loyihada uchta asosiy rol mavjud:

### Client

Client:

- o‘z ticketlarini ko‘radi
- yangi ticket yaratadi
- o‘z ticketini tahrirlashi mumkin
- boshqa clientlarning ticketlarini ko‘ra olmaydi
- `status` va `operator` maydonlarini o‘zgartira olmaydi
- kategoriya yarata olmaydi

### Operator

Operator:

- o‘ziga biriktirilgan ticketlarni ko‘radi
- biriktirilgan ticketlarni boshqaradi
- ticketlar bo‘yicha real-time yozishmada qatnashadi

### Admin

Admin:

- barcha ticketlarni ko‘ra oladi
- barcha ticketlarni boshqaradi
- kategoriya yaratadi
- ticketlarni operatorlarga biriktiradi
- tizimdagi barcha ma'lumotlarni nazorat qiladi

---

# Project strukturasi

```text
SupportHub/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── celery.py
│
├── control/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── filters.py
│   ├── pagination.py
│   ├── middleware.py
│   ├── consumers.py
│   ├── routing.py
│   ├── tasks.py
│   └── signals.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tickets.py
│   ├── test_categories.py
│   ├── test_filters.py
│   ├── test_pagination.py
│   ├── test_statistics.py
│   ├── test_middleware.py
│   └── test_websocket.py
│
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── pytest.ini
└── README.md