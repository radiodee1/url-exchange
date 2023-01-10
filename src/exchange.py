#!/usr/bin/python3

import argparse
import copy
import dill as pickle


class Wizard:
    def __init__(self):
        self.active = False
        self.is_silent = True 
        self.commands = []
        #self.process = None 
        #self.query = None 
        self.line_in = ''
        self.key = ''
        self.print = None
        self.input = None
        self.settings = { }
        self.PREPEND = '''{human}: Hi?
{jane}: Hello there.

{human}: Do you like candy?
{jane}: Yes I like candy.

{human}: What is your favorite color?
{jane}: My favorite color is blue.

{human}: How old are you?
{jane}: I am 21 years old.

{human}: '''.format(human="Human", jane="Jane")


    def set_process_cmd(self, p): ## what for??
        self.process = p          ## what for?? 

    def set_query_cmd(self, q):
        self.query = q

    def set_print_cmd(self, p):
        self.print = p

    def set_input_cmd(self, i):
        self.input = i 

    def set_line(self, line):
        self.line_in = line 

    def set_key(self, key):
        self.key = key 

    def set_active(self, a):
        self.active = a 

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
        pass 

    def silent(self):
        for i in self.commands:
            if len(i) > 1:
                x = self.PREPEND + self.line_in + ". " + i[0].strip() + " "
                #x =  self.line_in + ". " + i[0].strip() + " "
                print("???", x, "???", sep="\n")
                x = self.query(x)
                x = self.mod_output(x)
                x = self.mod_input(x)
                self.settings[i[1].strip()] = x.strip() 
        pass

    def process(self, input):
        return input

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


class Radio(Wizard):
    def __init__(self):
        super().__init__()
        self.key = 'radio'
        self.is_silent = True


