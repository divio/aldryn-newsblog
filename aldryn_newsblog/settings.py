# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

ENABLE_REVERSION = getattr(settings, 'ALDRYN_NEWBLOG_ENABLE_REVERSION', False)
