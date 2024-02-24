from os import curdir, walk
from os.path import dirname, isdir, splitext
from typing import TypeAlias

Analytics: TypeAlias = dict[str: (str | None, bool, str | None)]


class FileSystemAnalyzer:
    """
    Анализатор файловой системы компьютера, на котором выполняется данный программный код. Предоставляет базовую
    характеристику папок и файлов по зафиксированному в экземпляре класса пути. Если путь не передан или передан
    неверно, используется текущий путь.
    """

    def __init__(self, folder_path: str = None) -> None:
        self._folder_path = folder_path if (folder_path is not None and isdir(folder_path)) else curdir

    @property
    def folder_path(self) -> str:
        return self._folder_path

    @folder_path.setter
    def folder_path(self, folder_path: str) -> None:
        self._folder_path = folder_path if (folder_path is not None and isdir(folder_path)) else curdir

    def analyze(self) -> Analytics:
        """
        Анализирует имя, расширения, флаг папки и название родительской папки для каждого объекта файловой системы
        (файла или папки), начиная с корня пути Анализатора. Для объектов, не имеющих какого-либо из анализируемых
        свойств, его значения определяется как None.

        :return: словарь, где ключом является имя объекта (в случае с файлом — без расширения), а значением — кортеж,
                 с расширением объекта, флагом каталога и названием родительского каталога.
        """
        analytics: Analytics = {}
        for current_folder, folders, files in walk(self._folder_path):
            for folder in folders:
                parent_folder = dirname(current_folder)
                analytics[folder] = (None, True, parent_folder if parent_folder else None)
            for file in files:
                basename, extension = splitext(file)
                parent_folder = dirname(current_folder)
                analytics[basename] = (extension if extension else None, False,
                                       parent_folder if parent_folder else None)
        return analytics
