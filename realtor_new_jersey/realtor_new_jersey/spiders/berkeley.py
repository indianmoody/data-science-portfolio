# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from time import sleep
import random

class BerkeleySpider(scrapy.Spider):
    name = 'berkeley'
    allowed_domains = ['realtor.com']
    #start_urls = ['https://www.realtor.com/realestateandhomes-search/Diamond-Beach_NJ?pgsz=50']

    def parse(self, response):

        if int(self.delay_counter) > 0:
            sleep(random.randint(200,300))

        try:

            if int(response.xpath('//span[@class="search-result-count srp-list-header-count font-bold"]/text()').extract_first().strip()[0]) > 0:

                house_box = response.xpath('//*[@data-omtag="srp-listMap:result:link"]')

                for house in house_box:
                    # house details
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
                    next_sale_full_url = response.urljoin(next_sale_url) + "?pgsz=50"
                    sleep(random.randint(15,20))
                    print(next_sale_full_url)
                    yield Request(next_sale_full_url)
                else:
                    sleep(random.randint(3,5))


            else:
                print("this region doesn't have any listings")
                sleep(10)

        except:
            print("except: this region doesn't have any listings")

        self.delay_counter = 0
