import ast, datetime, json, operator, os, random, re
from urllib.parse import quote_plus
from database import load_memory, save_memory, load_knowledge, save_knowledge
BASE_DIR=os.path.dirname(os.path.abspath(__file__))

def _import_legacy():
    memory=load_memory(); knowledge=load_knowledge()
    for filename,target in [('memory.json',memory),('knowledge.json',knowledge)]:
        path=os.path.join(BASE_DIR,filename)
        try:
            with open(path,'r',encoding='utf-8') as f: target.update(json.load(f))
        except Exception: pass
    save_memory(memory); save_knowledge(knowledge)
_import_legacy()

def banner(): return 'QUANTUM MIND AI\nThink Beyond. Learn Beyond.'
def speak(text): return str(text)

OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Mod:operator.mod,ast.Pow:operator.pow,ast.USub:operator.neg}
def calculate(expr):
    def ev(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
        if isinstance(n,ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.left),ev(n.right))
        if isinstance(n,ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.operand))
        raise ValueError('Unsupported calculation')
    return ev(ast.parse(expr,mode='eval').body)

def process_command(command, username='user'):
    raw=command.strip(); q=raw.lower().strip(); memory=load_memory(); knowledge=load_knowledge()
    if not q: return {'text':'Please type a message.'}
    if q in ('bye','exit','quit'): return {'text':'Goodbye!','exit':True}
    if q in ('help','commands'):
        return {'text':'Try: time, date, calculate 12*4, remember favourite colour: blue, what is my favourite colour, what did we talk about, define gravity, weather in Lagos, or ask a question.'}
    if q in ('time','what is the time','what time is it','current time'): return {'text':datetime.datetime.now().strftime('%I:%M %p')}
    if q in ('date',"what is today's date",'what is todays date',"today's date",'todays date','what date is it'): return {'text':datetime.datetime.now().strftime('%d %B %Y')}
    if q.startswith('calculate '):
        try: return {'text':str(calculate(raw[10:].strip()))}
        except Exception: return {'text':'I could not calculate that. Use numbers and operators such as +, -, *, /, **.'}
    if q in ('who created you','who made you'): return {'text':'I was created by Emmanuel Abraham for Softnet Technology Academy.'}
    if q=='who can use you': return {'text':'Quantum Mind is a private AI for authorized pupils, teachers and administrators of Softnet Technology Academy.'}
    if q.startswith('remember '):
        text=raw[9:].strip()
        if ':' not in text: return {'text':'Use this format: remember favourite colour: blue'}
        key,value=text.split(':',1); memory[key.strip().lower()]=value.strip(); save_memory(memory)
        return {'text':f'I will remember that your {key.strip()} is {value.strip()}.'}
    if q.startswith('remember that '):
        memory[f'note_{len(memory)+1}']=raw[14:].strip(); save_memory(memory); return {'text':'Saved to memory.'}
    if q.startswith('what is my '):
        key=q.replace('what is my ','',1).rstrip('?').strip()
        return {'text':memory.get(key,f"I don't have {key} saved yet.")}
    if q=='what did we talk about':
        hist=memory.get('_history',[]); return {'text':'Recent topics: '+', '.join(hist[-5:]) if hist else "We haven't talked about any saved topics yet."}
    if q.startswith('teach '):
        text=raw[6:].strip()
        if ':' not in text: return {'text':'Use: teach question: answer'}
        key,value=text.split(':',1); knowledge[key.strip().lower()]=value.strip(); save_knowledge(knowledge); return {'text':'Thank you. I learned that.'}
    if q in knowledge: return {'text':knowledge[q]}
    # conservative fuzzy knowledge matching, avoiding the old gravity-for-everything bug
    words=set(re.findall(r'\w+',q))
    best=None; score=0
    for k,v in knowledge.items():
        kw=set(re.findall(r'\w+',k.lower())); s=len(words & kw)/max(len(words|kw),1)
        if s>score: best,score=v,s
    if best and score>=0.65: return {'text':best}
    if q.startswith('define '):
        term=raw[7:].strip(); return {'text':f'I can look up “{term}” online.','url':'https://en.wikipedia.org/wiki/Special:Search?search='+quote_plus(term),'source':'Wikipedia'}
    if q.startswith('weather in '):
        city=raw[11:].strip(); return {'text':f'Open the weather results for {city}.','url':'https://www.google.com/search?q='+quote_plus('weather in '+city),'source':'Google weather results'}
    if q.startswith('news about '):
        topic=raw[11:].strip(); return {'text':f'Open the latest news results about {topic}.','url':'https://news.google.com/search?q='+quote_plus(topic),'source':'Google News'}
    if q.startswith(('what is ','who is ','how to ','why ','when ','where ')):
        return {'text':'I do not have a reliable saved answer yet. You can search the web or teach me the answer.','url':'https://www.google.com/search?q='+quote_plus(raw),'source':'Web search'}
    hist=memory.setdefault('_history',[]); hist.append(raw); memory['_history']=hist[-20:]; save_memory(memory)
    return {'text':"I don't know that yet. You can teach me with: teach question: answer",'url':'https://www.google.com/search?q='+quote_plus(raw),'source':'Web search'}
