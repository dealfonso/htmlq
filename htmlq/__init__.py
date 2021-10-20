import sys
import argparse
from .version import VERSION
import string, random
import re

# This function tryes different methods to download the web page
def gethtml(url, headers = None, retry = True):

    # Delay importing libraries
    import urllib3
    import requests

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

# This class simply stores the variable name using our format
class StoreVar(argparse._AppendAction):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, nargs=1, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, "%#{}#".format(values[0]), option_string)

# The funcion explodes the variables and its values from a query string, and returns them as a dictionary
def getvars(q):
    vars = {}
    if q is None: return vars
    varvalues = q.split('&')
    for vv in varvalues:
        vv = vv.split('=') + [ "" ]
        vars[vv[0]] = vv[1]
    return vars

# Shorthand to print "" is value is none
def nprint(v):
    print("" if v is None else v)

# Shorthand to return "" is value is none
def rprint(v):
    return ("" if v is None else v)

# A simple id generator; returns a string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "<{}>".format(''.join(random.choice(chars) for _ in range(size)))

# The main function for urlf command
def urlf():
    # Delay importing libraries
    from urllib.parse import urlparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-U", "--url", action="append_const", const="%U", dest="format", help="the input url as is")
    parser.add_argument("-s", "--scheme", action="append_const", const="%s", dest="format", help="shows the scheme of the url (e.g. https)")
    parser.add_argument("-u", "--username", action="append_const", const="%u", dest="format", help="shows the username to accede to the url (i.e. user in https://user@pass:myserver.com)")
    parser.add_argument("-w", "--password", action="append_const", const="%w", dest="format", help="shows the password to accede to the url (i.e. pass in https://user@pass:myserver.com)")
    parser.add_argument("-H", "--hostname", action="append_const", const="%H", dest="format", help="shows the hostname in the url (i.e. myserver.com in https://myserver.com/my/path)")
    parser.add_argument("-p", "--port", action="append_const", const="%p", dest="format", help="shows the port in the url (i.e. 443 in https://myserver.com:443/my/path)")
    parser.add_argument("-P", "--path", action="append_const", const="%P", dest="format", help="shows the path in the url (i.e. my/path in https://myserver.com/my/path)")
    parser.add_argument("-q", "--query", action="append_const", const="%q", dest="format", help="shows the query in the url (i.e. q=1&r=2 in https://myserver.com/my/path?q=1&r=2)")
    parser.add_argument("-m", "--parameters", action="append_const", const="%m", dest="format", help="shows the parameters to accede to the url (i.e. param in https://myserver.com/my/path;param?q=1&r=2)")
    parser.add_argument("-f", "--fragment", action="append_const", const="%f", dest="format", help="shows the fragment in the url (i.e. sec1 in https://myserver.com/my/path#sec1)")
    parser.add_argument("-v", "--var", action=StoreVar, metavar="var name", dest="format", help="show the value of a var in the query string (this parameter may appear multiple times)", type=str)
    parser.add_argument("-j", "--join-string", action="store", dest="separator", default=" ", help="character (or string) used to separate the different fields (default: <blank space>)", type=str)
    parser.add_argument("-F", "--format-string", action="store", metavar="format string", dest="fmtstring", default=None, help="user defined format string", type=str)
    parser.add_argument("-V", "--version", action="version", version="%(prog)s {}".format(VERSION))
    parser.add_argument("urls", nargs="+", help="the urls to be formatted", type=str)

    args = parser.parse_args()

    # This way we will interpret escaped strings like \n
    args.separator = args.separator.encode("utf-8").decode('unicode-escape')

    # If provided a custom format string, let's ignore the rest
    if args.fmtstring is None:
        if args.format is None:
            format_string="%U"
        else:
            format_string = args.separator.join(args.format)
    else:
        format_string = args.fmtstring

    id1 = "#" + id_generator() + "#"

    linejoin = "\n"

    # If the file name is '-' read from the stdin
    if args.urls[0] == "-":
        urls = map(lambda x: x.decode(), sys.stdin.buffer.readlines())
    else:
        urls = args.urls

    result = []
    
    for url in urls:
        url=url.strip()
        parsed = urlparse(url)

        # Save the %%
        result_string = format_string.replace("%%", id1)

        # Replace the special values
        result_string = result_string.replace("%U",rprint(url))
        result_string = result_string.replace("%s",rprint(parsed.scheme))
        result_string = result_string.replace("%u",rprint(parsed.username))
        result_string = result_string.replace("%w",rprint(parsed.password))
        result_string = result_string.replace("%H",rprint(parsed.hostname))
        result_string = result_string.replace("%p",rprint(parsed.port))
        result_string = result_string.replace("%P",rprint(parsed.path))
        result_string = result_string.replace("%q",rprint(parsed.query))
        result_string = result_string.replace("%m",rprint(parsed.params))
        result_string = result_string.replace("%f",rprint(parsed.fragment))

        # Find variables and replace their values
        variables = re.finditer(r'%#(?P<varname>[^#]*)#', result_string)
        vars = getvars(parsed.query)
        shift = 0
        if variables is not None:
            for v in variables:
                varname = v.group("varname")
                value = rprint(vars[varname] if varname in vars else None)
                result_string = result_string[:v.start("varname")-2-shift] + value + result_string[v.end("varname")+1-shift:]
                size = v.end("varname") - v.start("varname") + 3 - len(str(value))
                shift += size

        # Restore the %%
        result_string = result_string.replace(id1, "%%")

        result.append(result_string)

    print(linejoin.join(result))

# The main function for htmlq command
def htmlq():

    # Delay importing libraries
    from bs4 import BeautifulSoup as Soup

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", dest="filename", default=None, help="file to read (default: stdin)")
    parser.add_argument("-u", "--url", action="store", dest="url", default=None, help="url to parse (it will be downloaded and queried); it is incompatible with the use of a file")
    parser.add_argument("-U", "--user-agent", action="store", dest="user_agent", default=None, help="use an user agent string to get the web page from the URL")
    parser.add_argument("-a", "--attr", action="append", dest="attribute", default=None, help="attributes to get from the html tags (the whole tag if not provided); may appear more than once", type=str)
    parser.add_argument("-r", "--rm", action="append", dest="rmquery", default=None, help="query string of elements to remove on each element found; may appear more than once", type=str)
    parser.add_argument("-s", "--separator", action="store", dest="separator", default="\0", help="character (or characters) used to separate the different results from the query (not the fields in a result) (default: 0 char)", type=str)
    parser.add_argument("-S", "--field-separator", action="store", dest="fieldseparator", default=",", help="character (or characters) used to separate the value of the different attributes of an entry resulting from the query (default: ,)", type=str)
    parser.add_argument("-n", "--no-empty-lines", action="store_true", dest="noemptylines", default=False, help="omits the empty resulting entries (i.e. those equal to \"\")")
    parser.add_argument("-N", "--no-empty-attr", action="store_true", dest="noemptyattr", default=False, help="omits the empty values of attributes (i.e. those equal to \"\")")
    parser.add_argument("-1", "--only-first", action="store_true", dest="onlyfirst", default=False, help="if multiple entries are found in the html document, show only the first one")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s {}".format(VERSION))
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
