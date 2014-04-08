from django.db import models


class Author(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(default="")

    def __unicode__(self):
        return self.name


class Message(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, default=Author(name="Anonymous", description="Nada"))

    def __unicode__(self):
        return self.title
