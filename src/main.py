#!/usr/bin/python3 

print("here...")

from exchange import Exchange 

import codecs
import argparse
import sys
import os 
import json 
import openai

from pipeline import PipelineCloud


e = Exchange()

# i = e.mod_input("hi there...")


PREPEND = '''{human}: Turn on classic radio.
{jane}: Set radio http://radio 

{human}: Set a timer for five minutes.
{jane}: Set timer http://timer 

{human}: Hi?
{jane}: Hello there.

{human}: Do you like candy?
{jane}: Yes I like candy.

{human}: What is your favorite color?
{jane}: My favorite color is blue.

{human}: How old are you?
{jane}: I am 21 years old.'''.format(human="Human", jane="Jane")


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
    print(output)
    return output


if  __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument('--dict_name', default='./../data/dict.pickle', help='name for "dictionary" json input file.')
    #parser.add_argument('--text_name', help='name for additional "csv" input file.')
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument("--path", default="./../data/", help="default data directory")
    args = parser.parse_args()

    e.set_verbose(True)
    #e.build_objects()
    e.load()
    #e.set_verbose(False)
    e.set_path(args.path)
    e.set_query_cmd(get_gpt3) ## input or get_gpt
    
    print("URL Exchange")
    while True:
        x = input("> ")

        xx = PREPEND + "\n\nHuman: " + x.strip() + "\nJane: "
        print('--xxx--', x, '--xxx--', sep="\n")
        #i = e.mod_input(x)
        if args.verbose:
            print(x)
        #z = e.set_input_post_query(x)
        #x = e.mod_input(x) 
        out = get_gpt3(xx)
        out = e.mod_output(out)
        print(out)
        x = e.mod_output(x)
        x = e.mod_input(x)
        print(out, '----', x, '----', sep="\n")
        z = e.set_input_post_query(x)
        print(e.exchange['post_query'])
        print(z, 'obj out')
        if z != None:
            print(z.settings)

