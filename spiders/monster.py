# -*- coding: utf-8 -*-
import scrapy
import json
from pprint import pprint
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from estyaauto.items import EstyaautoItem



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


class MonsterSpiderSpider(scrapy.Spider):
    name = 'monster'
    allowed_domains = ['monster.fr']
    start_urls = ['https://www.monster.fr/emploi/recherche/pagination/'
                '?q=Informatique&isDynamicPage=true&isMKPagination=true&page={}'.format(i + 1) for i in range(50) ]

    def parse(self, response):
        results = json.loads(response.body.decode('utf-8'))
        for result in results:
            try:
                job_id = result['MusangKingId']
                next_url = ('https://offre-demploi.monster.fr/v2/job/pure-json-view?jobid={}').format(job_id)
                yield response.follow(next_url, callback = self.parse_detail)
            except:
                continue

    def parse_detail(self,response):
        result = json.loads(response.body.decode('utf-8'))
        item =EstyaautoItem()
        item["jobLink"] = "https://offre-demploi.monster.fr/v2/job/pure-json-view?jobid="+result['jobId']
        item["statut"] = "Monster"
        item["jobId"] = result['jobId']
        item["contactMail"] = "null"
        item["jobDuration"] = "null"
        item['status']='enabled'

        item["jobTitle"] = result['companyInfo']['companyHeader']
        item["jobLocation"] = result['companyInfo']['jobLocation']
        try:
          item['companyName'] = result['companyInfo']['name']
        except:
          item['companyName'] = "null"
        try:
          item['contactPhone'] = result['contacts']['phoneNumber']
        except:
          item['contactPhone'] = "null"


        item['jobDescription'] = text_from_html(result["jobDescription"])
        item['postedDate'] =  result["postedDate"]
        try:
            p = result["positionType"]
            item['jobPositionType'] = string.join(p)
        except:
            item['jobPositionType'] = 'null'
        try:
            item['jobWage'] = result["salary"]["rangeText"]
        except:
            item['jobWage'] = 'null'
        try:
            item['contactName'] =  result["contacts"]["name"]
        except:
            item['contactName'] = 'null'

        #try:
        #    detail["expertise_domain"] = result['companyInfo']["companySizeName"]
        #except:
        #    detail["expertise_domain"] = 'N/A'


        try:
            r = result['jobIndustry']
            item["jobIndustry"] = string.join(r)
        except:
            item["jobIndustry"] = 'null'

        return item
