import os
import logging
import sys

log_dir = 'logs'
log_filepath = os.path.join(log_dir,'running.log')

os.makedirs(log_filepath, exist_ok=True)

logging.basicConfig(
     level=logging.INFO, 
     format = '[%(levelname)s %(message)s %(module)s %(message)s]',
     handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ],
)

logger = logging.getLogger('Textsummerizerlogger')
   
