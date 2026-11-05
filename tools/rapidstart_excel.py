"""Rewrite data rows of a BC RapidStart Excel export while keeping BC's XML map, tables and comments."""
import re, zipfile, openpyxl
from xml.sax.saxutils import escape
def col(i):
    s=''
    i+=1
    while i: i,r=divmod(i-1,26); s=chr(65+r)+s
    return s
def read(src):
    wb=openpyxl.load_workbook(src); out={}
    for ws in wb.worksheets:
        hdr=[c.value for c in ws[3]]
        n=len([h for h in hdr if h is not None])
        rows=[list(r[:n]) for r in ws.iter_rows(min_row=4,values_only=True)]
        rows=[[('' if v is None else str(v)) for v in r] for r in rows if any(v not in (None,'') for v in r)]
        out[ws.title]={'hdr':hdr[:n],'rows':rows}
    return out
def write(src,dst,data):
    z=zipfile.ZipFile(src); files={i.filename:z.read(i.filename) for i in z.infolist()}
    wbx=files['xl/workbook.xml'].decode()
    rels=files['xl/_rels/workbook.xml.rels'].decode()
    for name,rid in re.findall(r'<x:sheet name="([^"]+)" sheetId="\d+" r:id="([^"]+)"',wbx):
        target=re.search(r'Id="%s"[^>]*Target="([^"]+)"|Target="([^"]+)"[^>]*Id="%s"'%(rid,rid),rels)
        path='xl/'+(target.group(1) or target.group(2)).lstrip('/').replace('xl/','')
        sheet=files[path].decode()
        d=data[name]; n=len(d['hdr'])
        head=re.search(r'(<x:row r="1">.*?</x:row><x:row r="3">.*?</x:row>)',sheet,re.S).group(1)
        body=[]
        for i,r in enumerate(d['rows'],start=4):
            assert len(r)==n,(name,len(r),n)
            body.append(f'<x:row r="{i}">'+''.join(
                f'<x:c r="{col(j)}{i}" s="1" t="inlineStr"><x:is><x:t xml:space="preserve">{escape(v)}</x:t></x:is></x:c>'
                for j,v in enumerate(r))+'</x:row>')
        files[path]=re.sub(r'<x:sheetData>.*</x:sheetData>','<x:sheetData>'+head+''.join(body)+'</x:sheetData>',sheet,flags=re.S).encode()
        # matching table part
        srels=files[path.replace('worksheets/','worksheets/_rels/')+'.rels'].decode()
        for t in re.findall(r'Target="([^"]*tables/table\d+\.xml)"',srels):
            tp='xl/tables/'+t.split('tables/')[1]
            last=3+max(1,len(d['rows']))
            files[tp]=re.sub(r'ref="A3:([A-Z]+)\d+"',lambda m:f'ref="A3:{m.group(1)}{last}"',files[tp].decode()).encode()
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as o:
        for i in z.infolist(): o.writestr(i,files[i.filename])
