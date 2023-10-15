from .models import *

def menu_context(request):
    categories = Catagory.objects.prefetch_related('subcatagory_set__supersubcatagory_set').all()
    return {'menu_catagory': categories}
