import sys
from dataclasses import dataclass
import os

import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """ Creates a data transformer object that applies preprocessing steps to the dataset."""
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            logging.info("Creating numerical and categorical transformers")
            numerical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))  # StandardScaler does not support sparse matrices
            ])
            logging.info("Creating preprocessor object with ColumnTransformer")
            # Create a ColumnTransformer to apply the transformers to the respective columns
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numerical_transformer, numerical_columns),
                    ('cat', categorical_transformer, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            logging.error("Error occurred while creating data transformer object")
            raise CustomException(e, sys) from e
        
    def initiate_data_transformation(self, train_path, test_path):
        """ Initiates the data transformation process by reading the train and test datasets,
            applying preprocessing, and saving the preprocessor object."""
        try:
            logging.info("Data Transformation started")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading train and test datasets")
            preprocessor_obj = self.get_data_transformer_object()

            target_column = 'math_score'
            input_features_train = train_df.drop(columns=[target_column], axis=1)
            target_feature_train = train_df[target_column]

            input_features_test = test_df.drop(columns=[target_column], axis=1)
            target_feature_test = test_df[target_column]

            logging.info("Fitting and transforming training data")
            input_features_train_transformed = preprocessor_obj.fit_transform(input_features_train)
            input_features_test_transformed = preprocessor_obj.transform(input_features_test)

            train_arr = np.c_[input_features_train_transformed, np.array(target_feature_train)]
            test_arr = np.c_[input_features_test_transformed, np.array(target_feature_test)]        
            logging.info("Data transformation completed")


            # Save the preprocessor object
            save_object(
                obj=preprocessor_obj,
                file_path=self.data_transformation_config.preprocessor_obj_file_path
            )
            logging.info("Preprocessor object saved")
            return train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            logging.error("Error occurred during data transformation")
            raise CustomException(e, sys) from e
if __name__ == "__main__":
    data_transformation = DataTransformation()