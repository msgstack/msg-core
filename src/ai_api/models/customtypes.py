__author__ = "root"
__date__ = "09/03/2022, 02:00 PM"

from django.db import models


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        return "tinyint"


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        return "tinyint unsigned"


class NormalTextField(models.TextField):
    def db_type(self, connection):
        return "text"


class MediumTextField(models.TextField):
    def db_type(self, connection):
        return "MEDIUMTEXT"


class SimpleDateTimeField(models.DateTimeField):
    def db_type(self, connection):
        return "datetime"
