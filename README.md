# Explore Anuradhapura

A day-visit planner for the heritage sites of Anuradhapura. Pick the places you want to see, arrange them in visiting order, and it works out how long the day takes and how much travelling is involved.

Django and SQLite on the back end, plain HTML, CSS and JavaScript on the front, with Tailwind for styling, Leaflet for the maps and Lucide for the icons.

Built for ITE2953 Programming Group Project.

## Running it

Needs Python 3.12 and Django 6.1.2.

```bash
cd "Explore Anuradhapura Web"
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ when it's running.

Django is the only package needed. SQLite is set up by `migrate`, so there's no database server to install.

The admin needs an account before anyone can sign in:

```bash
python manage.py createsuperuser
```

Then go to http://127.0.0.1:8000/admin/.

## Pages

| URL | What it does |
| --- | --- |
| `/` | Places list with live filtering |
| `/place/<slug>/` | Detail page for one place |
| `/map` | Map of every place, with a filterable sidebar |
| `/my-day` | Your planned route, with times and distances |
| `/api/places/` | JSON version of the places list |
| `/admin/` | Admin panel for adding and editing places |

### Places

The home page lists every place with its image, categories, rating and short description. Three dropdowns filter by category, minimum rating and sort order.

Filtering runs through `/api/places/` and redraws the cards in the browser, so changing a dropdown never reloads the page.

One place can carry two categories, shown as `Stupa / Monument`.

### Place detail pages

Every place gets an address built from its name, so Jetavanaramaya sits at `/place/jetavanaramaya/`. The slug is created in `save()` when a place is added, so it never has to be typed in.

The page shows opening hours, entry fee and time on site first, then the full description and a visitor tip when there is one. A map marks the location, and buttons are there for adding the place to the day or opening directions in Google Maps.

### The map

Leaflet on OpenStreetMap tiles. Heritage sites show a terracotta pin and cafes and restaurants a green one. Clicking a pin opens a popup, and the sidebar list uses the same category filter as the pins.

### My day

Add places from the list or the map and they land here as an ordered route.

Four numbers sit at the top: number of stops, time spent at the sites, time spent travelling, and the total for the day.

Travel time works from the distance between consecutive stops, measured with the Haversine formula. That distance is multiplied by 1.3 because roads do not run in straight lines, then divided by 18 km/h, which is roughly what a tuk-tuk averages through the heritage zone. The result works out at about 3 minutes 20 seconds per kilometre.

Both numbers sit at the top of the script in `my_day.html` and can be changed there:

```javascript
const AVG_SPEED = 18;    // km/h
const ROAD_FACTOR = 1.3; // real roads vs straight line
```

Stop order changes the answer, so each stop has arrows to move it up or down. Totals recalculate straight away, which makes it easy to compare two arrangements before picking one. The map draws the route in numbered order to match.

The plan is saved in `localStorage` under the `myDayPlan` key, so no account is needed. It only appears in the browser where the places were added.

## Project layout

```
core/
  settings.py        Django configuration
  urls.py            routes /admin/ and forwards everything else to places/
places/
  models.py          the Place model
  views.py           page views and the JSON endpoint
  urls.py            URL routes for the public site
  admin.py           admin panel configuration
  templates/places/  base.html, home.html, map.html, my_day.html, detail.html
  templates/admin/   admin header override
  static/places/
    images/          logo and hero image
    js/plan.js       localStorage helpers shared by every page
    css/admin.css    admin colour theme
  migrations/        database change history
db.sqlite3           the database
```

`base.html` holds the navigation, footer, Tailwind config and icon setup, and every other template extends it.

## Admin

The admin is Django's own, restyled to fit the site. Django already handles search, validation and forms, so the admin only needed the reskin.

The header shows the project logo on a white bar with a terracotta rule underneath. Colours come from CSS variables in `places/static/places/css/admin.css`. The places list adds a search box, category filters and columns for categories, rating and coordinates. Editing a place groups the fields into identity, description, categories and location.

Typing a name fills in the slug as you go, so the address appears before you save.

Worth knowing: `places` sits first in `INSTALLED_APPS` in `settings.py`. Django looks for templates in app order, so `places/templates/admin/base_site.html` only wins because it comes ahead of `django.contrib.admin`.

## Data

Places are managed through the admin. Each record holds the name, two optional categories, a short and full description, a visitor tip, a rating, coordinates, opening hours, entry fee, expected visit length, an image URL and the slug.

## Design

Terracotta `#af5a2e` for the accent, sand `#f6ecdc` for the background.
