from .models import Wishlist

def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        wishlist = Wishlist.objects.filter(session_key=session_key).first() if session_key else None
        
    if wishlist:
        count = wishlist.items.count()
    return {'wishlist_item_count': count}
