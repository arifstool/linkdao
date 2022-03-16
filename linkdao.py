#!/usr/bin/python

__author__ = "ARiF"
__copyright__ = ""
__license__ = "GPL"
__version__ = "1.0.2"
__email__ = "arifsnoor@gmail.com"
__status__ = ""

import re, getopt
import sys
import os

def uses():
    print(''' 
    Simple url extractor | Under development

    options:
    -i input file
    -o output file
    -d specific domain (BETA)
    -h, --help help menu
    -x provides only domain
    -v verbose
    
    example: linkdoa.py -i vksl.txt -d google.com -x

    ISSUE: 
        There is a problem in domain name validator. You can use only a specific format 
        to provide -d 
         
        valid format for domain:
        -d domain_name.top_level.domain.country_domain

    ''')


def domainextractor(domain):
    domain_name = tld = country_domain = subdomain = None
    domains = domain.split(".")
    if len(domains) == 1:
        domain_name = domains[0]
    elif len(domains) == 2:
        domain_name = domains[0]
        tld = domains[1]
    elif len(domains) == 3:
        domain_name = domains[0]
        tld = domains[1]
        country_domain = domains[2]
    elif len(domains) == 4:
        subdomain = domains[0]
        domain_name = domains[1]
        tld = domains[2]
        country_domain = domains[3]
    else:
        print("linkdaoERROR: Failed to extract domain name| function 'domainextractor'")
        exit()

    return subdomain, domain_name,  tld, country_domain, len(domains)


def linkdao(inp_file, out_file, domain_provided, domain, domain_only, isverbose):
    if isverbose:
        print("Loading file")
    txt_file = open(inp_file)
    text = txt_file.read()

    extn = '(/\S+)?'
    #INCLUDE ALL THE PROTOCOLS ////////////////////// HERE  
    protocol = r'(https?://)?' 

    if domain_only:
        extn = ''

    # IF DOMAIN PROVIDED
    if domain_provided:

        subdomain, domain_name,  tld, cd, domain_count = domainextractor(
            domain)

        if subdomain == None:
            subdomain = r'[a-z0-9-]+'
        if domain_name == None:
            domain_name = r'[0-9a-z-]+'
        if tld == None:
            tld = r'[a-z0-9]+'
        if cd == None:
            cd = '[a-z]{2}'

        pattern = re.compile(
            protocol+r'(www\.)?'+'('+subdomain+'\.)?'+domain_name+'\.'+tld+'(\.'+cd+')?'+extn)

    else:
        pattern = re.compile(
            protocol+r'(www\.)?([a-z0-9-]+\.)?[0-9a-z-]+\.[a-z0-9]+(\.[a-z]{2})?'+extn)

    if not os.path.exists(out_file):
        with open(out_file, 'a') as wf:
            matches = pattern.finditer(text)
            if isverbose:
                print("Fetching urls...")
            for match in matches:
                if isverbose:
                    print(match.group(0))
                wf.write(match.group(0) + '\n')
            wf.close()
    else:
        print("linkdaoError: Output file already exists | error Function: linkdao")
        exit()
    txt_file.close()
    return "Process Completed"


def arghandeler(argumets):
    inp_file = None
    out_file = None
    domain_provided = False
    domain = "example.com"
    domain_only = False
    isverbose = False
    try:
        opts, args = getopt.getopt(argumets, "d:hi:o:vx", [
                                   "domain=", "domain-only", "help", "inpfile=", "outfile=", "--verbose"])
    except getopt.GetoptError as err:
        print("problem\n\n"+err)
        # print help
        sys.exit(2)

    for o, a in opts:
        if o == "-h" or o == "--help":
            uses()
            sys.exit()
        elif o in ("-i", "--inpfile"):
            inp_file = a

        elif o in ("-d", "--domain"):
            domain = a
            # domain_valider()///////////////////////////HERE
            domain_provided = True
        elif o in ("-o", "--outfile"):
            out_file = a
            if os.path.exists(out_file):
                print(f"{out_file} already exists. Try using different name")

        elif o in ("-x", "--domain-nly"):
            domain_only = True

        elif o in ("-v", "--verbose"):
            isverbose = True
        else:
            print("linkdaoEroor:unknown option | function: arghandeler")

    if inp_file == None:
        print("Input File not provided")
        uses
        exit()

    if out_file == None:
        out_file = inp_file+"-urls"
        n = 0
        while os.path.exists(f"{out_file}.txt"):
            out_file += f"({n+1})"
        out_file += ".txt"

    return inp_file, out_file, domain_provided, domain, domain_only, isverbose


def main():
    arguments_provided = sys.argv[1:]
    inp_file, out_file, domain_provided, domain, domain_only, isverbose = arghandeler(
        arguments_provided)

    result = linkdao(inp_file, out_file, domain_provided,
                     domain, domain_only, isverbose)
    print(result)


if __name__ == "__main__":
    main()
