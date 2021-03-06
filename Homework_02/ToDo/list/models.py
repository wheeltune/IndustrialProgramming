from django.db import models

class ToDo(models.Model):
	content = models.CharField(max_length=256)
	deadline = models.DateTimeField()
	is_done = models.BooleanField(default=False)

	def __str__(self):
		return self.content
