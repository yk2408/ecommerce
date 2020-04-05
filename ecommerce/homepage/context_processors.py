from cart.models import CartItem, WishList
from categoryandproduct.models import Brand, SubCategory, SubCategoryMenu
from userprofile.forms import SubscribeForm


def cart_and_wish_count(request):
    username = request.user.username
    cart_item = CartItem.objects.filter(user__username=username).count()
    wish_item = WishList.objects.filter(user__username=username).count()
    return {'count_cart_items': cart_item, 'count_wish_items': wish_item}


def website_menu(request):
    # Electronic Menu :-
    mobile_brand = Brand.objects.filter(sub_category__name="Mobiles")
    laptop_brand = Brand.objects.filter(sub_category__name="Laptops")
    tablet_brand = Brand.objects.filter(sub_category__name="Tablets")
    pc_brand = Brand.objects.filter(sub_category__name="Desktop Pcs")
    elec_sub_cat = SubCategory.objects.filter(category__name="Electronics")
    e_menu = mobile_brand, laptop_brand, tablet_brand, pc_brand
    # Men Menu :-
    top = SubCategoryMenu.objects.filter(sub_category__name="Top wear")
    bottom = SubCategoryMenu.objects.filter(sub_category__name="Bottom wear")
    foot = SubCategoryMenu.objects.filter(sub_category__name="Foot wear", sub_category__category__name="Men")
    seasonal = SubCategoryMenu.objects.filter(sub_category__name="Seasonal wear", sub_category__category__name="Men")
    watches = SubCategoryMenu.objects.filter(sub_category__name="Watches", sub_category__category__name="Men")
    men_sub_cat = SubCategory.objects.filter(category__name="Men")
    men_menu = top, bottom, foot, seasonal, watches
    # Women Menu :-
    top = SubCategoryMenu.objects.filter(sub_category__name="Western wear")
    foot = SubCategoryMenu.objects.filter(sub_category__name="Foot wear", sub_category__category__name="Women")
    seasonal = SubCategoryMenu.objects.filter(sub_category__name="Seasonal wear", sub_category__category__name="Women")
    watches = SubCategoryMenu.objects.filter(sub_category__name="Watches", sub_category__category__name="Women")
    women_menu = top, foot, seasonal, watches
    women_sub_cat = SubCategory.objects.filter(category__name="Women")
    # Newsletters :-
    subscribe_form = SubscribeForm()

    return {
            'E_menu': e_menu,
            'e_sub_cat': elec_sub_cat,
            'Men_menu': men_menu,
            'm_sub_cat': men_sub_cat,
            'Women_menu': women_menu,
            'w_sub_cat': women_sub_cat,
            'subscribe_form': subscribe_form,
            }
