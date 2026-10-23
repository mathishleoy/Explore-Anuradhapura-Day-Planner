from django.db import models
from django.utils.text import slugify


class Place(models.Model):
    CATEGORY_CHOICES = [
        ('stupa', 'Stupa'),
        ('monument', 'Monument'),
        ('temple', 'Temple'),
        ('heritage_site', 'Heritage Site'),
        ('sculpture', 'Sculpture'),
        ('museum', 'Museum'),
        ('ruins', 'Ruins'),
        ('sacred_site', 'Sacred Site'),
        ('lake', 'Lake'),
        ('cafe', 'Cafe'),
        ('restaurant', 'Restaurant'),
    ]

    name = models.CharField(max_length=100)
    short_description = models.TextField(max_length=200)
    full_description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    category2 = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    rating = models.FloatField(default=4.8)
    latitude = models.FloatField()
    longitude = models.FloatField()
    opening_hours = models.CharField(max_length=100, blank=True, null=True)
    typical_visit = models.IntegerField(blank=True, null=True)
    entry_fee = models.CharField(max_length=50, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    image_url = models.URLField(blank=True)
    visitor_tip = models.TextField(max_length=300, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def display_categories(self):
        if self.category2:
            return f"{self.get_category_display()} / {self.get_category2_display()}"
        return self.get_category_display()

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 2
            while Place.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
