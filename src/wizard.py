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
        self.blacklist_words = []
        self.whitelist_words = []
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
            elif len(part) == 1 and part[0].startswith('blacklist:'):
                self.blacklist_words = part[0].lower().split(':')[1].strip().split(',')
                self.blacklist_words = [ x.strip() for x in self.blacklist_words ]
                print(self.blacklist_words, 'blacklist')
            elif len(part) == 1 and part[0].startswith('whitelist:'):
                self.whitelist_words = part[0].lower().split(':')[1].strip().split(',')
                self.whitelist_words = [ x.strip() for x in self.whitelist_words ]
                print(self.whitelist_words, 'whitelist')
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
                for z in self.blacklist_words:
                    self.line_in = self.line_in.replace(z,'')
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

    def start(self, x):
        ## launch a program or something ##
        pass 

    def finish(self, x):
        ## launch a program or something ##
        pass

    def may_delete_neighbor(self, x):
        delete = False
        if x.key == self.key and 'off_flag' in self.settings and 'off_flag' in x.settings and x.settings['off_flag'] != self.settings['off_flag']:
            if x.key == 'radio':
                delete = True
            elif 'name' in self.settings and 'name' in x.settings and x.settings['name'] == self.settings['name']:
                delete = True
        return delete

    def may_replace_neighbor(self, x):
        replace = False 
        if self.key == x.key and 'type' in self.settings and 'type' in x.settings and self.settings['type'] != x.settings['type']:
            replace = True 
        elif 'name' in self.settings and 'name' in x.settings and self.settings['name'] == x.settings['name'] and self.key == 'timer' and x.key == 'timer':
            replace = True 
        return replace 

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

class Switch(Wizard):
    def __init__(self):
        super().__init__()
        self.key = 'switch'
        self.is_silent = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Wizard Objects", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument('--prepare', action="store_true", help='write empty launch scripts.')
    parser.add_argument('--path', default='../data/', help='use this project path.')
    args = parser.parse_args()
    
    if args.prepare:
        obj_list = [ Radio, Switch ]
        for j in obj_list:
            j_obj = j()
            j_filename = args.path + "/wiz-" + j_obj.key.lower() + ".txt" 
            
            j_obj.load_commands(j_filename)
            print(j_obj.whitelist_words)
            for k in j_obj.whitelist_words:
                script_pos = args.path  + "/" + j_obj.key.lower() + "_posotive_" + k + ".sh"
                script_neg = args.path  + "/" + j_obj.key.lower() + "_negative_" + k + ".sh"
                print(k)
                for f in [ script_pos, script_neg ]:
                    ff = open(f, 'w')
                    ff.write(   '''#!/bin/bash
                                
                                echo "Launch Script"
                                echo $@ 
                                # curl 
                                # ping www.google.com 
                                ''')
                    ff.close()
                pass 
        pass 

