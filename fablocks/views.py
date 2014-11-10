# -*- coding: utf-8 -*-

from django.views import generic
from fablocks import models


class HomeView(generic.ListView):
    model = models.Block
    template_name = 'home.html'


home = HomeView.as_view()
