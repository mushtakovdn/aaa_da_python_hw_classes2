import keyword
from typing import Union
import json


class ColorizeMixin:
    """
    Меняет цвет текста при выводе текстового представления объекта в консоль
    задает цвет в атрибуте класса repr_color_code
    """
    def __init_subclass__(cls, repr_color_code):
        """
        При инициализации класса наследника ему пробрасывается атрибу класс,
        отвечающий за цвет текста в текстовом представлении объектов
        """
        super().__init_subclass__()
        cls.repr_color_code = repr_color_code

    def __repr__(self):
        return f'\033[0;{str(self.repr_color_code)};40m'


class Advert(ColorizeMixin, repr_color_code=33):
    """
    Парсер словарей (json) в питоновские объекты
    """

    def __init__(self, mapping: dict, is_nested=False):
        self._is_nested = is_nested
        self._parse_dict(mapping)

    def __repr__(self):
        if 'repr_color_code' in Advert.__dict__:
            prefix = super().__repr__()
            return f'{prefix}{self.title} | {self.price}\033[0m'
        else:
            return f'{self.title} | {self.price}'

    @property
    def price(self):
        if '_price' in self.__dict__:
            return self._price
        else:
            return 0

    @price.setter
    def price(self, value: Union[float, int]):
        if value >= 0:
            self._price = value
        else:
            raise ValueError('ValueError: must be >= 0')

    def _parse_dict(self, mapping: dict):
        """
        Парсинг входного словаря
        """
        for attr, value in mapping.items():
            # В случае вложенности параметра заводится новый объект
            if isinstance(value, dict):
                value = Advert(value, is_nested=True)
            if attr != 'price':
                if keyword.iskeyword(attr):
                    attr += '_'
                self.__dict__[attr] = value
            else:
                self.price = value

        # если корневой объект (первого уровня) то обязательно наличие title
        if not self._is_nested and 'title' not in mapping:
            raise ValueError('На первом уровне обязательно наличие "title"')


if __name__ == '__main__':
    dog_str = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "nested_params": {
            "weight": 3.5,
            "color": "white and black",
            "height": 0.35
        }
    }"""
    dog = json.loads(dog_str)
    dog_ad = Advert(dog)
    print('price:', dog_ad.price)
    print('height:', dog_ad.nested_params.height)
    print(dog_ad)
