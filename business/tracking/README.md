# Activity Tracking Module

A comprehensive Django application for tracking and analyzing user activities across your platform.

## Features

- **Detailed Activity Logging**: Captures user actions with full context (user, device, location, etc.)
- **Real-time Monitoring**: Track activities as they happen
- **Advanced Filtering**: Powerful query capabilities for historical data
- **Security Features**: Flag suspicious activities for review
- **Analytics Dashboard**: Built-in statistics and metrics
- **Data Export**: Export activity logs in CSV or JSON format

## Installation

1. Add to your Django project's `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       ...
       'tracking',
       ...
   ]
   ```

2. Include the URLs in your project's `urls.py`:

   ```python
   urlpatterns = [
       ...
       path('api/tracking/', include('tracking.urls')),
       ...
   ]
   ```

3. Run migrations:
   ```bash
   python manage.py migrate tracking
   ```

## Configuration

Add these settings to your Django settings file:

```python
# Geolocation settings (optional)
DISABLE_GEOLOCATION = False  # Set to True to disable IP geolocation

# Sensitive fields to redact from logs
SENSITIVE_FIELDS = ['password', 'token', 'secret']

# Throttling rates (requests per minute)
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/hour'
    }
}
```

## Usage

### Tracking Activities

Decorate views to track activities:

```python
from tracking.services.decorators import track

@track(activity_type='AUTH')
def login_view(request):
    # Your view logic
    pass

@track(activity_type='PAYMENT', async_log=True)
def payment_view(request):
    # Process payment asynchronously
    pass
```

### API Endpoints

| Endpoint                                | Method | Description                      |
| --------------------------------------- | ------ | -------------------------------- |
| `/api/tracking/activities/`             | GET    | List all activities (filterable) |
| `/api/tracking/activities/<id>/`        | GET    | Get activity details             |
| `/api/tracking/activities/<id>/delete/` | DELETE | Delete an activity               |
| `/api/tracking/activities/<id>/flag/`   | PATCH  | Toggle flagged status            |
| `/api/tracking/stats/`                  | GET    | Get activity statistics          |
| `/api/tracking/activities/export/`      | GET    | Export activities (CSV/JSON)     |

### Admin Interface

Access the admin panel at `/admin/tracking/activity/` to:

- View activity logs
- Filter by type, country, or flagged status
- Search by user, IP, or endpoint

## Models

### Activity Model

```python
class Activity(models.Model):
    """Tracks comprehensive user activity data."""

    # Core fields: id, timestamp, type, flagged, tags
    # User context: user, session_id
    # Network context: ip_address, isp, asn
    # Geo context: country, region, city, coordinates
    # Device context: device, os, browser, is_mobile
    # Request context: endpoint, method, status, headers, params, duration
```

## Serializers

- `ActivitySerializer`: Full activity details
- `ActivityListSerializer`: Compact representation for lists

## Services

- `ActivityTracker`: Core tracking logic
- `@track` decorator: Easy view integration

## Example API Responses

### List Activities

```json
{
  "count": 125,
  "next": "http://api.example.com/activities/?page=2",
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "timestamp": "2023-01-01T12:00:00Z",
      "type": "AUTH",
      "type_display": "Authentication",
      "user": 1,
      "ip_address": "192.168.1.1",
      "endpoint": "/api/auth/login/",
      "status": 200,
      "duration": 150.2
    }
  ]
}
```

### Activity Statistics

```json
{
  "counts": {
    "total": 125,
    "flagged": 3,
    "last_30_days": 42
  },
  "response_times": {
    "avg": 210.5,
    "max": 1250.0,
    "min": 50.2
  },
  "types": [
    {
      "type": "AUTH",
      "type_display": "Authentication",
      "count": 42
    }
  ]
}
```

## Requirements

- Django 3.2+
- Django REST Framework
- django-ipware (for IP detection)
- user-agents (for device parsing)
- requests (for geolocation)
- drf-spectacular (for API docs - optional)

## Testing

Run tests with:

```bash
python manage.py test tracking
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

## License

[MIT](https://choosealicense.com/licenses/mit/)
