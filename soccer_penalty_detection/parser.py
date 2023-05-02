import logging
import json
import os
import time
from urllib.error import URLError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from imageio import imread
from mmocr.apis import MMOCRInferencer
from tqdm import tqdm


logging.basicConfig(filename='youtube_parser.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

mmocr = MMOCRInferencer(det='DRRG', det_weights='drrg_resnet50_fpn-unet_1200e_ctw1500_20220827_105233-d5c702dd.pth', rec='svtr-small')

SCROLL_PAUSE_TIME = 2
url = 'https://www.youtube.com/c/SACAF%C3%9ATBOL/videos'
driver = webdriver.Chrome()
driver.get(url)

d_video_links = {}
list_p_element = []
prev_len_set, prev_len_list = 0, 0
i = 0

while True:
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # add elements
    list_p_element += driver.find_elements(By.XPATH, "//*[@id='dismissible']")

    for el in tqdm(list_p_element[prev_len_list:]):
        # check text
        video_title = el.text.split('\n')[-3]
        if video_title in d_video_links:
            continue

        img_src = el.find_elements(By.CSS_SELECTOR, '#thumbnail > yt-image > img')[0].get_attribute('src')
        if img_src is None:
            list_p_element = list_p_element[:list_p_element.index(el)]
            break

        if 'penalty' in video_title.lower():
            d_video_links[video_title] = {'penalty_status': 'series'}
        else:
            # parse image
            # link to image
            img_src = img_src.split('?')[0]

            try:
                preds = mmocr(imread(img_src))
                txts = ''.join(preds['predictions'][0]['rec_texts'])
            except (ValueError, FileNotFoundError, TimeoutError, URLError) as e:
                logging.warning(f"Warning: raised {type(e).__name__} on {img_src}")
                txts = ''

            if 'penalty' in txts.lower():
                d_video_links[video_title] = {'penalty_status': 'series'}
            else:
                d_video_links[video_title] = {'penalty_status': 'unknown'}

        d_video_links[video_title]['link'] = el.find_elements(By.XPATH, ".//a")[0].get_attribute('href')

    i += 1
    logging.info(f'Page {i} processed')

    # Scroll down with PAGE_DOWN
    driver.execute_script("window.scrollBy(0, 1000);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new number of elements in set and compare it with the previous number
    p_element = set(list_p_element)
    new_len_set = len(p_element)
    if new_len_set == prev_len_set:
        break
    prev_len_set = new_len_set
    prev_len_list = len(list_p_element)

driver.close()

with open('d_video_links.json', 'w') as f:
    json.dump(d_video_links, f)

n_penalty = 0
for video in d_video_links:
    if d_video_links[video]['penalty_status'] == 'series':
        n_penalty += 1

logging.info(f'Number of videos with penalties {n_penalty}')
