## 使用方法

1. 在mySpider中找到`email`和`password`字段修改成自己的用户名和密码

2. 在项目目录下输入`scrapy crawl users -a url=https://www.zhihu.com/people/<user> -o data.json` 待程序运行完毕后即可在当前目录下的data.json中找到抓取的数据。

3. 主要参考代码 [scrapy-zhihu-users](https://github.com/ansenhuang/scrapy-zhihu-users)。 (侵立删)

## TODO:

- [ ] 处理知乎反爬

![users](http://ww4.sinaimg.cn/large/5e515a93jw1f63xqh6w4hj21kw0omaq0.jpg)
