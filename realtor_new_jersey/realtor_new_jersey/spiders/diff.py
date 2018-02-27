# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import time
import random

class DiffSpider(scrapy.Spider):
    name = 'diff'
    allowed_domains = ['realtor.com', 'googleusercontent.com']
    start_urls = ['http://webcache.googleusercontent.com/search?q=cache:https://realtor.com/local/New-Jersey']

    def parse(self, response):
        region_boxes = response.xpath("//div[@id='top-cities']/table/tbody/tr")
        region_dict = {}

        for region in region_boxes:
            region_name = region.xpath(".//td[@class='col-area']/a/text()").extract_first()
            region_url = region.xpath(".//td[@class='text-center']/a/@href").extract_first()
            region_full_url = "http://webcache.googleusercontent.com/search?q=cache:" + response.urljoin(region_url)
            region_dict[region_name] = region_full_url

        for reg_name, reg_url in region_dict.items():
            #time.sleep(random.randint(180,240))
            print("region: {}, url: {}".format(reg_name, reg_url))
            yield Request(reg_url, callback=self.parse_region, meta={'r_name':reg_name})
            #time.sleep(3)



    def parse_region(self, response):

        region_name2 = response.meta['r_name']

        try:

            if int(response.xpath('//span[@class="search-result-count srp-list-header-count font-bold"]/text()').extract_first().strip()[0]) > 0:

                house_box = response.xpath('//*[@data-omtag="srp-listMap:result:link"]')

                for house in house_box:

                    house_price = house.xpath(".//span[@itemprop='price']/text()").extract_first()
                    house_street = house.xpath('.//*[@class="listing-street-address"]/text()').extract_first()
                    house_city = house.xpath('.//*[@class="listing-city"]/text()').extract_first()
                    house_district = house.xpath('.//*[@class="listing-region"]/text()').extract_first()
                    house_postal = house.xpath('.//*[@class="listing-postal"]/text()').extract_first()

                    house_beds = house.xpath('.//*[@data-label="property-meta-beds"]/span/text()').extract_first()
                    house_baths = house.xpath('.//*[@data-label="property-meta-baths"]/span/text()').extract_first()
                    house_area_sqft = house.xpath('.//*[@data-label="property-meta-sqft"]/span/text()').extract_first()
                    house_garage_car_space = house.xpath('.//*[@data-label="property-meta-garage"]/span/text()').extract_first()

                    house_broker = house.xpath('.//*[@data-label="property-broker"]/text()').extract_first()

                    yield {
                        'region': region_name2,
                        'price': house_price,
                        'beds': house_beds,
                        'baths': house_baths,
                        'area_sqft': house_area_sqft,
                        'car_space_garage': house_garage_car_space,
                        'street': house_street,
                        'city': house_city,
                        'district': house_district,
                        'postal': house_postal,
                        'broker': house_broker
                    }

                next_sale_url = response.xpath('//a[@class="next"]/@href').extract_first()
                if next_sale_url:
                    next_sale_full_url = "http://webcache.googleusercontent.com/search?q=cache:" + response.urljoin(next_sale_url)
                    #time.sleep(random.randint(4,8))
                    yield Request(next_sale_full_url, callback=self.parse_region, meta={'r_name':region_name2})
                else:
                    pass


            else:
                pass

        except:
            print("no of home not specified for: {}".format(region_name2))
