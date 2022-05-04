from django import template

register = template.Library()


@register.filter()
def censor(value):
    CENS_WORDS = ['что ', 'новости', 'редиска', 'болван', ]
    cens_set = set(CENS_WORDS)
    value_set = set(value.split(' '))

    if value_set.intersection(cens_set):
        bad_words = list(value_set.intersection(cens_set))
        for i in bad_words:

            value = value.replace(i[1::], "*" * (len(i) - 1))

    return value








# def censor(value):
#     OBSCENE_WORDS = ['новость', 'редиска', 'болван', ]
#     value = value.lower()  # создаём для поиска копию текста в нижнем регистре
#     for word in OBSCENE_WORDS:
#         if word.find(value):
#             value = value.replace(word[1::], "*" * len(word))
#             return f'{value}'

