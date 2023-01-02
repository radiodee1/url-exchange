#!/usr/bin/python3

import argparse

class Exchange:
    def __init__(self):
        self.exchange = {}
        self.dict_name = ""
        self.text_name = ""

    def save_dict(self):
        pass 

    def load_dict(self):
        pass

    def load_txt(self):
        if self.text_name == "" or self.text_name == None:
            return
        print("load", self.text_name)
        pass

    def set_dict_name(self, dict_name):
        self.dict_name = dict_name;

    def set_text_name(self, text_name):
        self.text_name = text_name


if __name__ == '__main__':
    e = Exchange()
    parser = argparse.ArgumentParser(description="URL Exchange", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dict_name', default='./../data/dict.txt', help='name for "dictionary" input file.')
    parser.add_argument('--text_name', help='name for additional "tsv" input file.')
    args = parser.parse_args()

    print(args.text_name)
    print(args.dict_name)

    e.set_dict_name(args.dict_name)

    e.load_dict()
    if args.text_name != None:
        e.set_text_name(args.text_name)
        e.load_txt()
