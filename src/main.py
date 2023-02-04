#!/usr/bin/python3 



from exchange import Exchange 
import argparse
import os 
import openai
#from pipeline import PipelineCloud
import requests 
import time
from word2number import w2n
import string
from prepend import PREPEND
from threading import Thread, Event
import json
import curses 
from curses.textpad import Textbox, rectangle 
import sys
import traceback

e = Exchange()

join_and_end = False
#t1 = Thread()

def add_to_q_history(h, HISTORY):
    HISTORY += "\n\nHuman: " + h
    return HISTORY

def add_to_a_history(h, HISTORY):
    HISTORY += "Jane: " + h
    return HISTORY

def get_gpt(question):

    output = ""
    prompt = question.strip()
    pipeline_token = os.environ['GPT_ETC_GPTJ_MODEL']
    pipeline_key = os.environ['GPT_ETC_GPTJ_KEY']

    response = requests.post(
        url="https://api.pipeline.ai/v2/runs",
        headers={"Authorization": "Bearer " + pipeline_key},
        json={
            "pipeline_id": pipeline_token,
            "data": [
                prompt ,
                {
                    "response_length": 64,
                    "temperature": 0.001, #1.0,
                    "top_k": 1 ## 50

    }]})
    
    if response != None:
        try:
            output = json.loads(response.text) #["result_preview"][0][0]
            output = output['result_preview'][0][0]
        except:
            print(response)
            while True:
                time.sleep(15)
                pass
            exit()
            pass
    else: 
        output = ""
   
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
    try:
        num = 0 
        while True:
            if join_and_end:
                break
            #if not event.is_set():
            time.sleep(10)
            out = e.get_status().strip()
            #print(num, 'thread', end=' ')
            if not event.is_set():
                inwin.erase()

                if len(out) != 0:
                    #print(out)
                    inwin.addstr(1,0, out)
                inwin.noutrefresh()
                inwin.refresh()
                    #sys.stdout.write(out)
                    
            num += 1 
            #print("*> ", end='')
            pass 
    except:
        curses.nocbreak()
        curses.echo()
        curses.endwin()


def main(stdscr):

    event = Event()
    num = 0 
    e.set_verbose(False)
    
    e.load()
    
    e.set_path(args.path)
   
    query = get_gpt3
    if args.gptj:
        query = get_gpt 

    e.set_query_cmd(query) ## input or get_gpt

    global HISTORY
    
    HISTORY = ""

    ## CURSES stuff here...
    stdscr.addstr(0, 0, "URL Exchange: (hit Enter to send)")

    editwin = curses.newwin(7*3+2+15,50, 1,1)
    #stdscr.refresh()
    statwin = editwin.subwin(5, 50, 1, 1) 
    rectangle(stdscr, 1,0, 7-1, 1+50+1)
    
    outwin = editwin.subwin(5, 50, 7, 1)
    rectangle(stdscr, 7, 0, 7*2-2, 1+50+1)

    inwin = editwin.subwin(5+15 ,50, 7*2-1,1)
    rectangle(stdscr, 7*2-1, 0, 7*3-3+15, 1+50+1)
    
    #hidewin = editwin.subwin(1,1,7*3+1,1)

    statwin.addstr(1,0, "> ")
    stdscr.refresh()
    #curses.doupdate()

    if args.timer:
        q = 0 
        t1 = Thread(target=get_status_thread, args=(event,inwin))
        t1.start()

    try:       
        while True:
            box1 = Textbox(statwin, insert_mode=True )
        
            box1.edit(enter_is_terminate)
            x = box1.gather()

            x = x.replace('> ', '') 
            XPREPENDX = PREPEND['include-url']
            #print("--Main--", XPREPENDX)
            XPREPENDX += HISTORY
            xx = XPREPENDX + "\n\nHuman: " + x.strip() + "\nJane: "
            HISTORY = add_to_q_history(x, HISTORY)

            event.set()
     
            out = query(xx)
            out = e.mod_output(out)
            HISTORY = add_to_a_history(out, HISTORY)
            
            outwin.erase()
            outwin.addstr(1,0, out) ## <-- good !!
            outwin.noutrefresh()
            outwin.refresh()

            event.clear()

            if args.timer:
                
                x = e.mod_output(x)
                x = e.mod_input(x)
                
                if e.detect_input_post_query(x) or e.detect_input_post_query(out):
                    z = e.set_input_post_query(x) ## x ??
            
            num += 1 
            
            statwin.erase()
            statwin.addstr(1,0, "> ")
            
            inwin.addstr(1,0,'')
            #editwin.refresh() ## <-- bad
            stdscr.refresh()
    except :
        global join_and_end
        join_and_end = True
        traceback.print_exc()
        if args.timer:
            t1.join() 
    finally:
        pass 

        

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
    
    #if args.verbose:
    #    sys.stdout = Logger()
    #print("URL Exchange")

    curses.wrapper(main) 
    join_and_end = True
    #if args.timer:
    #    t1.join()
    #sys.exit()

    curses.nocbreak()
    curses.echo()
    curses.endwin()
    #os.system('clear')
    if args.verbose:
        print(HISTORY)
