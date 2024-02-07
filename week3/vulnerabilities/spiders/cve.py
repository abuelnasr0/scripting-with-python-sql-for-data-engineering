import scrapy
import os
import csv
import json

HTML_FILE = "source-EXPLOIT-DB.html"
URL_PATH = os.path.join(os.getcwd(),HTML_FILE)

class CveSpider(scrapy.Spider):
    name = "cve"
    allowed_domains = ["cve.mitre.org"]
    # start_urls = ["https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html"]
    start_urls = [f"file://{URL_PATH}"]

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
                exploit_data["exploit_id"] = id[0][11:]
                exploit_data["cve_id"] = names
                expolits.append(exploit_data)
        
        for exploit in expolits[:10]:
            print(exploit)

        def save_as_json(exploits, file_name):
            with open(file_name, "w") as f:
                json.dump(exploits, f, indent=4)

        def save_as_csv(exploits, file_name):

            with open(file_name, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["exploit_id", "cve_id"])
                for exploit in exploits:
                    writer.writerow(exploit.values())

        save_as_csv(expolits, "exploits.csv")
        save_as_json(expolits, "exploits.json")
        # Example output
        # {'id': ':10102', 'names': ['CVE-2009-4186']}
        # {'id': ':1013', 'names': ['CVE-2005-1598']}
        # {'id': ':10168', 'names': ['CVE-2009-4767']}
        # {'id': ':10180', 'names': ['CVE-2009-4091', 'CVE-2009-4092', 'CVE-2009-4093']}
        # {'id': ':10183', 'names': ['CVE-2011-4906']}
        # {'id': ':10201', 'names': ['CVE-2009-4781']}
        # {'id': ':10216', 'names': ['CVE-2009-4223']}
        # {'id': ':10217', 'names': ['CVE-2009-4779']}
        # {'id': ':10218', 'names': ['CVE-2009-4082']}
