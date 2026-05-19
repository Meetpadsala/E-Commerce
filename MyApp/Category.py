from .models import*

def Cat(request):
    cate=Category.objects.all()
    
    wcount=0
    ccount=0
    if request.user.is_authenticated:
        wcount=Wishlist.objects.filter(u_id=request.user).count()
        ccount=Cart.objects.filter(u_id=request.user).count()

    return {'cate':cate,'wcount':wcount,'ccount':ccount}
