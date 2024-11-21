# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class RdwsPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("quotes.db")
        self.cursor = self.connection.cursor()
        sql = """
            create table if not exists quotes (
                quote text,
                author text
            )
        """
        self.cursor.execute(sql)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            "insert into quotes (quote, author) values (?, ?)",
            (item['text'], item['author'])
        )
        self.connection.commit()
        return item