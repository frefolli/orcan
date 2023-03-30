
class Post:
    def __init__(self, title : str = "", descr : str = "", file_id = None):
        self.set_title(title)
        self.set_description(descr)
        self.set_file_id(file_id)

    def set_title(self, title : str) -> None:
        self.__title = title

    def set_description(self, description : str) -> None:
        self.__description = description
    
    def set_file_id(self, file_id : str) -> None:
        self.__file_id = file_id

    def get_title(self) -> str:
        return self.__title 
    
    def get_description(self) -> str:
        return self.__description
    
    def has_file(self) -> bool:
        return True if self.__file_id != None else False

    def get_text(self) -> str:
        return self.get_title() + '\n' + self.get_description()

    def get_file_id(self) -> str:
        return self.__file_id

    def __str__(self) -> str:
        return f"Post(title={self._title}, descr={self.__description}, photo={self.__photo})"    