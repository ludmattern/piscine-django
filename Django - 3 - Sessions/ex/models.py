from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    @property
    def reputation(self):
        rep = 0
        for tip in self.tip_set.all():
            rep += tip.upvotes.count() * 5
            rep -= tip.downvotes.count() * 2
        return rep

    def has_perm(self, perm, obj=None):
        if perm == "ex.downvote_tip":
            return self.reputation >= 15
        if perm == "ex.delete_tip":
            return self.reputation >= 30
        return super().has_perm(perm, obj)


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
