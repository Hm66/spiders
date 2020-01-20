# -*- coding: utf-8 -*-
import scrapy
import requests
import urllib
from bs4 import BeautifulSoup
from bs4.element import Comment
from estyaauto.items import EstyaautoItem
import uuid
from scrapy.selector import Selector
from scrapy.http import FormRequest
import re

class FreelanceSpider(scrapy.Spider):
    name = 'freelance'
    allowed_domains = ['freelance-info.fr',]
    start_urls = ['https://www.freelance-info.fr/login-page.php',]


    def parse(self,response):
        return scrapy.FormRequest.from_response(response,
        formdata={
            'username': 'a.******@*****.com',
            'password': '**************  ',
            },
            callback=self.after_login)

    def after_login(self, response):
        offrespage='https://www.freelance-info.fr/missions.php'
        request= scrapy.Request(offrespage)
        yield request
        sel = Selector(response)
        results = sel.xpath("//*[contains(@id, 'offre_')]")
        for result in results :
            item = EstyaautoItem()
            item['postedDate'] = result.xpath('.//span[@class = "textgrisfonce9"]/text()').extract_first()
            item['statut'] = 'Freelance-info'
            item['jobDuration'] =result.xpath ('.//div[@class="rlig_det"]/span[1]/text()').extract_first()
            item['jobWage'] =result.xpath ('.//div[@class="rlig_det"]/span[2]/text()').extract_first()
            item['jobLocation'] = result.xpath ('.//span[@class = "textvert9"]/text()').extract_first()
            item['jobIndustry'] = 'Informatique'
            idsource = result.xpath('.//*[@class = "rtitre"]/@href').extract_first()
            item ['jobId'] = ''.join(filter(str.isdigit,idsource))
            offrepage = 'https://www.freelance-info.fr/'+ result.xpath('.//a[@class = "rtitre"]/@href').extract_first()
            item['jobPositionType'] = 'Developpeur'
            item['jobLink'] =offrepage
            item['status']='enabled'

            request= scrapy.Request(offrepage, callback=self.get_description1)
            request.meta['item'] = item
            yield request

        nextpageurl = response.xpath('//div[@class="pages"]//a[text()="Suivante"]/@href')
        if nextpageurl:
             path = nextpageurl.extract_first()
             nextpage = response.urljoin(path)
             print("Found url: {}".format(nextpage))
             yield scrapy.Request(nextpage, callback=self.after_login)

    def get_description1(self, response):
        item = response.meta['item']
        item['jobTitle'] = response.xpath('//div[@id="divcontmain-pad"]/div[2]/h1/text()').extract_first()
        trans_table = {ord(c): None for c in u'\r\n\t' }
        item['jobDescription'] = ''.join(s.strip().translate(trans_table) for s in response.xpath('.//div[@class = "textnoir9"]/text()').extract())
        contactfull =''.join (response.xpath ('.//*[@id="zone-postule-bis"]/div/text()').extract())
        contact=''.join(s.strip().translate(trans_table) for s in response.xpath ('.//*[@id="zone-postule-bis"]/div/text()').extract())
        entrepriseFromLink = response.xpath('//*[@id="divcontmain-pad"]/div[2]/div[2]/div[2]/a/img/@alt').extract_first()
        email = re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',contactfull)
        phone =  re.findall('([\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9])', contactfull)
        entreprise = response.xpath('//*[@id="divcontmain-pad"]/div[2]/div[2]/div[2]/img/@alt').extract_first()
        entrepriseWithNoP = response.xpath('//*[@id="divcontmain-pad"]/div[2]/div[2]/div[2]/div/text()').extract_first()
        item['notes'] = contact
        if contactfull:
            item['contactName'] =''.join(email[0])
            item ['contactMail'] = ' '.join(email)
            if entreprise:
                item['companyName'] = entreprise
            elif entrepriseFromLink :
                item['companyName'] = entrepriseFromLink
            elif entrepriseWithNoP:
                item['companyName'] =entrepriseWithNoP
            else :
                item['companyName'] ="Inconnue"

        elif entreprise and not contactfull:
            item['companyName'] = entreprise
            item['contactName'] =entreprise
            item ['contactMail'] = entreprise
        elif entrepriseFromLink and not contactfull:
            item['companyName'] = entrepriseFromLink
            item['contactName'] = entrepriseFromLink
            item ['contactMail'] = entrepriseFromLink
        elif entrepriseWithNoP and not contactfull:
            item['companyName'] = entrepriseWithNoP
            item ['contactMail'] = entrepriseWithNoP
            item ['contactName'] = entrepriseWithNoP
        else:
            item['companyName'] = "Inconnue"
            item ['contactMail'] = "Introuvable pour cette offre"
            item ['contactName'] = "Introuvable pour cette offre"

        if phone :
            item['contactPhone'] = ''.join(phone)
        else :
            item['contactPhone'] = 'Introuvable pour cette offre'

        yield item


    #     contactpage =response.xpath('//*[@id="divcontmain-pad"]/div[2]/div[2]/div[2]/a/@href').extract_first()
    #     xt=response.xpath('//*[@id="divcontmain-pad"]/div[2]/div[2]/div[2]/a/@href').extract_first()
    #     if xt:
    #         request = scrapy.Request(xt, callback=self.get_contact2)
    #         request.meta['item'] = item
    #         yield request
    #     else:
    #         item['contactPhone'] = 'Introuvable pour cette offre'
    #         yield item
    #
    #
    # def get_contact2(self, response):
    #     item = response.meta['item']
    #     phone = response.xpath('//*[@id="divcontmain-pad"]/div[2]/div/div[2]/div/text()[2]').extract_first()
    #     if phone:
    #         item['contactPhone'] = phone
    #     else:
    #         item['contactPhone'] = 'Introuvable pour cette offre'
    #     yield item
