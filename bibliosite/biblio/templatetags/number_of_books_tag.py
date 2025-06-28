from django.template import Library

register = Library()

@register.simple_tag()
def num(all_books, dist_books):
    rem_books = all_books - len(dist_books)
    if rem_books:
        message = ''
    else:
        message = '(нет в наличии)'
    return message