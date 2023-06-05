import requests
import time
# 定义要检测的网页 URL
url = 'https://dazi.91xjr.com/typing'

# 发起 GET 请求获取网页内容
response = requests.get(url)
response.encoding='gbk'
content = response.text

# 将网页内容保存到文件，以便后续比较
file_path = 'original_content.txt'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

# 后续操作...

# 重新获取网页内容
response = requests.get(url)
new_content = response.text

# 将原始内容与新内容进行比较
with open(file_path, 'r', encoding = 'gb18030', errors = 'ignore') as file:
    original_content = file.read()

while original_content ==new_content:
    # 重新获取网页内容
    time.sleep(6)
    response = requests.get(url)
    new_content = response.text

    # 将原始内容与新内容进行比较
    with open(file_path, 'r', encoding = 'gb18030', errors = 'ignore') as file:
        original_content = file.read()
    
#if original_content == new_content:
#    print("网页内容未发生变化")
#else:
print("网页内容发生变化")
