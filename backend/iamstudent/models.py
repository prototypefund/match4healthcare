from django.db import models
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError
from mapview.utils import plzs
from django.utils.translation import gettext as _
from accounts.models import User


def validate_semester(value):
    if value < 0:
        raise ValidationError(_("Semester darf nicht negativ sein"))
    else:
        return value


class Student(models.Model):
    """A typical class defining a model, derived from the Model class."""

    class Bezahlung(models.IntegerChoices):
        UNENTGELTLICH = 1
        BEZAHLUNG = 4

    class Verfuegbarkeiten(models.IntegerChoices):
        TEN = 1
        TWENTY = 2
        THIRTY = 3
        FOURTY = 4

    class Ampel(models.IntegerChoices):
        ROT = 1
        GELB = 2
        GRUEN = 3

    class Umkreise(models.IntegerChoices):
        LESSFIVE = 1
        LESSTEN = 2
        LESSTWENTY = 3
        MORETWENTY = 4



    ## Database stuff
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    COUNTRY_CODE_CHOICES = [
        ("DE", 'Deutschland'),
        ("AT", 'Österreich'),
    ]
    countrycode = models.CharField(
        max_length=2,
        choices=COUNTRY_CODE_CHOICES,
        default="DE",
    )
    # Allgemeines

    # vorerkrankungen
    # Berufserfahrung

    # TODO add more validators!

    # Bezahlung

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    name_first = models.CharField(max_length=50, default='')
    name_last = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=100, blank=True, default='')

    plz = models.CharField(max_length=5, null=True)
    umkreis = models.IntegerField(choices=Umkreise.choices, null=True, blank=False)
    availability_start = models.DateField(null=True)



    braucht_bezahlung = models.IntegerField(choices=Bezahlung.choices,
                                            default=Bezahlung.UNENTGELTLICH)  # RADIO BUTTONS IM FORM!

    zeitliche_verfuegbarkeit = models.IntegerField(choices=Verfuegbarkeiten.choices, null=True, blank=False)

    """
    vorausbildung_typ_krankenpflege = models.BooleanField(default=False)
    vorausbildung_typ_intensiv = models.BooleanField(default=False)
    vorausbildung_typ_innere = models.BooleanField(default=False)
    vorausbildung_typ_anaesthesie = models.BooleanField(default=False)
    vorausbildung_typ_pflege = models.BooleanField(default=False)
    vorausbildung_typ_rettungsdienst = models.BooleanField(default=False)
    vorausbildung_typ_hebamme = models.BooleanField(default=False)
    vorausbildung_typ_labor = models.BooleanField(default=False)
    vorausbildung_typ_verwaltunglogistik = models.BooleanField(default=False)
    vorausbildung_typ_fsjgesundheitswesen = models.BooleanField(default=False)
    vorausbildung_typ_blutentnahmedienst = models.BooleanField(default=False)
    vorausbildung_typ_kinderbetreuung = models.BooleanField(default=False)
    """

    ### TODO:

    # ausbildung_mfa_details
    # ausbildung_mta_details
    # ausbildung_mtla_details
    # ausbildung_notfallsani_details
    # ausbildung_pflegestud_details
    # ausbildung_sani_details
    # ausbildung_zahni_details
    # ausbildung_kindebetreuung_details

    # Metadata
    class Meta:
        ordering = ['plz']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.user.email

    def clean(self):
        if self.plz not in plzs[self.countrycode]:
            raise ValidationError(str(self.plz) + _(" ist keine Postleitzahl in ") + self.countrycode)


"""Add stufff to model"""
wunschorte = ['arzt', 'gesundheitsamt', 'krankenhaus', 'pflege', 'rettungsdienst', 'labor']
wunschorte_prefix = 'wunsch_ort'
for w in wunschorte:
    Student.add_to_class('%s_%s' % (wunschorte_prefix.lower(),w.lower()), models.BooleanField(default=False))


class Arzttyp(models.IntegerChoices):
    ANAESTHESIE = 1
    CHIRURGIE = 2
    INNERE = 3
    INTENSIV = 4
    NOTAUFNAHME = 5
    ANDERE = 6


class MedstudAbschnitt(models.IntegerChoices):
    VORKLINIK = 1
    KLINIK = 2
    PJ = 3


AUSBILDUNGS_TYPEN = {
    'ARZT':
        {
            'typ': models.IntegerField(choices=Arzttyp.choices, null=True),
            'sonstige': models.CharField(max_length=50, default='')
        },
    'MEDSTUD':
        {
            'abschnitt': models.IntegerField(choices=MedstudAbschnitt.choices, null=True),
            'farmulaturen_anaesthesie': models.BooleanField(default=False),
            'famulaturen_chirurgie': models.BooleanField(default=False),
            'famulaturen_innere': models.BooleanField(default=False),
            'famulaturen_intensiv': models.BooleanField(default=False),
            'famulaturen_notaufnahme': models.BooleanField(default=False),
            'anerkennung_noetig': models.BooleanField(default=False)
        },
    'MFA':
        {
            'todo': models.BooleanField(default=False)
        },
    'MTLA':
        {
            'todo': models.BooleanField(default=False)
        },
    'MTA': {
        'todo': models.BooleanField(default=False)
    },
    'NOTFALLSANI': {
        'todo': models.BooleanField(default=False)
    },
    'SANI': {
        'todo': models.BooleanField(default=False)
    },
    'ZAHNI': {
        'todo': models.BooleanField(default=False)
    },
    'KINDERBETREUNG': {
        'todo': models.BooleanField(default=False)
    },
    'SONSTIGE': {
        'todo': models.BooleanField(default=False)
    },
}
AUSBILDUNGS_IDS = dict(zip(AUSBILDUNGS_TYPEN.keys(),range(len(AUSBILDUNGS_TYPEN))))

for ausbildungs_typ, felder in AUSBILDUNGS_TYPEN.items():
    Student.add_to_class('ausbildung_typ_%s' % ausbildungs_typ.lower(), models.BooleanField(default=False))
    for key, field in felder.items():
        Student.add_to_class('ausbildung_typ_%s_%s' % (ausbildungs_typ.lower(), key.lower()), field)

"""End"""


import django_filters
from django import forms
from django.db import models


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {}
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
