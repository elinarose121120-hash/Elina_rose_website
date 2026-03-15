"""
Compatibility fixes for Python 3.14 and Django 4.2.29
This fixes the AttributeError in Django's template context system
"""
import django.template.context

# Fix for Python 3.14 compatibility issue with Django template context
# This patches the __copy__ method to work with Python 3.14's super() changes
if hasattr(django.template.context.Context, '__copy__'):
    _original_copy = django.template.context.Context.__copy__
    
    def _patched_copy(self):
        """Patched __copy__ method for Python 3.14 compatibility"""
        try:
            duplicate = _original_copy(self)
        except AttributeError as e:
            if "'super' object has no attribute 'dicts'" in str(e):
                # Fallback for Python 3.14 compatibility
                duplicate = django.template.context.Context()
                if hasattr(self, 'dicts'):
                    duplicate.dicts = self.dicts[:]
                else:
                    duplicate.dicts = []
                # Copy other attributes if they exist
                for attr in ['autoescape', 'current_app', 'use_l10n', 'use_tz']:
                    if hasattr(self, attr):
                        setattr(duplicate, attr, getattr(self, attr))
            else:
                raise
        else:
            # Ensure dicts attribute exists
            if not hasattr(duplicate, 'dicts'):
                duplicate.dicts = getattr(self, 'dicts', [])[:]
        return duplicate
    
    # Apply the patch
    django.template.context.Context.__copy__ = _patched_copy

