from django.conf import settings
from .models import Category

def categories(request):
    """
    Makes all categories and WhatsApp number available in every template.
    """
    return {
        'all_categories': Category.objects.all(),
        'whatsapp_number': getattr(settings, 'WHATSAPP_NUMBER', '918086297803')
    }

