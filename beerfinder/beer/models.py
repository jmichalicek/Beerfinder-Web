from django.db import models
from django.conf import settings
from django.utils.text import slugify

import re
from unidecode import unidecode

class Beer(models.Model):
    """
    Describes a beer

    :ivar name: the name of the beer
    :ivar normalized_name: the normalized name of the beer for searching, etc.
    :ivar brewery: the :class:`Brewery` of the beer
    :ivar created_by: the :class:`accounts.models.User` who created the Beer
    :ivar slug: a URL usable slug
    """
    name = models.CharField(max_length=75)
    brewery = models.ForeignKey('Brewery')
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    slug = models.SlugField(max_length=150)
    normalized_name = models.CharField(max_length=75, blank=True, db_index=True, help_text='normalized, simplified name for easy searching')

    class Meta:
        unique_together = (('name', 'brewery'),)
        ordering = ('name', )

    def __unicode__(self):
        return u'{0}'.format(self.name)

    @staticmethod
    def normalize_for_name(name):
        """
        Normalize a string to be used as the normalized_name
        or to be compared to stored normalized_name of existing
        models

        :param name: The name string to normalize
        :type name: str or unicode str

        :rtype: unicode str
        """
        normalized = name.strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = unidecode(u'{0}'.format(normalized))
        # the below re takes anything that is not a capital ascii letter, lowercase ascii letter
        # or ascii digit and removes it.  \w is not used because underscore should be removed
        normalized = re.sub(r'[^A-Za-z0-9\s]+', '', normalized)
        return u'{0}'.format(normalized)

    def generate_slug(self):
        """
        Generate a slug from the brewery name and beer name

        :returns: the generated slug
        :rtype: str
        """
        # beer name is unique and brewery name is unique, so by default these
        # will be unique although it is not enforced at the database level
        return slugify(u'{0} {1}'.format(self.brewery.get_normalized_name(), self.get_normalized_name()))

    def get_normalized_name(self):
        """
        Returns a normalized name with whitespace trimmed from the ends,
        whitespace in the middle condensed to single spaces, and non-ascii
        characters replaced with an ascii transliteration

        :returns: a normalized name
        :rtype: str
        """
        return Beer.normalize_for_name(self.name)

    def save(self, *args, **kwargs):
        """
        Automatically updates self.normalized_name
        and generates a slug if one does not already exist
        """
        self.normalized_name = self.get_normalized_name()

        if not self.slug:
            self.slug = self.generate_slug()

        super(Beer, self).save(*args, **kwargs)


class Brewery(models.Model):
    """
    A beer brewery

    :ivar name: the name of the beer
    :ivar normalized_name: the normalized name of the beer for searching, etc.
    :ivar slug: a URL usable slug
    """
    name = models.CharField(max_length=75, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=75)
    normalized_name = models.CharField(max_length=75, blank=True, db_index=True, help_text='normalized, simplified name for easy searching')

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return u'{0}'.format(self.name)

    @staticmethod
    def normalize_for_name(name):
        """
        Normalize a string to be used as the normalized_name
        or to be compared to stored normalized_name of existing
        models

        :param name: The name string to normalize
        :type name: str or unicode str

        :rtype: unicode str
        """
        normalized = name.strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = unidecode(u'{0}'.format(normalized))
        # the below re takes anything that is not a capital ascii letter, lowercase ascii letter
        # or ascii digit and removes it.  \w is not used because underscore should be removed
        normalized = re.sub(r'[^A-Za-z0-9\s]+', '', normalized)
        return u'{0}'.format(normalized)

    def generate_slug(self):
        """
        Generate a slug from the brewery name and beer name

        :returns: the generated slug
        :rtype: str
        """
        # almost guaranteed unique because name is unique
        # but the normalization could change that.
        # allow it to be saved even if not unique and catch the errors later for now
        return slugify(u'{0}'.format(self.get_normalized_name()))

    def get_normalized_name(self):
        """
        Returns a normalized name with whitespace trimmed from the ends,
        whitespace in the middle condensed to single spaces, and non-ascii
        characters replaced with an ascii transliteration

        :returns: a normalized name
        :rtype: str
        """
        return Brewery.normalize_for_name(self.name)

    def save(self, *args, **kwargs):
        self.normalized_name = self.get_normalized_name()

        if not self.slug:
            self.slug = self.generate_slug()

        super(Brewery, self).save(*args, **kwargs)


