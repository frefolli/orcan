
class Post:
    def __init__(self, title : str = "", descr : str = "", photo = None):
        self.__title = title
        self.__description = descr
        self.__photo = photo

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def get_title(self):
        return self.__title 
    
    def get_description(self):
        return self.__description
    
    def get_photo(self, photo):
        return self.__photo

    def __str__(self) -> str:
        return f"Post(title={self._title}, descr={self.__description}, photo={self.__photo})"    