#!/usr/bin/python3 

print("here...")

from exchange import Exchange 

import codecs
import argparse
import sys
import os 
import json 

from pipeline import PipelineCloud


e = Exchange()

i = e.mod_input("hi there...")

print(i)
print(e)

PREPEND = '''{human}: Hi?
{jane}: Hello there.

{human}: Do you like candy?
{jane}: Yes I like candy.

{human}: What is your favorite color?
{jane}: My favorite color is blue.

{human}: How old are you?
{jane}: I am 21 years old.'''.format(human="Human", jane="Jane")


def get_gpt(question):
    prompt = PREPEND + "\n\nHuman: " + question.strip() + "\nJane: "
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
                "top_k": 50
            },
        ],
    )
    
    output = run["result_preview"][0][0]
    return output


