#!/usr/bin/env python

import csv
import sys

if __name__ == "__main__":
    input_dir = sys.argv[1] #'input/test.csv'
    output_dir = sys.argv[2] #'output/report.csv'
    items = []
    file =  open(input_dir, encoding="utf8")
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        items.append(row)
    file.close()

    class company:
        def __init__(self, name):
            self.name = name
            self.complaints = 0
        def add_complaint(self):
            self.complaints = self.complaints + 1

    class year:
        def __init__(self, year):
            self.year = year
            self.companies = []
            self.hash_companies = {}
            
        def is_company_present(self, company_obj):
            return company_obj.name in self.hash_companies.keys()
            
        def add_company(self, company_obj):
            if not self.is_company_present(company_obj):
                self.companies.append(company_obj)
                self.hash_companies[company_obj.name] = company_obj 

        def list_companies(self):
            for i in self.companies:
                print(i.name)

    class product:
        def __init__(self, name):
            self.product_name = name
            self.years = []
            self.hash_years = {}
            
        def add_year(self, new_year_obj):
            if not self.is_year_present(new_year_obj):
                self.years.append(new_year_obj)
                self.hash_years[new_year_obj.year] = new_year_obj
        
        def is_year_present(self, query_year):
            return query_year.year in self.hash_years.keys()
            
        def list_years(self):
            for i in self.years:
                print(i.year)


    class Data:
        def __init__(self):
            self.products = []
            self.hash_products = {}
        
        def is_product_present(self, query_product):
            return query_product.product_name in self.hash_products.keys()
            
        def add_product(self, new_product):
            if not self.is_product_present( new_product):
                self.products.append(new_product)
                self.hash_products[new_product.product_name] = new_product
                    
        def list_products(self):
            for i in self.products:
                print(i.product_name)

    data = Data()
    for temp in items:
        prod = temp[1]
        yr = temp[0][-4:]
        cmp = temp[7]
        data.add_product(product(prod))
        data.hash_products[prod].add_year(year(yr))
        data.hash_products[prod].hash_years[yr].add_company(company(cmp))
        data.hash_products[prod].hash_years[yr].hash_companies[cmp].add_complaint()
    data.list_products()
    print(data.hash_products.keys())

    with open(output_dir, 'w', newline='') as csvfile:
        field_names = ["Product Name", "Year", "Total Compalaints", "Max complaints", "Highest Percentage"]
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for each_product in data.hash_products.values():
            for each_yr in each_product.hash_years.values():
                complaints = 0
                max_complaints = -1
                for each_company in each_yr.hash_companies.values():
                    complaints = complaints + each_company.complaints
                    max_complaints = max(max_complaints, each_company.complaints)
                print(each_product.product_name, each_yr.year, complaints, max_complaints, round((max_complaints/complaints)*100))
                
                writer.writerow({
                    "Product Name": each_product.product_name,
                    "Year": each_yr.year,
                    "Total Compalaints":complaints,
                    "Max complaints": max_complaints,
                    "Highest Percentage": round((max_complaints/complaints)*100) })
