#!/usr/bin/env python3
"""Deterministic BDP retrieval; no credentials, models or non-BDP routes."""
import argparse,json,os,re,sys,time,unicodedata,urllib.request,urllib.parse,urllib.error
MEDIA='application/vnd.bdp.v0.1+json'
BASE=os.environ.get('CHRIS_BOT_BDP_ORIGIN','https://chris-bot.sellsbrothers.com').rstrip('/')

class BdpHttpError(RuntimeError):
    def __init__(self,status,result):
        self.status=status
        super().__init__(f'BDP HTTP {status}: {json.dumps(result)}')

def compact(s):
    return ''.join(c for c in unicodedata.normalize('NFKC',s).lower() if not c.isspace() and c not in '_-')
def request(path,body=None):
    target=urllib.parse.urljoin(BASE+'/',path)
    if urllib.parse.urlsplit(target).netloc!=urllib.parse.urlsplit(BASE).netloc:raise ValueError('Cross-origin BDP request refused')
    headers={'Accept':MEDIA,'User-Agent':''}
    if body is not None:headers['Content-Type']=MEDIA
    req=urllib.request.Request(target,headers=headers,data=None if body is None else json.dumps(body).encode())
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=90) as r:result=json.load(r);status=r.status
        except urllib.error.HTTPError as e:
            status=e.code
            raw=e.read().decode()
            try:result=json.loads(raw)
            except json.JSONDecodeError:result={'detail':raw[:400]}
        log=os.environ.get('CHRIS_BOT_HTTP_LOG')
        if log:
            with open(log,'a') as f:f.write(json.dumps({'url':target,'method':'GET' if body is None else 'POST','request':body,'status':status,'response':result,'attempt':attempt+1})+'\n')
        if status in [502,503,504] and attempt<2:
            time.sleep(2**attempt);continue
        if status!=200:raise BdpHttpError(status,result)
        return result

def field(name):return {'op':'field','of':{'op':'binding','name':'b'},'path':['properties',*name.split('.')]}
def compare(name,op,value):return {'op':'compare','operator':op,'left':field(name),'right':{'op':'literal','value':value}}
def query(selection,form='resources'):
    return request('/read?readVersion=1&operation=query',{'query':{'ir':'bdp-query-design-1','profile':'query','selection':selection,'result':{'form':form}}})['result']
def resource_view(resource):
    # The search-only normalized duplicate adds no evidence for the answer.
    # Retain original text, attribution and identity; HTTP logs keep the full wire record.
    return {**resource,'properties':{k:v for k,v in resource['properties'].items() if k!='search'}}
def search(args):
    terms=[compact(t) for t in args.terms]
    predicates=[{'op':'typeIs','of':{'op':'binding','name':'b'},'type':'https://sellsbrothers.com/ns/chris-bot/'+('source' if args.sources else 'passage'),'match':'exact'},
                {'op':'or','operands':[{'op':'contains','text':field('search.compact'),'substring':{'op':'literal','value':t}} for t in terms]}]
    if not args.fiction:predicates.append(compare('genre','ne','fiction'))
    if not args.unverified:predicates.append(compare('attribution.confidence','ne','unverified'))
    for key,value in [('kind',args.kind),('voice',args.voice)]:
        if value:predicates.append(compare(key,'eq',value))
    if args.since:predicates.append(compare('published','ge',args.since))
    if args.until:predicates.append(compare('published','lt',args.until))
    selection={'op':'filter','input':{'op':'scan','collection':'beads'},'bind':'b','predicate':{'op':'and','operands':predicates}}
    if args.count:return query(selection,'count')
    try:result=query(selection)
    except BdpHttpError as error:
        if error.status!=413:raise
        result=query(selection,'count')
        return {'count':result['count'],'refine':'Result exceeds a delivery bound. Narrow with --since/--until, --kind, a longer phrase, or --sources; no partial result was returned.'}
    limit=args.limit if args.limit is not None else (50 if args.sources else 12)
    items=rank_matches(result['items'],terms,limit,recent=args.recent)
    order='publication date first' if args.recent else 'topic titles and substantive attributed sources first, date within each group'
    return {'count':len(result['items']),'shown':len(items),'selection':order+'; at most two passages per source','items':[resource_view(r) for r in items]}

