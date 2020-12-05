from abc import abstractmethod, ABC
import pandas as pd


class DataLoader(ABC):

    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        pass


class FileLoader(DataLoader):

    def __init__(self, path: str):
        self.path = path

    def get_data(self) -> pd.DataFrame:
        return self.df_from_file()

    @staticmethod
    def file_mapping():
        return {
            'csv': CsvDataLoader,
            'xlsx': ExcelDataLoader
        }

    @abstractmethod
    def df_from_file(self) -> pd.DataFrame:
        pass


class CsvDataLoader(FileLoader):

    def df_from_file(self) -> pd.DataFrame:
        return pd.read_csv(self.path, delimiter=';')


class ExcelDataLoader(FileLoader):

    def df_from_file(self) -> pd.DataFrame:
        return pd.read_csv(self.path)
