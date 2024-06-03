from django import template

register = template.Library()

@register.filter(name='intcomma_custom')
def intcomma_custom(value):
    """
    Converts an integer to a string containing commas every three digits.
    For example, intcomma_custom(3000) returns '3,000'.
    """
    orig = str(value)
    new = ""
    while orig != "":
        orig, last3 = orig[:-3], orig[-3:]
        if new:
            new = last3 + "," + new
        else:
            new = last3
    return new