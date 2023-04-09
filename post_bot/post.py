from datetime import date

class Post:
    def __init__(self, title : str = "", descr : str = "", author_id : str = "", file_id = None):
        self.set_title(title)
        self.set_description(descr)
        self.set_file_id(file_id)
        self.set_author_id(author_id)
        self.__date_time = date.today()

    def __text2md(self, str : str) -> str:
        charset = ['_', '*', '[', '`']
        for i in charset:
            str = str.replace(i,'\\'+i)
        return str


    def set_title(self, title : str) -> None:
        self.__title = title
        
    def get_title(self) -> str:
        return self.__title 

    def set_description(self, description : str) -> None:
        self.__description = description
    
    def get_description(self) -> str:
        return self.__description
    
    def set_author_id(self, author_id : str) -> None:
        self.__author_id = author_id

    def get_author_id(self) -> str:
        return self.__author_id

    def set_file_id(self, file_id : str) -> None:
        self.__file_id = file_id

    def has_file(self) -> bool:
        return True if self.__file_id != None else False

    def get_file_id(self) -> str:
        return self.__file_id
    
    def get_text(self) -> str:
        return '*'+ self.get_title() + '*\n' + self.get_description() + '\n\n Author: @' + self.__text2md(self.get_author_id()) + ''

    def __hash__(self) -> int:
        return hash((self.get_author_id(), self.get_title(), self.get_description(), self.__date_time))

    def __str__(self) -> str:
        return f"Post(title={self._title}, descr={self.__description}, photo={self.__photo})"    