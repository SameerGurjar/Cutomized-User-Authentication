from django.shortcuts import render
from .models import City, Country, Countrylanguage
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.



def auto_suggest(request):
    if request.is_ajax():
        keyword = request.GET.get('keyword', False)
        if keyword == '':
            return HttpResponse('')

        city_qs = City.objects.filter(name__startswith=keyword)
        city_list = [city.name for city in city_qs]

        country_qs = Country.objects.filter(name__startswith=keyword)
        country_list = [country.name for country in country_qs]

        language_qs = Countrylanguage.objects.filter(language__startswith=keyword)
        language_list = [l.language for l in language_qs]

        suggest_list = city_list + country_list + language_list

        html_string = ''
        for suggest in suggest_list:
            html_string += '<li onClick=\"selectKeyword(\'' + suggest + '\')\">' + suggest + '</li>'

        html_string =  '<ul id="country-list">' + html_string + '</ul>'
        return HttpResponse(html_string)



@login_required(login_url='/login/')
def world_detail(request):

    obj_list = None
    fields = None

    keyword = request.GET.get('search', None)

    if keyword == '' or keyword is None:
        return reverse("auto_suggest")


    city_qs = City.objects.filter(name=keyword)
    if city_qs.exists():
        obj_list = city_qs.values()
        fields = City._meta.get_fields(include_parents=False)



    country_qs = Country.objects.filter(name=keyword)
    if country_qs.exists():
        obj_list = country_qs.values()
        fields = Country._meta.get_fields(include_parents=False)



    language_qs = Countrylanguage.objects.filter(language=keyword)
    if language_qs .exists():
        obj_list = language_qs.values()
        fields = Countrylanguage._meta.get_fields(include_parents=False)


    context = {
        'obj_list': obj_list,
        'fields': fields
    }

    return render(request, 'world_detail.html', context)
