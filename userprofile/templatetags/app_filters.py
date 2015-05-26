from django import template
from userprofile.models import UserProfile

register = template.Library()

@register.filter(name="has_delete")
def is_delete(cell,delete):
    if(str(cell) == "delete"):
        return True
    else:
        return False


@register.filter(name='has_type')
def has_type(user,user_type):
    t = UserProfile.objects.get(user=user)
    if(t.user_type==user_type):
        return True
    else:
        return False

@register.filter(name='has_registered')
def has_registered(user,registered):
    u = UserProfile.objects.get(user=user)
    if(u.registered == True):
        return True
    else:
        return False
