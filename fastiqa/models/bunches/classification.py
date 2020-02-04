from ..bunch import Im2MOS

class IqaCategoryList(CategoryList):
    def __init__(self, items: Iterator, **kwargs):
        super().__init__(items, classes=['bad', 'poor', 'fair', 'good', 'excellent'], **kwargs)

class TwoClasses(Im2MOS):
    label_col = ['class']
    label_cls = CategoryList


class FiveClasses(Im2MOS):
    label_col = 'category'
    label_cls = IqaCategoryList