from django.db import models

class CalendarEntry(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.category} - {self.start_date} to {self.end_date})"

    class Meta:
        verbose_name_plural = "Calendar entries"
