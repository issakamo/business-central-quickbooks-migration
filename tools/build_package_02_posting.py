import csv, copy
import sys
from pathlib import Path
from rapidstart_excel import read, write
ROOT=Path(__file__).resolve().parent.parent
SRC=sys.argv[1]   # QCS-02-POSTING export template
OUT=ROOT/'packages/QCS-02-POSTING_import.xlsx'
D=read(SRC); log=[]
def rowdict(sheet,r): return dict(zip(D[sheet]['hdr'],r))
def add(sheet,values,why):
    h=D[sheet]['hdr']; r=['']*len(h)
    for k,v in values.items(): r[h.index(k)]=v
    D[sheet]['rows'].append(r); log.append((sheet,'ADD',' | '.join(f'{k}={v}' for k,v in values.items() if v not in ('','false')),why))
def change(sheet,keyfn,field,val,why):
    h=D[sheet]['hdr']
    for r in D[sheet]['rows']:
        if keyfn(rowdict(sheet,r)):
            old=r[h.index(field)]
            if old!=val:
                r[h.index(field)]=val; log.append((sheet,'CHANGE',f"{'/'.join(x for x in r[:2] if x) or '(blank)'}: {field} {old or '(empty)'} -> {val}",why))

# 1 Location: MAIN
h=D['Location']['hdr']; bools=[i for i,x in enumerate(h) if x in ('Use As In-Transit','Require Put-away','Require Pick','Use Cross-Docking','Require Receive','Require Shipment','Bin Mandatory','Directed Put-away and Pick','Use Put-away Worksheet','Pick According to FEFO','Allow Breakbulk','Check Warehouse Class','Always Create Put-away Line','Always Create Pick Line','Use ADCS','Do Not Use For Tax Calculation')]
D['Location']['rows']=[]
add('Location',{'Code':'MAIN','Name':'Charlotte Warehouse','Address':'4810 Freight Way','City':'Charlotte','State':'NC','ZIP Code':'28206','Country/Region Code':'US',**{h[i]:'false' for i in bools}},
    'The client has one warehouse (brief). Basic setup only: no warehouse documents at go-live')

# 2/3 posting groups
add('250 Gen. Business Posting Group',{'Code':'MIGRATION','Description':'Opening balances only (do not use)','Auto Insert Default':'true'},'D-006')
for c,dsc in [('CHEMICALS','Cleaning chemicals'),('PAPER','Paper & can liners'),('EQUIPMENT','Equipment & tools')]:
    add('251 Gen. Product Posting Group',{'Code':c,'Description':dsc,'Auto Insert Default':'true'},'D-007')

# 5 General Posting Setup
GPS='252 General Posting Setup'
tmpl={k:v for k,v in rowdict(GPS,[r for r in D[GPS]['rows'] if r[0]=='DOMESTIC' and r[1]=='RETAIL'][0]).items()}
blank_tmpl={k:v for k,v in rowdict(GPS,[r for r in D[GPS]['rows'] if r[0]=='' and r[1]=='RETAIL'][0]).items()}
# block every template combination (none are used by the client)
for r in D[GPS]['rows']:
    pass
for r in list(D[GPS]['rows']):
    key=(r[0],r[1])
    change(GPS,lambda d,k=key:(d['Gen. Bus. Posting Group'],d['Gen. Prod. Posting Group'])==k,'Blocked','true','Template combination not used by the client')
sales={'CHEMICALS':'40140','PAPER':'40150','EQUIPMENT':'40160'}
for p,acc in sales.items():
    v=dict(tmpl); v.update({'Gen. Bus. Posting Group':'DOMESTIC','Gen. Prod. Posting Group':p,'Sales Account':acc,'Sales Credit Memo Account':acc,
        'Inventory Adjmt. Account':'50140','Description':f'Domestic trade, {p.lower()}','Blocked':'false'})
    add(GPS,v,'Copied from template DOMESTIC/RETAIL; sales account per D-007; adjustments to 50140')
    v=dict(blank_tmpl); v.update({'Gen. Bus. Posting Group':'','Gen. Prod. Posting Group':p,'Inventory Adjmt. Account':'50140','Description':f'Item journals, {p.lower()}','Blocked':'false'})
    add(GPS,v,'Copied from template (blank)/RETAIL; used by item journals (counts, adjustments)')
    v={k:('false' if k in ('View All Accounts on Lookup','Blocked') else '') for k in tmpl}
    v.update({'Gen. Bus. Posting Group':'MIGRATION','Gen. Prod. Posting Group':p,'Inventory Adjmt. Account':'25900','Description':f'Opening stock only, {p.lower()}'})
    add(GPS,v,'D-006: opening stock credits the clearing account; sales/purchase accounts left empty on purpose')

# 7/8 customer & vendor posting groups: verify, no change
cpg=rowdict('92 Customer Posting Group',[r for r in D['92 Customer Posting Group']['rows'] if r[0]=='DOMESTIC'][0])
vpg=rowdict('93 Vendor Posting Group',[r for r in D['93 Vendor Posting Group']['rows'] if r[0]=='DOMESTIC'][0])
assert cpg['Receivables Account']=='15110' and vpg['Payables Account']=='22100'

# D-010 payment tolerance
for f in ('Payment Tolerance Debit Acc.','Payment Tolerance Credit Acc.'):
    change('92 Customer Posting Group',lambda d:d['Code']=='DOMESTIC',f,'40910','D-010: customer underpayments written off are a discount, not interest')
    change('93 Vendor Posting Group',lambda d:d['Code']=='DOMESTIC',f,'68290','D-010: vendor tolerance is a purchase discount, not interest')
# 9 bank account posting groups
change('277 Bank Account Posting Group',lambda d:d['Code']=='SAVINGS','G/L Account No.','18220','Savings G/L account from the account mapping')
add('277 Bank Account Posting Group',{'Code':'PAYROLL','G/L Account No.':'18210'},'Payroll Checking (account mapping)')
add('277 Bank Account Posting Group',{'Code':'CREDITCARD','G/L Account No.':'22510'},'D-009: credit card as a bank account')

# 6 inventory posting setup
IPS='5813 Inventory Posting Setup'
v=rowdict(IPS,D[IPS]['rows'][0]); v.update({'Location Code':'MAIN','Description':'Charlotte Warehouse, resale stock'})
add(IPS,v,'Inventory account for stock at location MAIN (blank-location row already exists)')

write(SRC,OUT,D)
with open(ROOT/'packages/reviews/QCS-02-POSTING-changes.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Table','Change','Detail','Reason']); w.writerows(log)
from collections import Counter; print(len(log), Counter((l[0],l[1]) for l in log))
print('referenced by DOMESTIC customer group:',{k:v for k,v in cpg.items() if v and k.endswith(('Acc.','Account'))})
print('referenced by DOMESTIC vendor group:',{k:v for k,v in vpg.items() if v and k.endswith(('Acc.','Account'))})
