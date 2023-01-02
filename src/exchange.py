#!/usr/bin/python3

import argparse

class Exchange:
    def __init__(self):
        self.exchange = {}
        self.pre_query = {} 
        self.dict_name = ""
        self.text_name = ""
        self.wizard = ['radio', 'timer']
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
        pass

    def load_wizards(self):
        for x in self.wizard:
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

    def set_extra_wizards(self, wizards):
        w = wizards.split(',')
        for x in w:
            if x.strip() not in self.wizard:
                self.wizard.append(x.strip())
        if self.verbose:
            print(self.wizard)


if __name__ == '__main__':
    e = Exchange()
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dict_name', default='./../data/dict.txt', help='name for "dictionary" input file.')
    parser.add_argument('--text_name', help='name for additional "csv" input file.')
    parser.add_argument("--wizards", default="radio,timer", help="comma sep list of possible wizards - added to current list.")
    parser.add_argument("--verbose", action="store_true", help="show debugging output.")
    parser.add_argument("--update", action="store_true", help="do not skip updating exchange on exit.")
    args = parser.parse_args()

    if args.verbose:
        print(args.text_name)
        print(args.dict_name)

    e.set_verbose(args.verbose) 
    e.set_dict_name(args.dict_name)
    e.set_extra_wizards(args.wizards)
    e.set_update_on_exit(args.update)

    e.load_dict()
    if args.text_name != None:
        e.set_text_name(args.text_name)
        e.load_txt()

    e.load_wizards()

    e.save_dict()
