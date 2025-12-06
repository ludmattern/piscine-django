from django.db import models
from django.conf import settings


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="upvoted_tips", blank=True
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="downvoted_tips", blank=True
    )

    class Meta:
        permissions = [
            ("downvote_tip", "Can downvote tip"),
        ]

    def __str__(self):
        return f"Tip by {self.author} on {self.date}"
