from src.TextsummerizeProject.pipeline.Data_injestion import dataingestionpipeline
from src.TextsummerizeProject.logging import logger

stage = 'Data_injestion'

try:
    logger.info('>>>>>>> stage {stage1} inited\n'.format(stage1=stage))
    datainjestion = dataingestionpipeline()
    datainjestion.main()
    logger.info('>>>>>>> stage {stage1} completed\n'.format(stage1=stage))
except Exception as e:
    logger.exception(e)
    raise e


stage = 'Data_Validation'

try:
    logger.info('>>>>>>> stage {stage2} inited\n'.format(stage2=stage))
    datainjestion = dataingestionpipeline()
    datainjestion.main()
    logger.info('>>>>>>> stage {stage2} completed\n'.format(stage2=stage))
except Exception as e:
    logger.exception(e)
    raise e