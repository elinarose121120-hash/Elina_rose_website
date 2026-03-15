# Python 3.14 Compatibility Fix

## Issue
Django 4.2.29 has a compatibility issue with Python 3.14 that causes an `AttributeError` when accessing Django's default admin panel:

```
AttributeError: 'super' object has no attribute 'dicts' and no __dict__ for setting new attributes
```

This error occurs in Django's template context system when trying to copy context objects.

## Solution
A compatibility patch has been implemented in `website/compatibility.py` that fixes this issue by patching Django's `Context.__copy__` method to work correctly with Python 3.14.

## Implementation
The fix is automatically loaded when the Django app starts via the `WebsiteConfig.ready()` method in `website/apps.py`.

## Files Involved
- `website/compatibility.py` - Contains the compatibility patch
- `website/apps.py` - Loads the compatibility fix on app startup

## Note
Since we're using custom dashboards (not Django's default admin), this fix ensures that:
1. Django admin panel works if needed for debugging
2. No errors occur in the template system
3. The application runs smoothly on Python 3.14

## Testing
After applying this fix, Django admin panel should work without errors. However, remember to use the custom dashboards for regular operations:
- Admin Dashboard: `/admin/dashboard/`
- Manager Dashboard: `/manager/dashboard/`

