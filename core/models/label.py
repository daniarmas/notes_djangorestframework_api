from django.db import models


class Label(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'label'

    def __str__(self):
        return self.title
