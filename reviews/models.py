from django.db import models

class GeneralReview(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Automatically sets the time

    def __str__(self):
        return f'Review by {self.name}'