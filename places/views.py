from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Place


def filtered_places(request):
    places = Place.objects.all()

    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    rating = request.GET.get('rating', '')
    order = request.GET.get('order', '')

    if q:
        places = places.filter(name__icontains=q)
    if category:
        places = places.filter(Q(category=category) | Q(category2=category))
    if rating:
        places = places.filter(rating__gte=float(rating))

    if order == 'highest':
        return places.order_by('-rating')
    if order == 'name':
        return places.order_by('name')
    if order == 'visit':
        return places.order_by(F('typical_visit').asc(nulls_last=True))
    if order == '-visit':
        return places.order_by(F('typical_visit').desc(nulls_last=True))
    return places.order_by('display_order')


def home(request):
    return render(request, 'places/home.html', {'places': filtered_places(request)})


def api_places(request):
    data = [{
        'id': place.id,
        'slug': place.slug,
        'name': place.name,
        'categories': place.display_categories(),
        'rating': place.rating,
        'short_description': place.short_description,
        'opening_hours': place.opening_hours,
        'typical_visit': place.typical_visit,
        'entry_fee': place.entry_fee,
        'image_url': place.image_url,
    } for place in filtered_places(request)]

    return JsonResponse(data, safe=False)


def map_page(request):
    places = Place.objects.all().order_by('display_order')
    return render(request, 'places/map.html', {'places': places})


def my_day(request):
    places = Place.objects.all().order_by('display_order')
    return render(request, 'places/my_day.html', {'places': places})


def place_detail(request, slug):
    place = get_object_or_404(Place, slug=slug)
    return render(request, 'places/detail.html', {'place': place})
