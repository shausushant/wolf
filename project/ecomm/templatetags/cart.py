from django import template



register = template.Library()


@register.filter(name = 'isexistincart')
def isexitisncart(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False



@register.filter(name="cartquantity")
def cartquantity(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return False


@register.filter(name = "total_price")
def total_price(product,cart):
    return product.price * cartquantity(product,cart)

@register.filter(name="grand_total")
def grand_total(products,cart):
    sum = 0
    for p in products:
        sum += total_price(p,cart)
    return sum
@register.filter(name = "total")
def total(quantity,price):
    return quantity*price

@register.filter(name="total_")
def grand_total(products,cart):
    sum = 0
    for p in products:
        sum += total_price(p,cart)
    return sum


@register.filter(name="total")
def total(price,quantity):
    return price*quantity
