import scrapy


class CveSpider(scrapy.Spider):
    name = "cve"
    allowed_domains = ["cve.mitre.org"]
    start_urls = ["https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html"]

    def parse(self, response):
        tables = response.xpath("//table")
        for table_instance in tables:
            if len(table_instance.xpath("//tr")) > 100:
                table = table_instance

        expolits = []
        print("*/-*/*-/*-/-*/*-/*/*-/-*/*-/*-/*-/-*/*-/-*/-*/*-/*-/-*-----------------/*/-*/-*/-*/-*/-*/-*/-*/-*/*")
        for table_row in table.xpath("//tr"):
            exploit_data = {}
            row_data = table_row.xpath("td")
            id = row_data[0].xpath("text()").extract()
            names = []
            for data_item in row_data[1:]:
                tag_elements = data_item.xpath("a//text()")
                if len(tag_elements)>0:
                    for element in tag_elements:
                        names.append(element.extract())
            if len(names) > 0 and len(id) > 0:
                if not names[0].startswith("CVE"):
                    break
                exploit_data["id"] = id[0]
                exploit_data["names"] = names
                expolits.append(exploit_data)
        
        for exploit in expolits[:10]:
            print(exploit)
            
        # Example output
        # {'id': 'EXPLOIT-DB:10102', 'names': ['CVE-2009-4186']}
        # {'id': 'EXPLOIT-DB:1013', 'names': ['CVE-2005-1598']}
        # {'id': 'EXPLOIT-DB:10168', 'names': ['CVE-2009-4767']}
        # {'id': 'EXPLOIT-DB:10180', 'names': ['CVE-2009-4091', 'CVE-2009-4092', 'CVE-2009-4093']}
        # {'id': 'EXPLOIT-DB:10183', 'names': ['CVE-2011-4906']}
        # {'id': 'EXPLOIT-DB:10201', 'names': ['CVE-2009-4781']}
        # {'id': 'EXPLOIT-DB:10216', 'names': ['CVE-2009-4223']}
        # {'id': 'EXPLOIT-DB:10217', 'names': ['CVE-2009-4779']}
        # {'id': 'EXPLOIT-DB:10218', 'names': ['CVE-2009-4082']}
        # {'id': 'EXPLOIT-DB:10220', 'names': ['CVE-2009-4220']}
