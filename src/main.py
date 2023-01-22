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
from queue import Queue
import curses 
from curses.textpad import Textbox, rectangle 
import sys 

e = Exchange()

stdscr = curses.initscr()
rows, cols = stdscr.getmaxyx()
#curses.echo()
#curses.nocbreak()
curses.endwin()

def position_top():
    #sys.stdout.write("\x1b[f")
    #os.system('clear')
    print("\033[%d;%dH" % (0, 0), end='')

    for _ in range(2):
        for _ in range(cols - 1):
            print(' ', end='')
    print("\033[%d;%dH" % (0, 0) + "> ", end='')



def position_mid(y):
    print("\033[%d;%dH" % (y, 0), end='')

def position_clear(x,y):
    x = min(x, cols)
    for _ in range(y):
        for _ in range(x):
            print(' ', end='')
            #sys.stdout.write(' ')
        print()

def position_line(y):
    y = min(y, rows)
    print("\033[%d;%dH" % (y, 0), end='')

    for _ in range(cols - 1):
        #sys.stdout.write('_')
        print('_', end='')
    print("\033[%d;%dH" % (0, 0) + "> ", end='')

    #sys.stdout.write('\x1b[f> ')

def add_to_q_history(h, HISTORY):
    HISTORY += "\n\nHuman: " + h
    return HISTORY

def add_to_a_history(h, HISTORY):
    HISTORY += "\nJane: " + h
    return HISTORY

def get_gpt(question):
    if args.timer:
        #position_mid(6)
        position_mid(6)
        position_clear(200, 4)
        position_top()
        position_mid(6)


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
    #position_top()
    return output

def get_gpt3(question):
    if args.timer:
        #position_mid(6)
        position_mid(6)
        position_clear(200, 4)
        position_top()
        position_mid(6)


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

def get_status_thread(q):
    num = 0 
    while True:
        #if not event.is_set():
        time.sleep(10)
        out = e.get_status().strip()
        #print(num, 'thread', end=' ')
        if not event.is_set():
            #q.put(out)
            if len(out) != 0:
                position_top()
                position_mid(11)
                position_clear(200, 9)
                position_top()
                position_mid(11)
                print(out)
                #sys.stdout.write(out)
                position_top()
        num += 1 
        #print("*> ", end='')
        pass 

def main(stdscr):
    stdscr.addstr(0, 0, "Enter message: (hit Enter to send)")

    editwin = curses.newwin(5*3+6,30, 2,1)
    rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
    #stdscr.refresh()
     
    inwin = editwin.subwin(5, 30, 5+2, 1)
    rectangle(stdscr, 5+2, 0, 5*2+2, 1+30+1)

    outwin = editwin.subwin(5 ,30, 5*2+2,1)
    rectangle(stdscr, 1+5*2+1+1, 0, 5*3+4, 1+30+1)
    
    outwin.addstr(1,0 , "out...")
    inwin.addstr(1,0, "Here...")
    stdscr.refresh()

    box = Textbox(inwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit(enter_is_terminate)

    # Get resulting contents
    message = box.gather()

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
    

    event = Event()
    q = Queue()

    if args.timer:
        t1 = Thread(target=get_status_thread, args=(q,))
        t1.start()

    num = 0 
    e.set_verbose(args.verbose)
    
    e.load()
    
    e.set_path(args.path)
   
    query = get_gpt3
    if args.gptj:
        query = get_gpt 

    e.set_query_cmd(query) ## input or get_gpt

    HISTORY = ""

    print("URL Exchange")

    if args.timer:
        curses.wrapper(main)
        exit()

    os.system('clear')
    position_top()
    position_clear(200, 20)
 
    position_line(10)
    position_line(5)
    position_line(20)
            #   
    while True:
        #position_top()
        #position_line(10)
        #position_line(5)
        #position_line(20)
         
        #position_top()
        x = input()
        #if args.timer:
        #    event.set()
        XPREPENDX = PREPEND['include-url']
        #print("--Main--", XPREPENDX)
        XPREPENDX += HISTORY
        xx = XPREPENDX + "\n\nHuman: " + x.strip() + "\nJane: "
        HISTORY = add_to_q_history(x, HISTORY)

        if args.verbose:
            print('--xxx--', xx, '--xxx--', sep="\n")
            print(x)

        if args.timer:
            event.set()

        position_mid(6)
        position_clear(200, 4)
        position_top()
        position_mid(6)

        out = query(xx)
        if args.verbose:
            print("--- long list ---", out, "--- end ---", sep="\n")
        out = e.mod_output(out)
        HISTORY = add_to_a_history(out, HISTORY)

        position_mid(6)
        position_clear(200, 4)
        position_top()
        position_mid(6)

        print(out)
        position_top()

        if args.timer:
            event.clear()
        
        x = e.mod_output(x)
        x = e.mod_input(x)
        
        if args.verbose:
            print(out, '----', x, '----', sep="\n")
        if e.detect_input_post_query(x) or e.detect_input_post_query(out):
            z = e.set_input_post_query(x) ## x ??
            if args.verbose:
                print(e.exchange['post_query'], ':post_query')
                print(z, 'obj out')
                if z != None:
                    print(z.settings)
        #print(num, "num")
        #e.get_status()
        num += 1 
        #if args.timer:
        #    event.clear()

