# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests

class EstyaautoPipeline(object):
    def process_item(self, item, spider):
        r = requests.post('http://localhost:8080/api/offresAuto/create',json={
                            'jobId':item['jobId'],
                            'companyName' : item['companyName'],
                            'contactMail':item['contactMail'],
                            'contactName' : item['contactName'],
                            'contactPhone':item['contactPhone'],
                            'jobDescription':item['jobDescription'],
                            'jobDuration':item['jobDuration'],
                            'jobIndustry':item['jobIndustry'],
                            'jobLink':item['jobLink'],
                            'jobLocationString':item['jobLocation'],
                            'jobPositionType': 'dev',
                            'jobTitle':item['jobTitle'],
                            'jobWage':item['jobWage'],
                            'jobLocation': item['jobLocation'],
                            'postedDate':item['postedDate'],
                            'statut':item['statut'],
                            'status':item['status'],
                            'notes' :item['notes'],
                            }
                            )
        return item
        #if r.status_code == 200:
        #    return item
        #else:
        #    raise DropItem("Failed to post item with title %s." % item['jobTitle'])
