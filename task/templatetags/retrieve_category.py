from django import template

# load the Task and Goal models
from category.models import Category
from task.models import Task

register = template.Library()

@register.filter(name='retrieve_category')
def retrieve_goal(qs):
    return qs.values_list('category')[0][0]

