def set_test_databases(settings, base_dir):
    settings["DATABASES"] = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(base_dir / 'default.sqlite3')
        },
        'users': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(base_dir / 'users.sqlite3')
        }
    }
