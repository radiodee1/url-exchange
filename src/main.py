#!/usr/bin/python3 



from exchange import Exchange 
import argparse
import os 
import openai
from pipeline import PipelineCloud
import time
from word2number import w2n
import string
from prepend import PREPEND
from threading import Thread, Event
#from queue import Queue
import curses 
from curses.textpad import Textbox, rectangle 
import sys 

e = Exchange()

'''
stdscr = curses.initscr()
rows, cols = stdscr.getmaxyx()
#curses.echo()
#curses.nocbreak()
curses.endwin()

'''


def add_to_q_history(h, HISTORY):
    HISTORY += "\n\nHuman: " + h
    return HISTORY

def add_to_a_history(h, HISTORY):
    HISTORY += "\nJane: " + h
    return HISTORY

def get_gpt(question):

    #HIDE Authentication message!!                  
    #devnull = open('/dev/null', 'w')
    #oldstdout_fno = os.dup(sys.stdout.fileno())
    #os.dup2(devnull.fileno(), 1)

    output = ""
    prompt = question.strip()
    pipeline_token = os.environ['GPT_ETC_GPTJ_MODEL']
    pipeline_key = os.environ['GPT_ETC_GPTJ_KEY']
    api = PipelineCloud(token=pipeline_key)
    run = api.run_pipeline(
        pipeline_token,
        [
            prompt, # [prompt],
            {
                "response_length": 64,
                "temperature": 0.001, #1.0,
                "top_k": 1 ## 50
            },
        ],
    )
    if run != None:
        try:
            output = run["result_preview"][0][0]
        except:
            print(run)
            pass
    else: 
        output = ""
    
    ## RESTORE Output
    #os.dup2(oldstdout_fno, 1)
    
    return output

def get_gpt3(question):
        
    question = question.strip()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=64,
        temperature=0
    )
    output = completion.choices[0].text 
    #print(output)
    #position_top()
    return output

def get_status_thread(event, inwin):
    num = 0 
    while True:
        #if not event.is_set():
        time.sleep(10)
        out = e.get_status().strip()
        #print(num, 'thread', end=' ')
        if not event.is_set():
            #q.put(out)
            if len(out) != 0:
                #print(out)
                inwin.addstr(1,0, out)
                inwin.noutrefresh()
                inwin.refresh()
                #sys.stdout.write(out)
                
        num += 1 
        #print("*> ", end='')
        pass 

def main(stdscr):

    event = Event()
    num = 0 
    e.set_verbose(args.verbose)
    
    e.load()
    
    e.set_path(args.path)
   
    query = get_gpt3
    if args.gptj:
        query = get_gpt 

    e.set_query_cmd(query) ## input or get_gpt

    HISTORY = ""


    stdscr.addstr(0, 0, "URL Exchange: (hit Enter to send)")

    editwin = curses.newwin(7*3+2,50, 1,1)
    #stdscr.refresh()
    statwin = editwin.subwin(5, 50, 1, 1) 
    rectangle(stdscr, 1,0, 7-1, 1+50+1)
    
    inwin = editwin.subwin(5, 50, 7, 1)
    rectangle(stdscr, 7, 0, 7*2-2, 1+50+1)

    outwin = editwin.subwin(5 ,50, 7*2-1,1)
    rectangle(stdscr, 7*2-1, 0, 7*3-3, 1+50+1)
    
    hidewin = editwin.subwin(1,1,7*3+1,1)

    #outwin.addstr(1,0 , "out...")
    #inwin.addstr(1,0, "Here...")
    statwin.addstr(1,0, "> ")
    stdscr.refresh()
    #curses.doupdate()

    q = 0 
    t1 = Thread(target=get_status_thread, args=(event,inwin))
    t1.start()

       
    while True:
        box1 = Textbox(statwin, insert_mode=True )
    
        box1.edit(enter_is_terminate)
        x = box1.gather()
        
        XPREPENDX = PREPEND['include-url']
        #print("--Main--", XPREPENDX)
        XPREPENDX += HISTORY
        xx = XPREPENDX + "\n\nHuman: " + x.strip() + "\nJane: "
        HISTORY = add_to_q_history(x, HISTORY)

        event.set()
        hidewin.addstr(0, 0, "")
        hidewin.refresh()
 
        out = query(xx)
        out = e.mod_output(out)
        HISTORY = add_to_a_history(out, HISTORY)
        
        #outwin.addstr(1,1,'')
        #outwin.noutrefresh()
        #outwin.refresh()
      
        outwin.erase()
        outwin.addstr(1,0, out)
        outwin.noutrefresh()
        outwin.refresh()

        event.clear()
        
        x = e.mod_output(x)
        x = e.mod_input(x)
        
        if e.detect_input_post_query(x) or e.detect_input_post_query(out):
            z = e.set_input_post_query(x) ## x ??
        num += 1 
        
        statwin.erase()
        statwin.addstr(1,0, "> ")
        
        #inwin.erase()
        inwin.addstr(1,0,'')
        #editwin.refresh() ## <-- bad
        stdscr.refresh()
    

def enter_is_terminate(x):
    if x == 10:
        x = 7
    return x

if  __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--timer', action='store_true', help='Use timer for wizard output.')
    parser.add_argument('--gptj',action='store_true', help='use gptj instead of gpt3.')
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument("--path", default="./../data/", help="default data directory")
    args = parser.parse_args()
    
    #print("URL Exchange")

    if args.timer:
        curses.wrapper(main) 
        sys.exit()

