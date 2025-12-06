import random
import time
from django.conf import settings


class RandomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = time.time()

        # Check if username exists and is valid (less than 42 seconds old)
        if (
            "username" not in request.session
            or "username_timestamp" not in request.session
            or current_time - request.session["username_timestamp"] > 42
        ):

            names = getattr(settings, "RANDOM_NAMES", ["Anonymous"])
            request.session["username"] = random.choice(names)
            request.session["username_timestamp"] = current_time

        response = self.get_response(request)
        return response
