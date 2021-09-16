from bs4 import BeautifulSoup as Soup
import sys
import requests
import urllib3
import argparse

def gethtml(url, headers = None, retry = True):
    urllib3.disable_warnings()
    try:
        if headers is None:
            headers = {}
        html = requests.get(url, headers = headers, verify=False)
        if (html.status_code != 200):
            print('could not retrieve url {}'.format(url))
            return None
        html = html.content
    except Exception as e:
        if retry:
            html = gethtml("https://{}".format(url), headers = headers, retry = False)
            if html is None:
                html = gethtml("http://{}".format(url), headers = headers, retry = False)
        else:
            print('could not retrieve url {}'.format(sys.argv[1]))
            return None
    return html

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", dest="filename", default=None, help="file to read (default: stdin)")
    parser.add_argument("-u", "--url", action="store", dest="url", default=None, help="url to parse (it will be downloaded and queried); it is incompatible with the use of a file")
    parser.add_argument("-U", "--user-agent", action="store", dest="user_agent", default=None, help="use an user agent string to get the web page from the URL")
    parser.add_argument("-a", "--attr", action="append", dest="attribute", default=None, help="attributes to get from the html tags (the whole tag if not provided); may appear more than once", type=str)
    parser.add_argument("-r", "--rm", action="append", dest="rmquery", default=None, help="query string of elements to remove on each element found; may appear more than once", type=str)
    parser.add_argument("-s", "--separator", action="store", dest="separator", default="\0", help="character (or characters) used to separate the different results from the query (not the fields in a result) (default: 0 char)", type=str)
    parser.add_argument("-S", "--field-separator", action="store", dest="fieldseparator", default=",", help="character (or characters) used to separate the value of the different attributes of an entry resulting from the query (default: ,)", type=str)
    parser.add_argument("-n", "--no-empty-lines", action="store_true", dest="noemptylines", default=False, help="omits the empty resulting entries (i.e. those equal to \"\"")
    parser.add_argument("-N", "--no-empty-attr", action="store_true", dest="noemptyattr", default=False, help="omits the empty values of attributes (i.e. those equal to \"\"")
    parser.add_argument("-1", "--only-first", action="store_true", dest="onlyfirst", default=False, help="if multiple entries are found in the html document, show only the first one")
    parser.add_argument("query", help="query string for the html content", type=str)
    args = parser.parse_args()

    # The default behaviour is to read from stdin
    if args.url is None and args.filename is None:
        args.filename = "-"

    # It cannot be both a file and an url; if so, deactivate the url
    if args.url is not None and args.filename is not None:
        print("cannot parse both a file and a url. Only the file will be parsed")
        args.url = None

    # If it is an url, retrieve it
    if args.url is not None:
        headers = {}
        if args.user_agent is not None:
            headers["User-Agent"] = args.user_agent

        html = gethtml(args.url, headers, True)
        if html is None:
            print("failed to get url {}".format(args.url))
            sys.exit(-1)

    # This enables parsing backslashes in python 3 (e.g. \n)
    args.separator = args.separator.encode("utf-8").decode('unicode-escape')
    args.fieldseparator = args.fieldseparator.encode("utf-8").decode('unicode-escape')

    # If it is a file, read it
    if args.filename is not None:
        if args.filename == '-':
            html = b''.join(sys.stdin.buffer.readlines())
        else:
            try:
                html = b''.join(open(args.filename, "rb").readlines())
            except:
                print("failed to open file {}".format(args.filename))
                sys.exit(-1)

    # We accept multiple attributes as a list of comma separated
    if args.attribute is not None:
        args.attribute = [ b.strip() for a in args.attribute for b in a.split(',') ]

    # If there is no query, there is no result
    if args.query is None:
        print("no query introduced")
        sys.exit(0)

    # If there is no html, there is no job
    if html is None:
        print("no input found in stdin")
        sys.exit(1)

    try:
        soup = Soup(html, "html5lib")

        # We'll select elements using the query
        wpmeta = soup.select(args.query)

        # If we only want the first result, let's omit the rest
        if args.onlyfirst and len(wpmeta) > 0:
            wpmeta = [ wpmeta[0] ]

        # If wanted to remove parts of the results... let's remove them
        if args.rmquery is not None:
            for w in wpmeta:
                for rm in args.rmquery:
                    m = w.find(rm)
                    if m is not None: m.decompose()

        # If no args requested, we want the whole html tag
        if args.attribute is None:
            result = [ str(w) for w in wpmeta ]
        else:
            # Otherwise process the parameters
            result = []
            for w in wpmeta:

                result_i = []
                for a in args.attribute:
                    r = None
                    if a == '.':
                        r = w.string
                    else:
                        if w.has_attr(a):
                            r = w[a]

                    if isinstance(r, list): r = " ".join(r)
                    if r is None: r = ""
                    result_i.append(r)

                # Remove emtpy attrs if requested
                if args.noemptyattr: result_i = [ x for x in result_i if x != "" ]
                result.append(args.fieldseparator.join(result_i))

        # Remove empty lines if requested
        if args.noemptylines: result = [ x for x in result if x != "" ]
        print(args.separator.join(result))

    except Exception as e:
        print("failed to parse or query html input")
        sys.exit(1)
