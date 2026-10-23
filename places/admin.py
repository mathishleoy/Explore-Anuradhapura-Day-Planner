from django.contrib import admin
from django.utils.html import format_html
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    # --- list page -------------------------------------------------------
    list_display = ('id', 'name', 'category_badge', 'star_rating',
                    'latitude', 'longitude', 'typical_visit')
    list_display_links = ('name',)
    list_per_page = 25
    ordering = ('display_order', 'id')

    # --- search + filter -------------------------------------------------
    search_fields = ('name', 'short_description', 'full_description')
    list_filter = ('category', 'category2', 'rating')

    # --- form ------------------------------------------------------------
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Identity', {
            'fields': ('name', 'slug', 'image_url'),
            'description': 'The slug becomes the page address: /place/<slug>/',
        }),
        ('Description', {
            'fields': ('short_description', 'full_description', 'visitor_tip'),
        }),
        ('Categories & rating', {
            'fields': ('category', 'category2', 'rating', 'display_order'),
        }),
        ('Location & visit', {
            'fields': ('latitude', 'longitude', 'opening_hours',
                       'typical_visit', 'entry_fee'),
        }),
    )

    # --- custom list columns --------------------------------------------
    @admin.display(description='Categories')
    def category_badge(self, obj):
        return obj.display_categories()

    @admin.display(description='Rating')
    def star_rating(self, obj):
        return format_html(
            '<span class="ea-rating">&#9733; {}</span>',
            f'{obj.rating:.1f}'
        )
