import openpyxl, csv, re, shutil, zipfile
from xml.sax.saxutils import escape
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
SRC=sys.argv[1]   # QCS-01-COA export template
OUT=ROOT/'packages/QCS-01-COA_import.xlsx'
ws=openpyxl.load_workbook(SRC).worksheets[0]
hdr=[c.value for c in ws[3]]
rows={r[0]:list(r) for r in ws.iter_rows(min_row=4,values_only=True)}
orig={k:list(v) for k,v in rows.items()}
NO,NAME,TYPE,CAT,IB,BLK,DP,TOT=range(8)
mp=list(csv.DictReader(open(ROOT/'mapping/account-mapping.csv',encoding='utf-8')))
log=[]
def setv(no,idx,val,why):
    old=rows[no][idx]
    if old!=val:
        rows[no][idx]=val; log.append((no,hdr[idx],old,val,why))

for m in mp:
    n=m['BC No.']
    if not n: continue
    if m['Action'] in ('Rename','Keep'):
        assert n in rows, n
        setv(n,NAME,m['BC Name'],'Client name (account mapping)')
    elif m['Action']=='New':
        assert n not in rows, n
        first=n[0]
        cat,ib={'1':('Assets','Balance Sheet'),'2':('Liabilities','Balance Sheet'),'3':('Equity','Balance Sheet'),
                '4':('Income','Income Statement'),'5':('Cost of Goods Sold','Income Statement'),
                '6':('Expense','Income Statement'),'7':('Expense','Income Statement')}[first]
        rows[n]=[n,m['BC Name'],'Posting',cat,ib,'false','true','']
        log.append((n,'(new account)','',f"{m['BC Name']} | Posting | {cat} | {ib}",'New account (account mapping)'))

# End-Total and group headings that go with the renamed groups
setv('40199',NAME,'Total, Sales','Matches renamed Begin-Total 40100')
setv('71999',NAME,'Total, Payroll Expenses','Matches renamed Begin-Total 71000')
setv('61000',NAME,'Fixed Asset Costs','Group now holds Depreciation Expense (61900)')
setv('61999',NAME,'Total, Fixed Asset Costs','Matches renamed Begin-Total 61000')
# Category fix
setv('40330',CAT,'Income','Template classifies interest income as Expense')
# Subledger-controlled accounts: no direct posting
for n,why in [('15110','AR control account: posts only through customers'),
              ('22100','AP control account: posts only through vendors'),
              ('14140','Inventory control account: posts only through items'),
              ('18200','Bank G/L account: posts only through the bank account'),
              ('18210','Bank G/L account: posts only through the bank account'),
              ('18220','Bank G/L account: posts only through the bank account'),
              ('22510','Credit card G/L account: posts only through the bank account')]:
    setv(n,DP,'false',why)

# sanity: every new posting account falls inside an End-Total range
ends=[(r[TOT]) for r in rows.values() if r[TYPE]=='End-Total']
def covered(n):
    for t in ends:
        for part in t.split('|'):
            if '..' in part:
                a,b=part.split('..')
                if a<=n<=b: return True
    return False
for n,r in rows.items():
    if r[TYPE]=='Posting': assert covered(n), n

# ---- write sheet XML in BC's own format ----
z=zipfile.ZipFile(SRC); files={i.filename:z.read(i.filename) for i in z.infolist()}
sheet=files['xl/worksheets/sheet1.xml'].decode('utf-8')
def cell(ref,val):
    return f'<x:c r="{ref}" s="1" t="inlineStr"><x:is><x:t xml:space="preserve">{escape(val or "")}</x:t></x:is></x:c>'
head_rows=re.search(r'(<x:row r="1">.*?</x:row><x:row r="3">.*?</x:row>)',sheet,re.S).group(1)
body=[]
for i,no in enumerate(sorted(rows),start=4):
    r=rows[no]
    body.append(f'<x:row r="{i}">'+''.join(cell(f'{c}{i}',v) for c,v in zip('ABCDEFGH',r))+'</x:row>')
last=3+len(rows)
new_sheet=re.sub(r'<x:sheetData>.*</x:sheetData>','<x:sheetData>'+head_rows+''.join(body)+'</x:sheetData>',sheet,flags=re.S)
files['xl/worksheets/sheet1.xml']=new_sheet.encode('utf-8')
tbl=files['xl/tables/table1.xml'].decode('utf-8').replace('A3:H353',f'A3:H{last}')
files['xl/tables/table1.xml']=tbl.encode('utf-8')
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as o:
    for i in z.infolist(): o.writestr(i,files[i.filename])
# change log for review
with open(ROOT/'packages/reviews/QCS-01-COA-changes.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['G/L Account','Field','Template value','New value','Reason']); w.writerows(sorted(log))
print('accounts:',len(rows),'changes:',len(log),'last row',last)
from collections import Counter; print(Counter(l[1] for l in log))
