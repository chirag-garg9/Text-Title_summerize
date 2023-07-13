
from src.TextsummerizeProject.constants import *
from src.TextsummerizeProject.utils.common import read_yaml, Create_directory
from src.TextsummerizeProject.entities import DataIngestionconfig
from src.TextsummerizeProject.entities import Datavalidationconfig


class ConfigrationManager:
    def __init__(
            self, 
            config_path = CONFIGPATH, 
            params_path = PARAMSPATH
            ):
        
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)
        print(self.config.artifacts_root)
        Create_directory([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionconfig:
        config = self.config.data_ingestion

        Create_directory([config.root])

        data_ingestion_config = DataIngestionconfig(
            root_dir = config.root,
            source_url = config.source_url,
            local_data_file = config.local_data_file,
            unzip_directory = config.unzip_directory,
        ) 
        
        return data_ingestion_config
    
    def get_data_validation_config(self) -> Datavalidationconfig:
        config = self.config.data_validation

        Create_directory([config.root])

        data_validation_config = Datavalidationconfig(
            root_dir = config.root,
            status_file=config.status_file,
            all_required_files=config.all_required_files
        ) 
        
        return data_validation_config
