import w3lib.html
import re

class WikiscrapySpider(scrapy.Spider):
    name = 'wikiscrapy'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)']

    def parse(self, response):
        caption = response.css('caption.infobox-title::text').get()
        tables = response.css('table.infobox tr')
        data_value = {'caption' : caption}
        for table in tables:
            # label = ""
            # data = ""
            info_label_paragraph = table.css('th.infobox-label::text').get()
            info_label_link = table.css('th.infobox-label a::text').get()
            info_data = table.css('td.infobox-data').get()
            info_header_link = table.css('th.infobox-header').get()
            info_data_full = table.css('td.infobox-full-data').get()
            if info_label_link is not None:
                info_label_link = re.sub(r'\s+', ' ', info_label_link)
                label = info_label_link
            elif info_label_paragraph is not None:
                info_label_paragraph = re.sub(r'\s+',' ',info_label_paragraph)
                label = info_label_paragraph
            elif info_header_link is not None:
                # if info_header is not None:
                #     label = info_header + info_header_link
                # else:
                info_header_link = w3lib.html.remove_tags(info_header_link)
                info_header_link = re.sub(r"[\[\]]", '', info_header_link)
                info_header_link = info_header_link.replace('[', '')
                label = info_header_link
                continue
            elif info_data_full is not None:
                info_data_full = w3lib.html.remove_tags(info_data_full)
                info_data_full = re.sub(r"[\[\]]", '', info_data_full)
                info_data_full = info_data_full.replace('[', '')
                data = info_data_full
            else:
                continue
            
            if info_data is not None:
                info_data = w3lib.html.remove_tags(info_data)
                info_data = re.sub(r"[\[\d]]", '', info_data)
                info_data = info_data.replace('[', '')
                info_data = w3lib.html.replace_escape_chars(info_data)
                # info_data = info_data.replace(u"\u00A0", " ")
                info_data = re.sub(r'\s+',' ',info_data)
                data = info_data

            # if info_data is not None:
            #     data = ""
            #     for info in info_data:
            #         data_text = info.css('.infobox::text').get()
            #         data_link = info.css('a')
            #         if data_link is not None:
            #             for link in data_link:
            #                 link_text = link('a::text').get()
            #                 data = link_text + ", "
            #         else:
            #             data = data_text
            # else:
            #     data = ""
            #     for info in info_data_full:
            #          info_text = info.css('.infobox::text').get()
            #          info_link = info.css('a')
            #          for link in info_link:
            #              data = link('a::text').get() + ", "
            if data != "":
                data_value[label] = data
        i = 0
        short_desc = ""
        while i < 3:
            short = response.xpath("//p[not(@class='mw-empty-elt')]")[1].get()
            short = w3lib.html.remove_tags(short)
            short = w3lib.html.replace_escape_chars(short)
            short = re.sub(r"[\[\d]]", '', short)
            short = short.replace('[', '')
            short_desc = short_desc + " " + short
            i += 1
        data_value['short desc'] = short_desc
        yield data_value
