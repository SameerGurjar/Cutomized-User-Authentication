from django.db import models

# Create your models here.


class Country(models.Model):
    CONTINENTS = (
        ('Asia', 'Asia'),
        ('Europe', 'Europe'),
        ('North America', 'North America'),
        ('Africa', 'Africa'),
        ('Oceania', 'Oceania'),
        ('Antarctica', 'Antarctica'),
        ('South America', 'South America')
       )


    code = models.CharField(max_length=3, default='', unique=True, primary_key=True)
    name = models.CharField(max_length=52, default='')
    continent = models.CharField(max_length=15, choices=CONTINENTS , default='Asia')
    region = models.CharField(max_length=26, default='')
    surface_area = models.FloatField(default=0.00)
    indep_year = models.SmallIntegerField(null=True, blank=True)
    population = models.IntegerField(default=0)
    life_expecttancy = models.FloatField(null=True, blank=True)
    gnp = models.FloatField(null=True, blank=True)
    gnp_old = models.FloatField(null=True, blank=True)
    local_name =  models.CharField(max_length=46, default='')
    government_form = models.CharField(max_length=45, default='')
    head_of_state = models.CharField(max_length=60, null=True, blank=True)
    capital = models.IntegerField(null=True, blank=True)
    code2 = models.CharField(max_length=2, default='')


    def __str__(self):
        return self.code

    @property
    def country_name(self):
        return self.name



class City(models.Model):
    name = models.CharField(max_length=35, default='')
    country_code = models.ForeignKey(Country, on_delete=models.CASCADE)
    district = models.CharField(max_length=100, default='')
    population = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Countrylanguage(models.Model):
    OFFICIAL = (
        ('T', 'T'),
        ('F', 'F')
    )

    country_code = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=30)
    is_offical = models.CharField(max_length=1, choices=OFFICIAL, default='F')
    percentage = models.FloatField(default=0.0)

    class Meta:
        unique_together = (('country_code', 'language'),)


    def __str__(self):
        return self.language

