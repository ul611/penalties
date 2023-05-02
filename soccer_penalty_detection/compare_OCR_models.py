import logging
import time

from mmocr.apis import MMOCRInferencer

# Set up logging
logging.basicConfig(filename='ocr.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Check time spent to OCR and its quality by every model
for model in [
              #'DB_r18',
              #'DB_r50',
              'DRRG', # +
              #'FCE_IC15',
              #'FCE_CTW_DCNv2',
              'MaskRCNN_CTW', # + but slow
              #'MaskRCNN_IC15',
              'MaskRCNN_IC17', # + but slow
              #'PANet_CTW',
              #'PANet_IC15',
              'PS_CTW', # +-
              #'PS_IC15',
              #'TextSnake'
                ]:
    logging.info('Starting OCR for {} model'.format(model))
    ts = time.time()
    mmocr = MMOCRInferencer(model, recog_backend='mmocr')
    mmocr_result = mmocr.inference('../football_1.webp')
    # # from mmocr.utils.ocr import MMOCR
    # mmocr.readtext('../football_1.webp', print_result=True)#, output=f'../outputs/check_models/f1_{model}.jpg')
    logging.info('Finished OCR for {} model in {} seconds'.format(model, round(time.time() - ts, 3)))
    logging.info('Result for {} model: {}'.format(model, mmocr_result))

# I choose 'DRRG' model, because it finds all the words and it's pretty fast
