
# Baidu Image Crawler

This repository contains a Python script to crawl and download images from Baidu based on a search term. The script has been optimized for better readability, error handling, and maintainability.

## Features

- Search for images on Baidu
- Download images to a specified directory
- Optimized code structure
- Enhanced error handling
- Randomized User-Agent to avoid blocking

## Requirements

- Python 3.x
- Libraries: `requests`, `beautifulsoup4`, `os`, `re`, `random`

You can install the necessary libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/baidu-image-crawler.git
cd baidu-image-crawler
```

2. **Run the script**:

```bash
python baidu_image_crawler.py
```

Replace `baidu_image_crawler.py` with the name of your script file. The script will prompt you to enter a search term and a directory to save the images.

## Improvements

1. **Error Handling**:
   - Added `try-except` blocks to catch request failures and continue processing the remaining requests.
   - Used `response.raise_for_status()` to check if the request was successful, avoiding processing erroneous responses.

2. **Optimized Code Structure**:
   - Moved the directory creation operation outside the loop to avoid repeated checks and directory creation.
   - Used `os.path.join` to generate file paths, improving code readability and cross-platform compatibility.

3. **Added Logging Information**:
   - Printed log information after a successful request.
   - Printed error information when image download fails.

4. **Reduced Magic Numbers**:
   - Replaced hard-coded numbers with clear variable names, improving code readability.

5. **Adjusted Page Number Example**:
   - Changed the `page_num` in the example to 10 to prevent beginners from setting excessively large values that could result in long execution times.

## Example

Here is an example of how to use the script:

```python
import requests
import os
import re
import random

def get_images_from_baidu(keyword, page_num, save_dir):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/605.1.15',
        # Add more User-Agents as needed
    ]

    url = 'https://image.baidu.com/search/acjson?'
    n = 0

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for pn in range(0, 30 * page_num, 30):
        header = {
            'User-Agent': random.choice(user_agents)
        }
        
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
    keyword = 'white hair JK'  # Define your search keyword
    page_num = 10    # Set the number of pages to crawl
    save_dir = os.path.join('.', 'BaiduImages', keyword)   # Save path, folder + keyword name
    get_images_from_baidu(keyword, page_num, save_dir)
```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
