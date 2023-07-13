import os
import urllib.request as request
import zipfile
from pathlib import Path
from src.TextsummerizeProject.logging import logger
from src.TextsummerizeProject.utils.common import get_size
from src.TextsummerizeProject.entities import DataIngestionconfig
from src.TextsummerizeProject.entities import Datavalidationconfig
from src.TextsummerizeProject.entities import Datatransformationconfig
from transformers import AutoTokenizer
import pandas as pd
import re
import pickle

class DataIngestion:
    def __init__(self, config: DataIngestionconfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, header = request.urlretrieve(
                url = self.config.source_url,
                filename= self.config.local_data_file
            )
            logger.info(f"{filename} download with following info: \n{header}")
        else:
            logger.info(f"{self.config.local_data_file} already exists of size {get_size(Path(self.config.local_data_file))}")
    
    def extract_file(self):
        '''Extracts the ZIP file'''
        unzip_path = Path(self.config.unzip_directory)
        with zipfile.ZipFile(self.config.local_data_file,'r') as unzip_file:
            unzip_file.extractall(unzip_path)


class Datavalidation:
    def __init__(self,config:Datavalidationconfig):
        self.config = config

    def validate(self)->bool:
        try:
            validation_status = None    
            all_files = os.listdir(os.path.join('artifacts','data_ingestion'))

            for file in all_files:
                if file not in self.config.all_required_files:
                    validation_status = False
                    with open(self.config.status_file,'w') as f:
                        f.write(f'validation_status: {validation_status}')
                else:
                    validation_status = True
                    with open(self.config.status_file,'w') as f:
                        f.write(f'validation_status: {validation_status}')

        except Exception as e:
            raise e
    
class Datatransformation:
    def __init__(self, config:Datatransformationconfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)


    def covert_to_features(self,source,target   ):
        input_encoding = self.tokenizer(source,max_length=1024,truncation=True,padding=True,is_split_into_words=True)

        with self.tokenizer.as_target_tokenizer():
            target_encoding = self.tokenizer(target,max_length=128,truncation=True,padding=True,is_split_into_words=True)

        return{
            'input_ids': input_encoding['input_ids'],
            'attention_mask': input_encoding['attention_mask'],
            'labels': target_encoding['input_ids']
            }

    def convert(self):
        sci_dataset = pd.read_json(self.config.data_path,lines=True)
        sci_dataset.dropna()
        # sci_dataset['source']=sci_dataset['source'].apply(lambda x: re.sub('<>:/\\|\?\*','',x))
        # sci_dataset['test']=sci_dataset['test'].apply(lambda x: re.sub('<>:/\\|\?\*','',x))
        x_train = list(sci_dataset['source'])
        y_train = list(sci_dataset['target'])
        sci_dataset_test = pd.read_json(self.config.data_path_test,lines=True)
        sci_dataset_test.dropna()
        # sci_dataset_test['source']=sci_dataset_test['source'].apply(lambda x: re.sub('<>:/\\|?*','',x))
        # sci_dataset_test['test']=sci_dataset_test['test'].apply(lambda x: re.sub('<>:/\\|?*','',x))
        x_test = list(sci_dataset['source'])
        y_test = list(sci_dataset['target'])
        dataset_pt = self.covert_to_features(x_train,y_train)
        dataset_pt_test = self.covert_to_features(x_train,y_train) 
        path,_ = os.path.split(self.config.data_path)
        path_test,_ = os.path.split(self.config.data_path_test)
        path = os.path.join(self.config.root_dir,'train.pkl')
        path_test = os.path.join(self.config.root_dir,'test.pkl')
        with open(path, 'wb') as f:
            pickle.dump(dataset_pt, f)
        with open(path_test, 'wb') as f:
            pickle.dump(dataset_pt_test, f)