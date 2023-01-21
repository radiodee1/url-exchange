#!/usr/bin/python3 



from exchange import Exchange 
import argparse
import os 
import openai
from pipeline import PipelineCloud
import time
from word2number import w2n
import string
import json 
from prepend import PREPEND
from threading import Thread, Event


e = Exchange()



def add_to_q_history(h, HISTORY):
    HISTORY += "\n\nHuman: " + h
    return HISTORY

def add_to_a_history(h, HISTORY):
    HISTORY += "\nJane: " + h
    return HISTORY

def get_gpt(question):
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
    return output

def get_status_thread():
    num = 0 
    while True:
        if not event.is_set():
            time.sleep(20)
            #print(num, 'thread', end=' ')
            if not event.is_set():
                out = e.get_status()
                print(out)
                num += 1 
            #print("*> ", end='')
        pass 


if  __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--timer', action='store_true', help='Use timer for wizard output.')
    parser.add_argument('--gptj',action='store_true', help='use gptj instead of gpt3.')
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument("--path", default="./../data/", help="default data directory")
    args = parser.parse_args()
    
    event = Event()

    if args.timer:
        t1 = Thread(target=get_status_thread)
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
    while True:
        #event.set()
        x = input("> ")
        if args.timer:
            event.set()
        XPREPENDX = PREPEND['include-url']
        #print("--Main--", XPREPENDX)
        XPREPENDX += HISTORY
        xx = XPREPENDX + "\n\nHuman: " + x.strip() + "\nJane: "
        HISTORY = add_to_q_history(x, HISTORY)

        if args.verbose:
            print('--xxx--', xx, '--xxx--', sep="\n")
        #i = e.mod_input(x)
        if args.verbose:
            print(x)
        #z = e.set_input_post_query(x)
        #x = e.mod_input(x) 
        out = query(xx)
        if args.verbose:
            print("--- long list ---", out, "--- end ---", sep="\n")
        out = e.mod_output(out)
        HISTORY = add_to_a_history(out, HISTORY)
        print(out) 
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
        if args.timer:
            event.clear()

