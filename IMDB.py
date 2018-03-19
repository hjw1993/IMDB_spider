# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
import re
from Article.items import MovieItem,ArticleItem
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'IMDB'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    def parse(self, response):
        movies_nodes= response.css('.lister-list tr')
        for node in movies_nodes:

            avatar_url=[]
            movie_avatar= node.css('.posterColumn img::attr(src)').extract_first("")
            movie_url= node.css('.titleColumn a::attr(href)').extract_first("")
            title= node.css('.titleColumn a::text').extract_first("")
            year = node.css('.titleColumn span::text').extract_first("")
            if year:
                res = (re.match(".*(\d{4}).*",year))
                if res:
                    year=int(res.group(1))
            rating = node.css(".imdbRating strong::text").extract_first("")


            print(parse.urljoin(response.url,movie_url))
            yield  Request(url=(parse.urljoin(response.url,movie_url)),
                    meta={"title":title,"year":year,"rating":rating,"movie_avatar":movie_avatar},
                    callback=self.parse_detail)


    def parse_detail(self,response):
        Movie_Item=MovieItem()
        summury= response.css(".plot_summary ")
        desc= summury.css('.summary_text::text').extract()[0].strip().split("\n")
        director= summury.css('span[itemprop="director"] span::text').extract()
        cast = summury.css('span[itemprop="actors"] a span::text').extract()
        video_url="http://www.imdb.com"+response.css('.video_slate a::attr(href)').extract_first("")
        count=1
        Movie_Item["title"]=response.meta["title"]
        Movie_Item["year"] = response.meta.get("year", "")
        Movie_Item["rating"] = response.meta.get("rating", "")
        avatar_url=[]
        video_urls=[]
        avatar_url.append(response.meta.get("movie_avatar", ""))
        video_urls.append(video_url)
        Movie_Item["movie_avatar"] = avatar_url
        Movie_Item["desc"] = ",".join(desc)
        Movie_Item["director"] = "/".join(director)
        Movie_Item["cast"] = "/".join(cast)
        Movie_Item["video_url"] = video_url
        item_loader=ItemLoader(item = MovieItem(),response=response)
        return Movie_Item

