from django_filters import FilterSet, ModelChoiceFilter, DateFromToRangeFilter, ChoiceFilter
from .models import Post, Author, User


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class NewsFilter(FilterSet):
    dateCreation = DateFromToRangeFilter(
        label='По дате'
    )
    author = ModelChoiceFilter(
        field_name='author__authorUser',
        queryset=User.objects.all(),
        label='По автору'
    )


    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию

            'title': ['icontains'],




        }
