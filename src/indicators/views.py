from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse

from indicators.models import Country


class HomeView(TemplateView):
    template_name = "indicators/home.html"


class CountriesView(ListView):
    model = Country
    context_object_name = "country_list"
    ordering = ["name"]

    def post(self, request):
        choice = request.POST["country"]
        country_pk = Country.objects.filter(label=choice).first().pk
        age = request.POST["age"]
        gender = request.POST["gender"]
        if age == "":
            age = "18"
        return redirect(f"{reverse('countries')}{country_pk}?age={age}&gender={gender}")


class IndicatorView(DetailView):
    template_name = "indicators/indicator_view.html"

    def get_object(self, queryset=None):
        country = Country.objects.filter(pk=self.kwargs["pk"]).first()
        country.current = self.request.GET
        return country
