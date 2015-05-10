from django import template
from userprofile.models import UserProfile

register = template.Library()

@register.filter(name='has_type')
def has_type(user,user_type):
    t = UserProfile.objects.get(user=user)
    if(t.user_type==user_type):
        return True
    else:
        return False
