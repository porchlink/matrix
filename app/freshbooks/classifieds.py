from freshbooks import FilterBuilder, PaginateBuilder, IncludesBuilder
from app.freshbooks.freshbooks_auth import *
from datetime import date
import pandas as pd

def get_classifieds(community='pradera'):
    filter = FilterBuilder()
    freshBooksClient, acc_id = auth()
    filter.between("date_min", "2024-03-01").between("date_max", "2024-03-31")
    
    includes = IncludesBuilder().include("lines")
    
    pg = PaginateBuilder(1,100) 
    invoices = None
    data = list()
    due_date = ['2024-03-01']
    while not invoices or (invoices.pages.page < invoices.pages.pages):
        try:
            invoices = freshBooksClient.invoices.list(acc_id, builders=[filter, pg, includes])
        except Exception as e:
            print(e)
            print(e.status_code)
            exit(1)
        data_ = invoices.data['invoices']
        #data_ = [d for d in data_ if d['due_date'] == due_date[0]]
        #data_ = [d for d in [l for l in ] if d['due_date'] == due_date[0]]
        filtered_data = list()
        for d in data_:
            f_data = [d_ for d_ in d['lines'] if community.upper() in d_['name'].upper() and 'CL' in d_['name'].upper()]
            if len(f_data)>0:
                filtered_data.append(f_data[0])
        data.extend(data_)
        print(invoices.pages.page)
        pg.page(invoices.pages.page + 1)

    # keyValList = ['2024-03-20']
    # res = [d for d in data if d['due_date'] in keyValList]

    # >>> exampleSet = [{'type':'type1'},{'type':'type2'},{'type':'type2'}, {'type':'type3'}]
    # >>> keyValList = ['type2','type3']
    # >>> expectedResult = [d for d in exampleSet if d['type'] in keyValList]
    print(len(filtered_data))
    return filtered_data