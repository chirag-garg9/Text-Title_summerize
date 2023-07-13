import os
import urllib.request as request
import zipfile
from pathlib import Path
from src.TextsummerizeProject.logging import logger
from src.TextsummerizeProject.utils.common import get_size
from src.TextsummerizeProject.entities import DataIngestionconfig
from src.TextsummerizeProject.entities import Datavalidationconfig

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