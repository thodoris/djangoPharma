from cart.cart import Cart


def user_cart(request):
    def inner():
        cart = Cart(request)
        cart_is_empty = cart.count() == 0
        return {
            'cart': cart,
            'cart_is_empty': cart_is_empty
        }
    return {'user_cart': inner}
