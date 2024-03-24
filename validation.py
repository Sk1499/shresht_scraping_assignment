import operator

class product(object):
    def __init__(self, id, image_link, price, title):
        self.id = id
        self.image = image_link
        self.price = price
        self.title = title
    id = property(operator.attrgetter('_id'))
    @id.setter
    def id(self, i):
        if not i: raise Exception("id cannot be empty")
        self._id = i
    image = property(operator.attrgetter('_image'))
    @image.setter
    def image(self, v):
        if not v: raise Exception("image cannot be empty")
        self._image = v
    price = property(operator.attrgetter('_price'))
    @price.setter
    def price(self, p):
        if not (p > 0): raise Exception("price must be greater than zero")
        self._price = p
    title = property(operator.attrgetter('_title'))
    @title.setter
    def title(self, i):
        if not i: raise Exception("title cannot be empty")
        self._title = i
    

