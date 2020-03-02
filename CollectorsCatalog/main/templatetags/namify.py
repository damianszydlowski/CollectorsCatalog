from django import template

from main.models import Category

register = template.Library()


@register.filter
def get_name(value):
    slug = value.split('/')[-1]
    category = Category.objects.get(slug=slug)
    return category.name
