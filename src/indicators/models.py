from django.db import models

from indicators.algorithm import get_indicators


class Country(models.Model):

    name = models.CharField(max_length=100)
    label = models.CharField(max_length=3)

    def __str__(self):
        return self.label + " " + self.name

    @property
    def indicators(self):
        return get_indicators(
            label=self.label,
            age=self.current.get("age", 18),
            gender=self.current.get("gender", "neither"),
        )
