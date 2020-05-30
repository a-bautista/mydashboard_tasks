from django import template

# load the Task and Goal models
from goal.models import Goal
from task.models import Task


register = template.Library()

@register.filter(name='retrieve_goal')
def retrieve_goal(qs):
    return qs.values_list('goal')[0][0]

