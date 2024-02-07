import scrapy
import os
import csv
import json
import sqlite3

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

        def save_as_sqlite(exploits, data_base_name):
            connection = sqlite3.connect(data_base_name)
            cursor = connection.cursor()

            #drop table if exists 
            
            create_CMD = "DROP TABLE IF EXISTS exploits;"
            cursor.execute(create_CMD)
            connection.commit()


            # Create table
            create_CMD = "CREATE TABLE IF NOT EXISTS exploits(exploit_id TEXT, cve_id TEXT);"
            cursor.execute(create_CMD)
            connection.commit()

            #insert the data
            insert_CMD = "INSERT INTO exploits VALUES (?, ?);"
            for exploit in exploits:
                exploit_id = exploit["exploit_id"]
                cve_id = exploit["cve_id"][0]
                cursor.execute(insert_CMD, [exploit_id, cve_id])
            connection.commit()

            #check insertion 
            select_CMD = "SELECT * FROM exploits LIMIT 10 "
            for i in cursor.execute(select_CMD):
                print(i)



        save_as_csv(expolits, "exploits.csv")
        save_as_json(expolits, "exploits.json")
        save_as_sqlite(expolits, "exploite.db")
        # Example output
    # {'exploit_id': '10102', 'cve_id': ['CVE-2009-4186']}
    # {'exploit_id': '1013', 'cve_id': ['CVE-2005-1598']}
    # {'exploit_id': '10168', 'cve_id': ['CVE-2009-4767']} 
    # {'exploit_id': '10180', 'cve_id': ['CVE-2009-4091', 'CVE-2009-4092', 'CVE-2009-4093']}
    # {'exploit_id': '10183', 'cve_id': ['CVE-2011-4906']}
    # {'exploit_id': '10201', 'cve_id': ['CVE-2009-4781']}
    # {'exploit_id': '10216', 'cve_id': ['CVE-2009-4223']}
    # {'exploit_id': '10217', 'cve_id': ['CVE-2009-4779']}
    # {'exploit_id': '10218', 'cve_id': ['CVE-2009-4082']}
    # {'exploit_id': '10220', 'cve_id': ['CVE-2009-4220']}
