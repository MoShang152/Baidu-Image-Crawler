# -*- coding: utf-8 -*-
# Not usable after connecting to VPN... It greatly affects my workflow, needs to be resolved
"""
Created on Wed Mar 29 10:17:50 2023
Original author: MatpyMaster
Modified by: Moshang
"""
import requests
import os
import re

def get_images_from_baidu(keyword, page_num, save_dir):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/126.0.0.0 Safari/537.36'}
    # Request URL
    url = 'https://image.baidu.com/search/acjson?'
    n = 0

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for pn in range(0, 30 * page_num, 30):
        # Request parameters
        param = {
            'tn': 'resultjson_com',
            'logid': '7603311155072595725',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': -1,
            'z': '',
            'ic': '',
            'hd': '',
            'latest': '',
            'copyright': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0,
            'istype': 2,
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'force': '',
            'cg': '',  # This parameter is not public, but it is necessary
            'pn': pn,  # Display: 30-60-90
            'rn': '30',  # Display 30 results per page
            'gsm': '1e',
            '1618827096642': ''
        }

        try:
            response = requests.get(url, headers=header, params=param, proxies=None)
            response.raise_for_status()  # Check if the request was successful
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            continue

        print('Request success.')
        response.encoding = 'utf-8'
        
        # Extract image links using regex
        html = response.text
        image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)

        for image_url in image_url_list:
            try:
                image_data = requests.get(image_url, headers=header).content
                with open(os.path.join(save_dir, f'{n:06d}.jpg'), 'wb') as fp:
                    fp.write(image_data)
                n += 1
            except requests.RequestException as e:
                print(f"Failed to download image {image_url}: {e}")
                continue

if __name__ == "__main__":
    keyword = '白毛JK'  # Define your search keyword
    page_num = 10    # Set the number of pages to crawl
    save_dir = os.path.join('.', 'BaiduImages', keyword)   # Save path, folder + keyword name
    get_images_from_baidu(keyword, page_num, save_dir)
