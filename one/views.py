# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse


def test(request):
    return JsonResponse({'success': True})
