# Urs Cart — Django E-commerce Store

A polished Django e-commerce demo with registration/login, product categories, local product artwork, cart, checkout and order history.

## Run

```bash
python3 -m venv myworld
source myworld/bin/activate
pip install -r requirements.txt --default-timeout=120
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py seed_products
python3 manage.py runserver
```

Open http://127.0.0.1:8000/

## Authentication

- New users register from `/register/`.
- Existing users use the **Login here** link shown on the registration page.
- The Login page is intentionally not placed in the main navigation.
- Registration automatically signs the new user in.
- Django admin remains available at `/admin/`.

## Included categories

Tech & Gadgets, Fashion, Home & Living, Beauty & Care, Stationery, Sports & Fitness, Travel, and Study Essentials.

All seeded product artwork is stored locally under `store/static/store/images/`, so product images do not depend on external image URLs.
