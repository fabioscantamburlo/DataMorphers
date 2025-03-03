import pandas as pd
from typing import Any
from datamorphers.base import DataMorpher


class AddColumn(DataMorpher):
    def __init__(self, column_name: str, value: Any):
        super().__init__()
        self.column_name = column_name
        self.value = value

    def _datamorph(self, df):
        """Adds a new column with a constant value to the dataframe."""
        df[self.column_name] = self.value
        return df


class ColumnsOperator(DataMorpher):
    def __init__(
        self, first_column: str, second_column: str, logic: str, output_column: str
    ):
        """Logic can be sum, sub, mul, div."""
        super().__init__()
        self.first_column = first_column
        self.second_column = second_column
        self.logic = logic
        self.output_column = output_column

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs an operation on the values in the specified column by
            the values inanother column.
        Renames the resulting column as 'output_column'.
        """
        if self.logic == "sum":
            df[self.output_column] = df[self.first_column] + df[self.second_column]
        if self.logic == "sub":
            df[self.output_column] = df[self.first_column] - df[self.second_column]
        if self.logic == "mul":
            df[self.output_column] = df[self.first_column] * df[self.second_column]
        if self.logic == "div":
            df[self.output_column] = df[self.first_column] / df[self.second_column]
        return df


class DeleteDataFrame(DataMorpher):
    def __init__(self, file_name: str):
        super().__init__()
        self.file_name = file_name

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Deletes a DataFrame previously saved using pickle."""
        import os.path

        if os.path.isfile(f"{self.file_name}.pkl"):
            os.remove(f"{self.file_name}.pkl")
        return df


class DropNA(DataMorpher):
    def __init__(self, column_name: str):
        super().__init__()
        self.column_name = column_name

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drops rows with any NaN values."""
        df = df.dropna(subset=self.column_name)
        return df


class FillNA(DataMorpher):
    def __init__(self, column_name: str, value: Any):
        super().__init__()
        self.column_name = column_name
        self.value = value

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fills NaN values in the specified column with the provided value."""
        df[self.column_name] = df[self.column_name].fillna(self.value)
        return df


class FilterRows(DataMorpher):
    def __init__(self, *, first_column: str, second_column: str, logic: str):
        """Logic can be e, g, l, ge, le."""
        super().__init__()
        self.first_column = first_column
        self.second_column = second_column
        self.logic = logic

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filters rows based on a condition in the specified column."""
        if self.logic == "e":
            df = df.loc[df[self.first_column] == df[self.second_column]]
        elif self.logic == "g":
            df = df.loc[df[self.first_column] > df[self.second_column]]
        elif self.logic == "ge":
            df = df.loc[df[self.first_column] >= df[self.second_column]]
        elif self.logic == "l":
            df = df.loc[df[self.first_column] < df[self.second_column]]
        elif self.logic == "le":
            df = df.loc[df[self.first_column] <= df[self.second_column]]
        return df


class MathOperator(DataMorpher):
    def __init__(self, column_name: str, logic: str, value: float, output_column: str):
        """Logic can be sum, sub, mul, div."""
        super().__init__()
        self.column_name = column_name
        self.logic = logic
        self.value = value
        self.output_column = output_column

    def _datamorph(self, df):
        """Math operation between a column and a value, with the operation defined in logic."""
        if self.logic == "sum":
            df[self.output_column] = df[self.column_name] + self.value
        elif self.logic == "sub":
            df[self.output_column] = df[self.column_name] - self.value
        elif self.logic == "mul":
            df[self.output_column] = df[self.column_name] * self.value
        elif self.logic == "div":
            df[self.output_column] = df[self.column_name] / self.value
        return df


class MergeDataFrames(DataMorpher):
    def __init__(
        self, df_to_join: pd.DataFrame, join_cols: list, how: str, suffixes: list
    ):
        super().__init__()
        self.df_to_join = df_to_join
        self.join_cols = join_cols
        self.how = how
        self.suffixes = suffixes

    @staticmethod
    def _handle_args(args: dict, extra_dfs: dict):
        args["df_to_join"] = extra_dfs[args["df_to_join"]]
        return args

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Merges two DataFrames."""
        merged_df = pd.merge(
            df,
            self.df_to_join,
            on=self.join_cols,
            how=self.how,
            suffixes=self.suffixes,
        )
        return merged_df


class NormalizeColumn(DataMorpher):
    def __init__(self, column_name: str, output_column: str):
        super().__init__()
        self.column_name = column_name
        self.output_column = output_column

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize a numerical column in the dataframe using Z-score normalization."""
        df[self.output_column] = (
            df[self.column_name] - df[self.column_name].mean()
        ) / df[self.column_name].std()
        return df


class RemoveColumns(DataMorpher):
    def __init__(self, columns_name: list | str):
        super().__init__()
        self.columns_name = (
            columns_name if type(columns_name) is list else [columns_name]
        )

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Removes a specified column from the DataFrame."""
        df = df.drop(columns=self.columns_name, errors="ignore")
        return df


class RenameColumn(DataMorpher):
    def __init__(self, old_column_name: str, new_column_name: str):
        super().__init__()
        self.old_column_name = old_column_name
        self.new_column_name = new_column_name

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renames a column in the dataframe."""
        df = df.rename(columns={self.old_column_name: self.new_column_name})
        return df


class SaveDataFrame(DataMorpher):
    def __init__(self, file_name: str):
        super().__init__()
        self.file_name = file_name

    def _datamorph(self, df: pd.DataFrame) -> pd.DataFrame:
        """Saves a DataFrame using pickle."""
        df.to_pickle(f"{self.file_name}.pkl")
        return df
