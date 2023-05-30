from datetime import date
from utils.config import text2md

class Post:
    def __init__(self, title : str = "", descr : str = "", author_name : str = "", author_last : str = "", author_id : str = "", file_id = None):
        self.set_title(title)
        self.set_description(descr)
        self.set_file_id(file_id)
        self.set_author_name(author_name)
        self.set_author_last(author_last)
        self.set_author_id(author_id)
        self.__date_time = date.today()

    def set_title(self, title : str) -> None:
        self.__title = title
        
    def get_title(self) -> str:
        return self.__title 

    def set_description(self, description : str) -> None:
        self.__description = description
    
    def get_description(self) -> str:
        return self.__description
    
    def get_author_complete_name(self) -> str:
        return self.__author_name + ' ' + self.__author_last
    
    def get_author_user_link(self) -> str:
        return "tg://user?id=" + self.__author_id
    
    def set_author_name(self, author_name : str) -> None:
        self.__author_name = author_name

    def set_author_last(self, author_last : str) -> None:
        self.__author_last = author_last

    def set_author_id(self, author_id : str) -> None:
        self.__author_id = str(author_id)

    def set_file_id(self, file_id : str) -> None:
        self.__file_id = file_id

    def has_file(self) -> bool:
        return True if self.__file_id != None else False

    def get_file_id(self) -> str:
        return self.__file_id
    
    def get_text(self) -> str:
        return '*'+ text2md(self.get_title()) + '*\n' + text2md(self.get_description()) + '\n\n Author: [' + text2md(self.get_author_complete_name()) + ']('+ self.get_author_user_link() +')'

    def __hash__(self) -> int:
        return hash((self.get_author_id(), self.get_title(), self.get_description(), self.__date_time))

    def __str__(self) -> str:
        return f"Post(title={self._title}, descr={self.__description}, photo={self.__photo})"    