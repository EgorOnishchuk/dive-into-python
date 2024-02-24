from argparse import ArgumentParser
from logging import basicConfig, DEBUG, getLogger
from os import curdir


class CommandLineInterface:
    """
    Интерфейс командной строки для анализа файловой системы. Принимает от пользователя пути к журналируемой папке и
    файлу для хранения журнала с результатами анализа.
    """
    LOGGING_FORMAT: str = "{levelname} — {asctime}. Модуль '{name}', функция или метод '{funcName}', строка {lineno}." \
                          " Проанализирован объект файловой системы: '{msg}' в {created} c."
    DEFAULT_FOLDER = [curdir]
    DEFAULT_FILE = ['log.txt']

    def __init__(self, file_system_analyzer) -> None:
        self._file_system_analyzer = file_system_analyzer
        self._argument_parser = ArgumentParser(prog='Система журналирования файловой системы',
                                               description='Журналирует базовые характеристики файлов и папок')
        self._argument_parser.add_argument('-folder', metavar='Папка', type=str, nargs='*',
                                           help='Путь к журналируемой папке.', default=self.DEFAULT_FOLDER)
        self._argument_parser.add_argument('-log', metavar='Журнал', type=str, nargs='*',
                                           help='Путь к файлу для журнала', default=self.DEFAULT_FILE)

    def run(self) -> None:
        """
        Анализирует файловую систему и записывает результаты в журнал. Если пути не переданы, журналируемой становится
        текущая папка, а файлом для журнала — файл "log.txt" в текущей папке. При передаче в качестве одного аргумента
        нескольких путей, учитывается только первый.
        """
        arguments = self._argument_parser.parse_args()
        analytics = self._file_system_analyzer(arguments.folder[0]).analyze()
        basicConfig(filename=arguments.log[0], format=self.LOGGING_FORMAT, style='{', level=DEBUG, encoding='UTF-8')
        logger = getLogger(__name__)
        for object_ in analytics.items():
            logger.debug(object_)
