# Core module


Shared primitives and helpers used across the project.


## How to install


1. Copy the `core` folder into your Django project.
2. Add `core` to `INSTALLED_APPS` in `settings.py` if you want to include migrations or tests.
3. Add middleware in `settings.py`:


```py
MIDDLEWARE = [
'core.middleware.RequestIDMiddleware',
'core.middleware.ExceptionToJSONMiddleware',
# ... existing middlewares
]
```


## Tests


Run `pytest` or `python manage.py test core`.


## Conventions
- Always use `now_utc()` for timestamps outside models.
- Raise `APIError` in services when something goes wrong.
- Use `ok()` / `error()` for consistent API responses in views.