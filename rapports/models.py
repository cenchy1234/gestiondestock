from django.db import models
from django.utils import timezone

class Report(models.Model):
    REPORT_TYPES = [
        ('STOCK_MOVEMENT', 'Mouvements de stock'),
        ('STOCK_STATE', 'État des stocks'),
        ('STATS', 'Statistiques')
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    date_generated = models.DateTimeField(default=timezone.now)
    data = models.JSONField()

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.date_generated.strftime('%d/%m/%Y')}"
