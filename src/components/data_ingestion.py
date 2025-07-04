import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# -----------------------------
# DataIngestionConfig holds only file paths as configuration
# -----------------------------
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

# -----------------------------
# DataIngestion handles the ingestion logic
# -----------------------------
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion started")
        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info("Dataset read as pandas dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved to artifacts folder")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Train and Test data saved to artifacts folder")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                self.ingestion_config.raw_data_path
            )

        except Exception as e:
            logging.error("Error occurred during data ingestion")
            raise CustomException(e, sys)  # Fixed typo: CustomExceptions -> CustomException

# -----------------------------
# DataTransformationConfig holds transformation config (e.g., file paths)
# -----------------------------
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

# -----------------------------
# DataTransformation handles transformation logic
# -----------------------------
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_data_transformer_object(self):
        # Example: return a scikit-learn ColumnTransformer or Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.compose import ColumnTransformer

        # Dummy example for demonstration
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['feature1', 'feature2'])
            ]
        )
        return preprocessor

# -----------------------------
# Main execution block
# -----------------------------
if __name__ == "__main__":
    # Data ingestion
    data_ingestion = DataIngestion()
    train_data_path, test_data_path, raw_data_path = data_ingestion.initiate_data_ingestion()

    # Data transformation
    data_transformation_config = DataTransformationConfig()
    data_transformation = DataTransformation(data_transformation_config)
    preprocessor_obj = data_transformation.get_data_transformer_object()
    # Now preprocessor_obj is ready to use for fit/transform
