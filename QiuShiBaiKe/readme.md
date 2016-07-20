## 糗事百科热门笑话 

爬取糗事百科热门笑话, 字段为`author`和`content`, 示例文件是抓取前两页

想要抓取更多的页修改 MySpider.py 文件中的

``` python
start_urls = [
        "http://www.qiushibaike.com/8hr/page/%s" % i for i in range(1, 3)
    ]
``` 
`range(1, 3)` 中的 3 即可。