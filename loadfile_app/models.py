from django.db import models


# Create your models here.
class LoadFile(models.Model):
    """Set field loadfile"""
    file_name = models.CharField(max_length=200, blank=True)
    file_obj = models.FileField(upload_to='media')
    str_for_search = models.CharField(max_length=200)
    file_size = models.IntegerField()
    count_found = models.SmallIntegerField()
    position_found = models.TextField()
    time_search = models.CharField(max_length=20, blank=True)


    def __str__(self):
        """Return string value model"""
        return str(self.file_obj)
