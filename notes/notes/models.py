from django.db import models
import datetime

# Create your models here.


class GroupNote(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(delete_time__isnull=True)


class Note(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(blank=True, null=True)
    group_node_fk = models.ForeignKey(
        GroupNote, on_delete=models.CASCADE, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(blank=True, null=True, editable=False)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.delete_time = datetime.timezone.now()
        self.save()

    def restore(self):
        self.delete_time = None
        self.save()

    class Meta:
        ordering = ['create_time']
