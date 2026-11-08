import csv
import sys
from pathlib import Path
from rapidstart_excel import read, write
ROOT=Path(__file__).resolve().parent.parent
SRC=sys.argv[1]   # QCS-03-TAX-TERMS export template
OUT=ROOT/'packages/QCS-03-TAX-TERMS_import.xlsx'
D=read(SRC); log=[]
def add(sheet,values,why):
    h=D[sheet]['hdr']; r=['']*len(h)
    for k,v in values.items(): r[h.index(k)]=v
    D[sheet]['rows'].append(r); log.append((sheet,'ADD',' | '.join(f'{k}={v}' for k,v in values.items() if v not in ('','false')),why))
def change(sheet,key,field,val,why):
    h=D[sheet]['hdr']
    for r in D[sheet]['rows']:
        if r[0]==key and r[h.index(field)]!=val:
            log.append((sheet,'CHANGE',f'{key}: {field} {r[h.index(field)]} -> {val}',why)); r[h.index(field)]=val

PT='Payment Terms'
add(PT,{'Code':'RECEIPT','Due Date Calculation':'0D','Discount %':'0','Description':'Due on receipt','Calc. Pmt. Disc. on Cr. Memos':'false'},'D-012: QuickBooks "Due on receipt"')
add(PT,{'Code':'2%10NET30','Due Date Calculation':'30D','Discount Date Calculation':'10D','Discount %':'2','Description':'2% 10, Net 30','Calc. Pmt. Disc. on Cr. Memos':'false'},'D-012: QuickBooks "2% 10 Net 30"')

change('321 Tax Group','SUPPLIES','Description','Taxable supplies','Template description refers to CRONUS ("Olympic")')

# jurisdictions: code, description, account, report-to, print order, print description, local rate
J=[('NC','North Carolina state','23100','NC','1','NC state tax'),
   ('NCMECK','Mecklenburg County, NC','23100','NC','2','Mecklenburg County tax'),
   ('NCCABARRUS','Cabarrus County, NC','23100','NC','2','Cabarrus County tax'),
   ('NCGASTON','Gaston County, NC','23100','NC','2','Gaston County tax'),
   ('NCUNION','Union County, NC','23100','NC','2','Union County tax'),
   ('SC','South Carolina state','23110','SC','1','SC state tax'),
   ('SCYORK','York County, SC','23110','SC','2','York County tax'),
   ('SCLANCAST','Lancaster County, SC','23110','SC','2','Lancaster County tax')]
for c,d,acc,rep,po,pd in J:
    add('320 Tax Jurisdiction',{'Code':c,'Description':d,'Tax Account (Sales)':acc,'Report-to Jurisdiction':rep,
        'Reverse Charge (Purchases)':'','Calculate Tax on Tax':'false','Adjust for Payment Discount':'false',
        'Name':d,'Country/Region':'US','Print Order':po,'Print Description':pd},'D-011')
AREAS=[('NC-MECK','Mecklenburg County, NC','NCMECK'),('NC-CABARRUS','Cabarrus County, NC','NCCABARRUS'),
       ('NC-GASTON','Gaston County, NC','NCGASTON'),('NC-UNION','Union County, NC','NCUNION'),
       ('SC-YORK','York County, SC','SCYORK'),('SC-LANCASTER','Lancaster County, SC','SCLANCAST')]
for a,d,cj in AREAS:
    add('318 Tax Area',{'Code':a,'Description':d,'Country/Region':'US','Round Tax':'To Nearest','Use External Tax Engine':'false'},'D-011')
    st=a[:2]
    add('319 Tax Area Line',{'Tax Area':a,'Tax Jurisdiction Code':st,'Calculation Order':'1'},'State rate')
    add('319 Tax Area Line',{'Tax Area':a,'Tax Jurisdiction Code':cj,'Calculation Order':'2'},'County rate')
# rates (Tax Below Maximum, %, with Maximum Amount 0 = applies to the full amount)
R=[('NC','',      '4.75','NCDOR: state rate'),
   ('NCMECK','',  '2.5', 'NCDOR: Mecklenburg local rate before 7/1/2026 (2.00 county + 0.50 transit)'),
   ('NCMECK','2026-07-01','3.5','NCDOR notice: +1.00% additional county rate from 7/1/2026 (total 8.25%)'),
   ('NCCABARRUS','','2.25','NCDOR: total 7%'),
   ('NCGASTON','','2.25','NCDOR: total 7%'),
   ('NCUNION','','2',  'NCDOR: total 6.75%'),
   ('SC','',      '6',   'SC DOR: state rate'),
   ('SCYORK','',  '1',   'SC DOR ST-500 (eff. 7/1/2025): total 7%'),
   ('SCLANCAST','','2',  'SC DOR ST-500 (eff. 7/1/2025): total 8%')]
for j,eff,rate,why in R:
    add('322 Tax Detail',{'Tax Jurisdiction Code':j,'Tax Group Code':'SUPPLIES','Tax Type':'Sales and Use Tax','Effective Date':eff,
        'Maximum Amount/Qty.':'0','Tax Below Maximum':rate,'Tax Above Maximum':'0','Calculate Tax on Tax':'false','Expense/Capitalize':'false'},why)
write(SRC,OUT,D)
with open(ROOT/'packages/reviews/QCS-03-TAX-TERMS-changes.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Table','Change','Detail','Reason / source']); w.writerows(log)
from collections import Counter; print(len(log),Counter((l[0],l[1]) for l in log))