def rank_matches(items,terms,limit,recent=False):
    def key(r):
        p=r['properties'];substantive=p.get('kind')!='tweet'
        title=compact(p.get('source_title') or p.get('title') or '')
        firsthand=(p.get('voice')=='chris' and p.get('kind')!='talk') or p.get('speakers')=='labeled'
        relevance=(substantive and any(t in title for t in terms),substantive,firsthand,p.get('published',''),r['id'])
        return (p.get('published',''),*relevance) if recent else relevance
    ranked=sorted(items,key=key,reverse=True);selected=[];seen={}
    for r in ranked:
        source=r['properties'].get('source_id') or r['id']
        if seen.get(source,0)>=2:continue
        selected.append(r);seen[source]=seen.get(source,0)+1
        if len(selected)>=limit:break
    return selected

def context(ref,unverified=False):
    if not ref.startswith(('http://','https://')):ref=BASE+'/sources/'+urllib.parse.quote(ref,safe='')
    source=request(ref)
    if not source['type'].endswith('/source'):raise ValueError('Context requires a source Bead')
    if source['properties'].get('attribution',{}).get('confidence')=='unverified' and not unverified:raise ValueError('Unverified transcript: use --unverified only to examine the transcript as an artifact, never as verified personal testimony.')
    selection={'op':'endpoints','input':{'op':'walk','roots':{'op':'refs','collection':'beads','references':[source['id']]},'direction':'outgoing'},'side':'target'}
    items=query(selection)['items']
    return {'source':resource_view(source),'passages':[resource_view(r) for r in sorted(items,key=lambda r:r['properties']['ordinal'])]}
def review_draft(draft):
    flags=[]
    for sentence in re.split(r'(?<=[.!?])\s+',draft):
        uncertain=re.search(r"(?:can(?:not|['’]t) (?:establish|determine|confirm)|don['’]t know)",sentence,re.I)
        current=re.search(r'\b(today|now|currently|still)\b',sentence,re.I)
        position=re.search(r"\bI(?: (?:now|currently|still|don['’]t|would|wouldn['’]t)){0,2} (?:recommend|think|prefer|believe|use|point)\b|\bmy (?:current )?view\b",sentence,re.I)
        if current and position and not uncertain:flags.append('undated-current-position')
    if re.search(r"\bI (?:never|have never|haven['’]t|didn['’]t) (?:gave|give|say|said|write|wrote|written|published|publish|explain|explained)\b",draft,re.I):flags.append('unsupported-absence-claim')
    return sorted(set(flags))

def main():
    p=argparse.ArgumentParser(description=__doc__);subs=p.add_subparsers(dest='command',required=True)
    s=subs.add_parser('search');s.add_argument('terms',nargs='+');s.add_argument('--sources',action='store_true');s.add_argument('--kind',choices=['blog','article','book','talk','tweet']);s.add_argument('--voice',choices=['chris','coauthored','conversation']);s.add_argument('--since');s.add_argument('--until');s.add_argument('--fiction',action='store_true');s.add_argument('--unverified',action='store_true');s.add_argument('--count',action='store_true');s.add_argument('--limit',type=int)
    s.add_argument('--recent',action='store_true',help='Rank matching sources by publication date before topic-title relevance')
    c=subs.add_parser('context');c.add_argument('reference');c.add_argument('--unverified',action='store_true')
    g=subs.add_parser('get');g.add_argument('path',nargs='?',default='/')
    v=subs.add_parser('verify',help='Check a draft supplied on stdin for demonstrated grounding failures and an optional length bound')
    v.add_argument('--max-words',type=int,help='Flag a draft that exceeds the requested conversational word budget')
    a=p.parse_args()
    if a.command=='verify':
        draft=sys.stdin.read();flags=review_draft(draft);words=len(draft.split())
        if a.max_words is not None:
            if a.max_words<1:p.error('--max-words must be positive')
            if words>a.max_words:flags.append('over-word-budget')
        print(json.dumps({'words':words,'max_words':a.max_words,'requires_revision':flags,'scope':'Deterministic length and narrow wording checks; not factual or voice certification.','action':'Shorten an over-budget reply to the current turn. Keep historical views dated and state unknown facts without claims about never publishing them.' if flags else 'Check each claim, speaker and date against the retrieved passages.'}));return
    if a.command=='search' and a.limit is not None and not 1<=a.limit<=250:p.error('--limit must be between 1 and 250')
    result=search(a) if a.command=='search' else context(a.reference,a.unverified) if a.command=='context' else request(a.path)
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,urllib.error.URLError) as e:print(str(e),file=sys.stderr);sys.exit(1)
