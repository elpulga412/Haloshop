def filter_product(request, instance):
    keyword = request.GET['q']
    if keyword == 'duoi-6-trieu':
        items = instance.filter(price__lt=6*(10**6))
    if keyword == 'tu-6-10-trieu':
        items = instance.filter(price__gte=6*(10**6), price__lt=10*(10**6))
    if keyword == 'tu-10-15-trieu':
        items = instance.filter(price__gte=10*(10**6), price__lt=15*(10**6))
    if keyword == 'tu-15-20-trieu':
        items = instance.filter(price__gte=15*(10**6), price__lt=20*(10**6))
    if keyword == 'tren-20-trieu':
        items = instance.filter(price__gte=20*(10**6))
    return items

def sort_product(request, instance):
    keyword = request.GET['sort']
    print(keyword)
    if keyword == 'gia-tu-thap-den-cao':
        items = instance.order_by('price')
    if keyword == 'gia-tu-cao-den-thap':
        items = instance.order_by('-price')
    if keyword == 'moi-cap-nhat':
        items = instance.order_by('updated_at')
    if keyword == 'san-pham-cu':
        items = instance.order_by('-updated_at')
    return items