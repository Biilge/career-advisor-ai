from pathlib import Path
import pandas as pd


class JobLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        """Loads the job skills dataset."""

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.file_path}"
            )

        df = pd.read_csv(
            self.file_path,
            compression="zip"
        )

        print("Dataset loaded successfully!")
        print(f"Total records: {len(df)}")
        print(f"Columns: {list(df.columns)}")

        return df