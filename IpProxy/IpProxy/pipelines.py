# -*- coding: utf-8 -*-

class IpproxyPipeline(object):

    def process_item(self, item, spider):
        print '---------write------------------'
        f=file("ip.txt","a+")
        content=item['IP'] + ':' +item['port'] +'\n'
        f.write(content)
        f.close()
        return item
