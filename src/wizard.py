#!/usr/bin/python3

import argparse
import copy
import dill as pickle
import time
from word2number import w2n 
import string

from prepend import PREPEND

class Wizard:
    def __init__(self):
        self.active = False
        self.is_silent = True 
        self.ident_ai = "Jane"
        self.ident_human = "Human"
        self.commands = []
        #self.process = None 
        #self.query = None 
        self.line_in = ''
        self.key = ''
        self.print = None
        self.input = None
        self.settings = { }
        self.status = {'RUNNING':0, 'DONE':1, 'DESTROY':2, 'GOOD':3, 'BAD':4}
        self.XPREPENDX = PREPEND['include-no-url'] 
        self.use_prepend = False

        #print("--Wizard--", self.XPREPENDX)

    def set_process_cmd(self, p): ## what for??
        self.process = p          ## what for?? 

    def set_query_cmd(self, q):
        self.query = q

    def set_print_cmd(self, p):
        self.print = p

    def set_input_cmd(self, i):
        self.input = i 

    def set_line(self, line):
        if not self.use_prepend:
            line = line.replace(self.ident_ai, '').replace(self.ident_human, "")
            line = line.replace(":", '')
            #print(line)
        self.line_in = line 

    def set_key(self, key):
        self.key = key 

    def set_active(self, a):
        self.active = a 

    def set_prepend(self, p):
        self.XPREPENDX = p

    def set_identity(self, jane="Jane", human="Human"):
        self.ident_ai = jane
        self.ident_human = human 

    def load_commands(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith('#') or line.strip() == "":
                continue
            part = line.strip().split(";")
            if len(part) > 1:
                self.commands.append([part[0].strip(), part[1].strip()]) 
        pass
        
    def loud(self):
        for i in self.commands:
            self.print(i[0].strip()) ## print the question
            x = self.input("> ")     ## wait for the answer
            self.settings[i[1].strip()] = x.strip() 
        self._set_time()
        pass 

    def silent(self):
        for i in self.commands:
            if len(i) > 1:
                if self.use_prepend:
                    x = self.XPREPENDX + self.line_in + ". " + i[0].strip() + "\nJane: "
                else:
                    x =  "Q: " + self.line_in + ". " + i[0].strip() + "\nA: "
                #print("???", x, "???", sep="\n")
                x = self.query(x)
                x = self.mod_output(x)
                x = self.mod_input(x)
                if i[1].strip().lower() == 'length':
                    pass
                    if self.use_prepend:
                        x = x.translate(str.maketrans("", "", string.punctuation))
                    try:
                        ## if x is a number, try to convert to int or int in string
                        words = w2n.word_to_num(x.split(" ")[0].strip())
                        x = str(words)
                    except:
                        pass ## not everything should be a number...
                
                x = x.translate(str.maketrans("", "", string.punctuation))
                self.settings[i[1].strip().lower()] = x.strip().lower() 
        self._set_time()
        pass

    def _set_time(self):
        #now = date.now()
        seconds = time.time()
        #print(seconds)
        self.settings['start-seconds'] = seconds
        self.settings['status'] = self.status['RUNNING']

    def process(self):
        return input

    def get_status(self):
        r = ''
        for i in self.status:
            if self.settings['status'] == self.status[i] :
                self.settings['status-readable'] = i 
                r = i
        #print(r, self.settings)
        return r 
        

    def query(self, input):
        return input

    def mod_input(self, i):
        ## possible multi-line input 
        if len(i) > 0:
            i = i.strip().split("\n")[-1]
            ## possible header before desired text 
            ii = ""
            y = 0
            for x in i.split(' '):
                if not x.endswith(":"):
                    ii = ii + " " + x
                elif y == 1:
                    ii = ""
                y += 1
            i = ii.strip() 
        return i
        pass

    def mod_output(self, i):
        ## assume single word output 
        if len(i) > 0:
            i = i.strip().split("\n")[0] ## pick first sentence
            #i = i.strip().split(" ")[0]  ## pick first word
        return i
        pass 


class Timer(Wizard):
    def __init__(self):
        super().__init__()
        self.key = 'timer'
        self.is_silent = True
        self.use_prepend = False

    def process(self):
        super().process()
        seconds = time.time()
        len = 0
        num = None
        try:
            num = float(self.settings['length'].split(" ")[0].strip()) 
        except:
            num = None
            pass 
        if num == None:
            try:
                words = w2n.word_to_num(self.settings['length'].split(" ")[0].strip())
                num = float(words)
                len = num * 60 
            except :
                num = 1 
                len = 60 
                self.settings['length'] = str(num)
                pass
        else:
            len = num * 60
        if seconds > self.settings['start-seconds'] + len :
            self.settings['status'] = self.status['DONE']
            self.settings['seconds-left'] = 0 
        else:
            self.settings['seconds-left'] = self.settings['start-seconds'] + len - seconds


class Radio(Wizard):
    def __init__(self):
        super().__init__()
        self.key = 'radio'
        self.is_silent = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Wizard Objects", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    args = parser.parse_args()

