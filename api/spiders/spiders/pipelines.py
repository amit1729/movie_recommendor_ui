# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from time import time
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from django.utils import timezone
from datetime import timedelta
from .spiders.googleverifier import GoogleVerifier
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
import asyncio

from ...models import PerliminaryData, MovieDatabase

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

class IMDbPipeline:
    def __init__(self,gl):
        print("Pipeline Initiated....")
        self.ids_seen = set()
        self.googleLikes = gl
        self.gv = GoogleVerifier()

    def process_item(self, item, spider):
        print("processing Item....")
        adapter = ItemAdapter(item)
        print(adapter['movie_id'])
        if adapter['movie_id'] in self.ids_seen:
            DropItem(f"Dupticate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['movie_id'])
            query = MovieDatabase.objects.filter(movie_id = adapter['movie_id'])
            print(query)
            print(len(query))
            if(len(query)):
                refreshcheck = query[0].created_at + timedelta(days=3)
                now = timezone.now()
                
                if(now>refreshcheck):
                    print("Refreshing movie_glikes.....")
                    glikes = self.gv.run(adapter["name"],adapter["release_date"])
                    print(glikes)
                    query[0].created_at = now
                    query[0].movie_details["gLikes"] = glikes
                    if(glikes>self.googleLikes or glikes==0):
                        query[0].active = True
                        query[0].save()
                    else:
                        query[0].save()
                    #update google rating and return movie_details to frontend if it satisfies the glikes criteria
                else:
                    glikes = query[0].movie_details["gLikes"]
                    if(glikes>self.googleLikes or glikes==0):
                        
                        query[0].active = True
                        query[0].save()
                    #return movie_details to frontend if it satisfies the glikes criteria
                    
            else:
                print("Creating new movie entry....")
                details = {}
                details["movie_id"] = adapter["movie_id"]
                details["name"] = adapter["name"]
                details["imdbLikes"] = adapter["imdbLikes"]
                details["releaseDate"] = adapter["release_date"]
                glikes =self.gv.run(adapter["name"],adapter["release_date"])
                print(glikes)
                details["gLikes"] = glikes
                if(glikes>self.googleLikes or glikes==0):
                    movie = MovieDatabase(movie_id=adapter["movie_id"],movie_details=details,active=True)
                    movie.save()
                else:
                    movie = MovieDatabase(movie_id=adapter["movie_id"],movie_details=details)

    def __del__(self):
        print("Destroyed....")