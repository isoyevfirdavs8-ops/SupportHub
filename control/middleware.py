from datetime import datetime

from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)

        now = datetime.now().timestamp()

        if ip not in self.requests:
            self.requests[ip] = []

        # Faqat 10 soniyadan yangi so‘rovlarni saqlaymiz
        self.requests[ip] = [timestamp for timestamp in self.requests[ip] if now - timestamp < 10]

        if len(self.requests[ip]) >= 5:
            return HttpResponseForbidden("Siz juda ko'p so'rov yubordingiz. Iltimos, biroz kuting.")

        self.requests[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
