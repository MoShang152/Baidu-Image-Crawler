
# 百度图片爬虫

该仓库包含一个用于根据搜索词从百度抓取和下载图片的Python脚本。该脚本经过优化，以提高可读性、错误处理和可维护性。

## 特性

- 在百度上搜索图片
- 将图片下载到指定目录
- 优化代码结构
- 增强错误处理
- 随机化 User-Agent 以避免被屏蔽

## 要求

- Python 3.x
- 库：`requests`，`beautifulsoup4`，`os`，`re`，`random`

您可以使用 pip 安装必要的库：

```bash
pip install requests beautifulsoup4
```

## 用法

1. **克隆仓库**：

```bash
git clone https://github.com/yourusername/baidu-image-crawler.git
cd baidu-image-crawler
```

2. **运行脚本**：

```bash
python baidu_image_crawler.py
```

将 `baidu_image_crawler.py` 替换为您的脚本文件名。脚本将提示您输入搜索词和保存图片的目录。

## 改进

1. **错误处理**：
   - 添加了 `try-except` 块来捕获请求失败并继续处理剩余请求。
   - 使用 `response.raise_for_status()` 检查请求是否成功，避免处理错误响应。

2. **优化代码结构**：
   - 将目录创建操作移到循环外部，以避免重复检查和创建目录。
   - 使用 `os.path.join` 生成文件路径，提高代码可读性和跨平台兼容性。

3. **添加日志信息**：
   - 在请求成功后打印日志信息。
   - 在下载图片失败时打印错误信息。

4. **减少魔法数**：
   - 用明确的变量名称代替硬编码的数字，提高代码可读性。

5. **调整页数示例**：
   - 将示例中的 `page_num` 更改为 10，以防止初学者设置过大数值导致程序运行时间过长。

## 示例

以下是如何使用该脚本的示例：

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
        # 根据需要添加更多 User-Agents
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
            'cg': '',  # 这个参数未公开，但它是必要的
            'pn': pn,  # 显示：30-60-90
            'rn': '30',  # 每页显示30个结果
            'gsm': '1e',
            '1618827096642': ''
        }

        try:
            response = requests.get(url, headers=header, params=param, proxies=None)
            response.raise_for_status()  # 检查请求是否成功
        except requests.RequestException as e:
            print(f"请求失败：{e}")
            continue

        print('请求成功。')
        response.encoding = 'utf-8'
        
        # 使用正则表达式提取图片链接
        html = response.text
        image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)

        for image_url in image_url_list:
            try:
                image_data = requests.get(image_url, headers=header).content
                with open(os.path.join(save_dir, f'{n:06d}.jpg'), 'wb') as fp:
                    fp.write(image_data)
                n += 1
            except requests.RequestException as e:
                print(f"下载图片失败 {image_url}：{e}")
                continue

if __name__ == "__main__":
    keyword = '白毛JK'  # 定义你的搜索关键词
    page_num = 10    # 设置要抓取的页数
    save_dir = os.path.join('.', '百度图片', keyword)   # 保存路径，文件夹 + 关键词名称
    get_images_from_baidu(keyword, page_num, save_dir)
```

## 贡献

如果您想为本项目做贡献，请 fork 该仓库并提交 pull request。

## 许可证

本项目使用 MIT 许可证。有关详细信息，请参阅 `LICENSE` 文件。
