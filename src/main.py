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

e = Exchange()


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
        max_tokens=15,
        temperature=0
    )
    output = completion.choices[0].text 
    #print(output)
    return output


if  __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument('--dict_name', default='./../data/dict.pickle', help='name for "dictionary" json input file.')
    parser.add_argument('--gptj',action='store_true', help='use gptj instead of gpt3.')
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument("--path", default="./../data/", help="default data directory")
    args = parser.parse_args()

    e.set_verbose(args.verbose)
    
    e.load()
    
    e.set_path(args.path)
   
    query = get_gpt3
    if args.gptj:
        query = get_gpt 

    e.set_query_cmd(query) ## input or get_gpt
 
    print("URL Exchange")
    while True:
        x = input("> ")

        XPREPENDX = PREPEND['include-url']
        #print("--Main--", XPREPENDX)

        xx = XPREPENDX + "\n\nHuman: " + x.strip() + "\nJane: "
        if args.verbose:
            print('--xxx--', x, '--xxx--', sep="\n")
        #i = e.mod_input(x)
        if args.verbose:
            print(x)
        #z = e.set_input_post_query(x)
        #x = e.mod_input(x) 
        out = query(xx)
        out = e.mod_output(out)
        print(out) # ':out')
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
        e.get_status()

