HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
    ),
    'INSTALLED_APPS': [
        'reversion',
        'aldryn_newsblog',
        'aldryn_people',
        'filer',
        'djangocms_text_ckeditor',
    ],
    # app-specific
    'ALDRYN_NEWSBLOG_PAGINATE_BY': 10,
}
