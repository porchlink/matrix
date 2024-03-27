from freshbooks import FilterBuilder, PaginateBuilder, IncludesBuilder
from app.freshbooks.freshbooks_auth import *
from datetime import date
import pandas as pd

def get_invoices():
    filter = FilterBuilder()
    #filter.like("organization_like", "FREE")
    freshBooksClient, acc_id = auth()
    client = freshBooksClient.clients.list(acc_id)#,builders=[filter])
    # for k in client.data:
    #     print(k, client.data[k])
    #filter.equals("customerid", "71916")#.between("due_date", "2024-03-01","2024-03-31")
    filter.between("create_date", "2024-01-01", "2024-04-30")
    pg = PaginateBuilder(1,10000)
    includes = IncludesBuilder().include("issued_date")
    data = freshBooksClient.invoices.list(acc_id, builders=[pg, filter, includes]).data['invoices']
    keyValList = ['2024-03-20']
    print(pd.DataFrame(freshBooksClient.invoices.list(acc_id, builders=[filter]).data['invoices']))
    
    res = [d for d in data if d['due_date'] in keyValList]

    # >>> exampleSet = [{'type':'type1'},{'type':'type2'},{'type':'type2'}, {'type':'type3'}]
    # >>> keyValList = ['type2','type3']
    # >>> expectedResult = [d for d in exampleSet if d['type'] in keyValList]
    return freshBooksClient.invoices.list(acc_id, builders=[filter, includes]).data['invoices']#freshBooksClient.invoices.list(acc_id,builders=[filter]).data['invoices']