from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(qty, m, *args, **kwargs):

	return qty * m