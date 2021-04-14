# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings
import os
import scrapy
from urllib.parse import urlparse
from scrapy.exceptions import DropItem


class SkindlPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        # print("Title: %s" % adapter['title'])
        for i,image_url in enumerate(adapter['preview_url']):
            filename = image_url.split("/")[-1].lower()
            ext = filename.split(".")[-1]
            adapter["ext"] = ext
            # print("Title: %s" % filename)
            yield scrapy.Request(image_url, meta={'filename' : filename, 'type' : 'preview'})
        for i,image_url in enumerate(adapter['skin_url']):
            filename = image_url.split("/")[-2].lower()
            # print("Title: %s" % filename)
            # print(image_url)
            yield scrapy.Request(image_url, meta={'filename' : filename, 'type' : 'skin', 'ext' : ext})

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
 
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        # print("Response: %s" % request.url)
        if((request.meta['type'].casefold()).__eq__("preview".casefold())):
            # return 'preview/' + os.path.basename(urlparse(request.url).path)
            return 'preview/' + request.meta['filename']
        if((request.meta['type'].casefold()).__eq__("skin".casefold())):
            return 'skin/' + request.meta['filename'] + "." + request.meta['ext']
        