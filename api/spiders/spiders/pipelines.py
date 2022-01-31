# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from ...models import PerliminaryData

class PermilinaryDataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        entries = PerliminaryData.objects.all()
        if(len(entries)==0):
            entry = PerliminaryData(data=adapter["data"])
            entry.save()
        else:
            entries[0].data = adapter["data"]
            entries[0].save()
