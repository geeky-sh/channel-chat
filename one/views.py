# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render


def test(request):
    name = request.GET.get('name') or 'aash'
    return render(request, 'templates/test.html', {'name': name})
