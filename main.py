from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
from  sensor.entity.config_entity import TrainingPipelineConfig 
from  sensor.entity.config_entity import  DataIngestionConfig
from  sensor.entity.config_entity import  DataValidationConfig
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
import sys,os

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)

        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        data_validation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact= data_ingestion_artifact)

        data_validation_artifact=data_validation.initiate_data_validation()


    except Exception as e:
        print(e)