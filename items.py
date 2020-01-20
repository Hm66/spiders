# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EstyaautoItem(scrapy.Item):
    jobId = scrapy.Field()
    jobTitle = scrapy.Field()
    jobDescription = scrapy.Field()
    jobDuration = scrapy.Field()
    jobIndustry = scrapy.Field()
    jobPositionType = scrapy.Field()
    jobLocation = scrapy.Field()
    jobWage = scrapy.Field()
    postedDate = scrapy.Field()
    jobLink = scrapy.Field()
    notes = scrapy.Field()
    companyName = scrapy.Field()
    contactName = scrapy.Field()
    contactMail = scrapy.Field()
    contactPhone = scrapy.Field()
    statut = scrapy.Field()
    status = scrapy.Field()
    pass
