from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Beer(models.Model):
    name = models.CharField(max_length=75, unique=True)
    brewery = models.ForeignKey('Brewery')
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    slug = models.SlugField(max_length=150)

    class Meta:
        unique_together = (('name', 'brewery'),)
        ordering = ('name', )

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def generate_slug(self):
        # beer name is unique and brewery name is unique, so by default these
        # will be unique although it is not enforced at the database level
        return slugify(u'{0} {1}'.format(self.brewery.name, self.name))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()

        super(Beer, self).save(*args, **kwargs)

class Brewery(models.Model):
    name = models.CharField(max_length=75, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=75)

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def generate_slug(self):
        # automatically unique because name is unique
        return slugify(u'{0}'.format(self.name))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()

        super(Brewery, self).save(*args, **kwargs)


