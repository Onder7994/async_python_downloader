import argparse
import os
from dataclasses import dataclass

@dataclass
class CommandLineParser:
    """Основной класс для CLI"""
    urls_file_path: str
    save_dir: str

    @classmethod
    def create_parser(cls):
        """Создаем CLI в методе класса"""
        parser = argparse.ArgumentParser(description="Async downloader")
        parser.add_argument(
            "-u", "--urls", dest="urls_file_path",
            required=False,
            default="urls.json",
            help="Path for url file"
        )
        parser.add_argument(
            "-d", "--dir",
            dest="save_dir",
            required=False,
            default=os.getcwd(),
            help="Save directory for download files"
        )
        
        return parser          