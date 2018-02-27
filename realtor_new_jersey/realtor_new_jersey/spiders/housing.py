# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import time

class HousingSpider(scrapy.Spider):
    name = 'housing'
    # allowed_domains = ['realtor.com/local/New%20Jersey']
    start_urls = ['https://realtor.com/local/New-Jersey/']


    def parse(self, response):

        region_boxes = response.xpath("//div[@id='top-cities']/table/tbody/tr/td[@class='col-area']")
        region_dict = {}

        for region in region_boxes:
            region_name = region.xpath(".//a/text()").extract_first()
            region_url = region.xpath(".//a/@href").extract_first()
            region_full_url = response.urljoin(region_url)
            region_dict[region_name] = region_full_url

            #curr_request = Request(region_full_url, callback=self.parse_region)
            #curr_request.meta['curr_region'] = region_name

            #yield curr_request
            yield Request(region_full_url, callback=self.parse_region)
            time.sleep(10)

        #yield region_dict


    def parse_region(self, response):
        # to get href of house for sale for region

        if int(response.xpath("//a[@data-omtag='local:under-hero:for-sale']/span/text()").extract_first()[0]) > 0:
            # if there are any houses in this region
            house_sale_url = response.xpath("//a[@data-omtag='local:under-hero:for-sale']/@href").extract_first()
            house_sale_full_url = response.urljoin(house_sale_url)

            house_sale_full_url_50 = house_sale_full_url + "?pgsz=50"

            #curr_request = Request(house_sale_full_url, callback=self.parse_house_sale)
            #curr_request.meta['curr_region'] = response.meta['curr_region']
            #yield curr_request
            yield Request(house_sale_full_url_50, callback=self.parse_house_sale)

        else:
            pass

        time.sleep(1)



    def parse_house_sale(self, response):

        #region_name = response.meta['curr_region']

        # to get block for each house details
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
                #'region': region_name,
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
        next_sale_full_url = response.urljoin(next_sale_url)
        #yield {'next_url': next_sale_full_url}


        #curr_request = Request(next_sale_full_url)
        #curr_request.meta['curr_region'] = region_name
        #yield curr_request
        yield Request(next_sale_full_url)
        time.sleep(5)
