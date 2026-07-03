from .models import Category

def categories(request):
    """
    Makes all categories available in every template.
    """
    return {
        'all_categories': Category.objects.all()
    }
