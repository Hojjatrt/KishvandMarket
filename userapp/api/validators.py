from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def NumericValidator(value):
    if value.isdigit():
        raise ValidationError(
            _("This Username is entirely numeric."),
            code='invalid',
        )


def FirstNumericValidator(value):
    if value[0].isdigit():
        raise ValidationError(
            _("This Username begin with number."),
            code='invalid',
        )


def phoneValidator(value):
    if not value.isdigit() or value[:2] != '09' or len(value) != 11:
        raise ValidationError(
            _("This Phone Number is not valid."),
            code='invalid',
        )
