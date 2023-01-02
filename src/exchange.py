#!/usr/bin/python3

import argparse

class Exchange:
    def __init__(self):
        self.exchange = {}
        self.exchange["pre_query"] = {}
        self.exchange["post_query"] = {}
        self.exchange['wizard-silent'] = {}
        self.exchange['wizard-loud'] = {}
        self.dict_name = ""
        self.text_name = ""
        self.wizards_silent = ['radio', 'timer']
        self.wizards_loud = []
        self.verbose = False
        self.update = False 

    def save_dict(self):
        if self.update == False:
            return 
        pass 

    def load_dict(self):
        pass

    def load_txt(self):
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
                elif x[2].strip() == "wizard-loud":
                    self.exchange['wizard-loud'][x[1].strip()] = {} 
                    self.exchange['wizard-loud'][x[1].strip()]['name'] = x[1].strip()
                    
        if self.verbose:
            print(self.exchange)
        pass

    def load_wizards(self):
        for x in self.wizards_silent:
            if self.verbose:
                print("load wizard", x)

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



if __name__ == '__main__':
    e = Exchange()
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dict_name', default='./../data/dict.txt', help='name for "dictionary" input file.')
    parser.add_argument('--text_name', help='name for additional "csv" input file.')
    parser.add_argument("--wizards_loud", default="", help="comma sep list of possible loud wizards - added to current list.")
    parser.add_argument("--wizards_silent", default="radio,timer", help="comma sep list of possible silent wizards - added to current list.")
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument("--update", action="store_true", help="do not skip updating exchange on exit.")
    args = parser.parse_args()

    if args.verbose:
        print(args.text_name)
        print(args.dict_name)

    e.set_verbose(args.verbose) 
    e.set_dict_name(args.dict_name)
    e.set_extra_wizards_silent(args.wizards_silent)
    e.set_extra_wizards_loud(args.wizards_loud)
    e.set_update_on_exit(args.update)

    e.load_dict()
    if args.text_name != None:
        e.set_text_name(args.text_name)
        e.load_txt()

    e.load_wizards()

    e.save_dict()