class Exchange:
    def __init__(self):
        self.exchange = {}
        self.exchange["pre_query"] = {}
        self.exchange["post_query"] = {}
        self.exchange['wizard-silent'] = {}
        self.exchange['wizard-loud'] = {}
        self.dict_name = "./../data/dict.pickle"
        self.text_name = "./../data/dict.csv"
        self.wizards_silent = ['radio', 'timer']
        self.wizards_loud = []
        self.verbose = False
        self.update = False 
        self.query = None
        self.classes = []
        self.path = "./../data/"

    def save_dict(self):
        if self.update == False:
            return
        #print(self.exchange)
        f = open(self.dict_name, 'wb')
        pickle.dump(self.exchange, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        pass 

    def _load_dict(self):
        f = open(self.dict_name, 'rb')
        self.exchange = pickle.load(f)
        f.close()
        #print(self.exchange)
        pass

    def _build_objects(self):
        for i in self.wizards_silent:
            if self.verbose:
                print(i)
            self.exchange['wizard-silent'][i.strip()] = {}
            self.exchange['wizard-silent'][i.strip()]['name'] = i.strip()

            wizard = self._choose_silent(i.strip())
            self.exchange['wizard-silent'][i.strip()]['object'] = wizard
            self.exchange['wizard-silent'][i.strip()]['object'].set_key(i.strip())
            self._load_wizard(wizard) 
        for i in self.wizards_loud:
            self.exchange['wizard-loud'][i.strip()] = {} 
            self.exchange['wizard-loud'][i.strip()]['name'] = i.strip()
            self.exchange['wizard-loud'][i.strip()]['object'] = Wizard()
            self.exchange['wizard-loud'][i.strip()]['object'].set_key(i.strip())
        pass 

    def _load_txt(self):
        if self.text_name == "" or self.text_name == None:
            return
        if self.verbose:
            print("load", self.text_name)
        f = open( self.text_name, "r") 
        lines = f.readlines()
        for i in lines:
            if i.strip().startswith("#") or i.strip() == "":
                continue
            x = i.split(";")
            if x[0].strip().startswith("["):
                self.exchange["pre_query"][x[0].strip()] = x[1].strip()
            else:
                self.exchange["post_query"][x[0].strip()] = x[1].strip()
                if x[2].strip() == "wizard-silent":
                    self.exchange['wizard-silent'][x[1].strip()] = {}
                    self.exchange['wizard-silent'][x[1].strip()]['name'] = x[1].strip()

                    wizard = self._choose_silent(x[1].strip())
                    self.exchange['wizard-silent'][x[1].strip()]['object'] = wizard
                    self.exchange['wizard-silent'][x[1].strip()]['object'].set_key(x[1].strip())
                    self._load_wizard(wizard) 
                elif x[2].strip() == "wizard-loud":
                    self.exchange['wizard-loud'][x[1].strip()] = {} 
                    self.exchange['wizard-loud'][x[1].strip()]['name'] = x[1].strip()
                    self.exchange['wizard-loud'][x[1].strip()]['object'] = Wizard()
                    self.exchange['wizard-loud'][x[1].strip()]['object'].set_key(x[1].strip())

        if self.verbose:
            print(self.exchange)
        pass

    def _choose_silent(self, xx):
        wizard = None 
        if xx == "timer":
            wizard = Timer()
        elif xx == "radio":
            wizard = Radio()
        elif xx == "username":
            wizard = Wizard()
        elif xx == "ainame":
            wizard = Wizard()
        else:
            wizard = Wizard()
            pass
        if self.verbose:
            print(wizard.key, ":key")
        return wizard
        pass

    def _get_wizard_path(self, w):
        x = self.path + "/wiz-" + w + ".txt"
        return x 

    def _load_wizard(self, obj ):
        x = obj.key 
        xx = self._get_wizard_path(x)
        obj.load_commands(xx)
        if self.verbose:
            print("load wizard", x)
            print(obj.commands, ":commands", xx)

    def load(self):
        if self.update:
            self._build_objects()
            #if self.text_name != None:
            self._load_txt()
            pass
        else:
            self._load_dict()
            pass 

    def set_path(self, p):
        self.path = p

    def set_verbose(self, v):
        self.verbose = v

    def set_update_on_exit(self, update):
        self.update = update

    def set_dict_name(self, dict_name):
        self.dict_name = dict_name;

    def set_text_name(self, text_name):
        self.text_name = text_name

    def set_extra_wizards_silent(self, wizards):
        w = wizards.split(',')
        for x in w:
            if x.strip() not in self.wizards_silent and x.strip() != "":
                self.wizards_silent.append(x.strip())
        if self.verbose:
            print(self.wizards_silent)

    def set_extra_wizards_loud(self, wizards):
        w = wizards.split(',')
        for x in w:
            if x.strip() not in self.wizards_loud and x.strip() != "":
                self.wizards_loud.append(x.strip())
        if self.verbose:
            print(self.wizards_loud)

    def set_query_cmd(self, q):
        self.query = q
        for xx in self.exchange['wizard-silent']:
            self.exchange['wizard-silent'][xx]['object'].set_query_cmd(self.query)

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

    def set_input_post_query(self, i):
        for x in self.exchange['post_query']:
            xx = self.exchange['post_query'][x].strip()
            if self.verbose:
                print(x, self.exchange['post_query'][x], xx , ':tag')
            if xx in i.lower() or x in i.lower():
                if xx.strip() in self.exchange['wizard-silent']:
                    key = self.exchange['wizard-silent'][xx]['object']
                if xx.strip() in self.exchange['wizard-loud']:
                    key = self.exchange['wizard-loud'][xx]['object']
                w = copy.copy(key)
                #w.set_key(key)
                w.set_line(i)
                if w.is_silent:
                    w.silent()
                elif not w.is_silent:
                    w.loud()
                if self.verbose:
                    print(w.settings)
                return w
        return None 
        pass 

    def set_input_pre_query(self, i):
        for x in self.exchange['pre_query']:
            if x in i:
                i = i.replace(x, self.exchange['pre_query'][x])
        if self.verbose:
            print(i, ": input after pre_query")
        return i.strip() 

    def get_status(self):
        return ""

if __name__ == '__main__':
    e = Exchange()
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dict_name', default='./../data/dict.pickle', help='name for "dictionary" json input file.')
    parser.add_argument('--text_name', help='name for additional "csv" input file.')
    parser.add_argument("--wizards_loud", default="", help="comma sep list of possible loud wizards - added to current list.")
    parser.add_argument("--wizards_silent", default="radio,timer", help="comma sep list of possible silent wizards - added to current list.")
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument("--update", action="store_true", help="do not skip updating exchange on exit.")
    parser.add_argument("--path", default="./../data/", help="default data directory")
    args = parser.parse_args()


    e.set_verbose(args.verbose) 
    e.set_dict_name(args.dict_name)
    e.set_extra_wizards_silent(args.wizards_silent)
    e.set_extra_wizards_loud(args.wizards_loud)
    e.set_update_on_exit(args.update)
    e.set_path(args.path)

    
    
    if args.text_name != None:
        e.set_text_name(args.text_name)
        

    e.load()
    z = e.set_input_pre_query("some text here from [http://ai-name].")

    if args.verbose:
        print(z)

    e.set_query_cmd(input)

    i = e.mod_input("Human : some text here for http://timer here.")
    if args.verbose:
        print(i)
    z = e.set_input_post_query(i)
    
    if args.verbose and z != None:
        print(z.key, type(z))
    e.save_dict()
