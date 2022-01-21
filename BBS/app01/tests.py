from django.test import TestCase

# Create your tests here.
import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BBS.settings")
    import django
    django.setup()
    from app01 import views
    form_boj = views.MyRegForm()
    print(form_boj.changed_data)
