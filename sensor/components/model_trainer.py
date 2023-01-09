from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os,sys 
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sensor import utils
from sklearn.metrics import f1_score
from sensor.config import params



class ModelTrainer:


    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def fine_tune(self,x,y):
        try:
            
            #Wite code for Grid Search CV
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            xgb_clf_=XGBClassifier()
            grid_cv = GridSearchCV(estimator=xgb_clf_, param_grid=params , n_jobs= 4 , cv = cv) 
            grid_cv.fit(x,y)
            xgb_clf_grid =  XGBClassifier(**grid_cv.best_params_)
            xgb_clf_grid.fit(x,y) 
            return xgb_clf_grid

        except Exception as e:
            raise SensorException(e, sys)

    def train_model(self,x,y):
        try:
            xgb_clf =  XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)


    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Train the model")
            model = self.train_model(x=x_train,y=y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train = model.predict(x_train)
            f1_train_score  =f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score  =f1_score(y_true=y_test, y_pred=yhat_test)

            """#Grid Search CV
            logging.info(f"Grid Search CV and Train the new model on top of those paramters")
            model_grid = self.fine_tune(x=x_train,y=y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train_grid = model_grid.predict(x_train)
            f1_train_grid_score  =f1_score(y_true=y_train, y_pred=yhat_train_grid)
            
            logging.info(f"Calculating f1 test score")
            yhat_test_grid = model_grid.predict(x_test)
            f1_test_grid_score  =f1_score(y_true=y_test, y_pred=yhat_test_grid)

            # comparision
            logging.info(f"comparing both the models")
            logging.info(f"default model --> train score:{f1_train_score} and tests score {f1_test_score}")
            logging.info(f"tuned model   --> train score:{f1_train_grid_score} and tests score {f1_test_grid_score}")

            if f1_test_score<f1_test_grid_score :

                logging.info("we are selecting tuned model ")
                logging.info("updating model")
                model = model_grid
                yhat_train = yhat_train_grid
                f1_train_score  =f1_train_grid_score
                yhat_test = yhat_test_grid
                f1_test_score = f1_test_grid_score          
            else: 
                logging.info("we are selecting our default model")"""
            


            # final model after comparision
            
            logging.info(f"train score:{f1_train_score} and tests score {f1_test_score}")
            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(f1_train_score-f1_test_score)

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
