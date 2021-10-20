# htmlq - command line HTML query 
This is a simple command line utility to query HTML content as if you were using jQuery selectors. The idea is to be able to use commands like the next one:

```console
$ wget -q -O- www.google.com | htmlq title
```

and get an output like this one:

```console
<title>Google</title>
```

The command is mainly useful for scripting. For example, it is possible to try to get the version of a wordpress installation, by checking the `meta name="generator"` tag:

```console
$ htmlq -u www.wordpress.com 'meta[name="generator"]'
<meta content="WordPress.com" name="generator"/>
```

Or the title of a web page:

```console
$ htmlq -u www.google.com title
<title>Google</title>
```

It is even possible to get the value of a particular attribute in a tag

```console
$ htmlq -u www.wordpress.com 'meta[name="generator"]' -a name
generator
```

Or even do more sophisticated queries than remove internal elements, empty values, etc. As an example, the next query gets the title string of the different items in a search of items in ebay:

```
$ htmlq -u "https://www.ebay.com/sch/i.html?_nkw=laptop"  "li.s-item h3.s-item__title" -s "\n" --rm span -a . -n
```

## Installing

Install using `python-pip`:

```
$ pip install htmlq
```

or building from source:

```
$ pip install bs4 html5lib urllib3 requests pathlib
...
$ git clone https://github.com/dealfonso/htmlq.git
$ cd htmlq
$ python3 setup.py install
```

## Use Cases

The most simple way to use `htmlq` is to get a tag from a web page:

```console
$ htmlq -u www.github.com title
<title>GitHub: Where the world builds software · GitHub</title>
```

_(*) this example gets the title of a web page_

---

But we may want to get other tag...

```console
$ htmlq -u www.github.com a
<a class="px-2 py-4 color-bg-info-inverse color-text-white show-on-focus js-skip-to-content" href="#start-of-content">Skip to content</a><a href="https://docs.github.com/articles/supported-browsers">
          Learn more about the browsers we support.
        </a><a aria-label="Homepage" class="mr-4" data-ga-click="(Logged out) Header, go to homepage, icon:logo-wordmark" href="https://github.com/">
          <svg aria-hidden="true" class="octicon octicon-mark-github color-text-white" data-view-component="true" height="32" version="1.1" viewBox="0 0 16 16" width="32">
    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" fill-rule="evenodd"></path>
</svg>
        </a><a class="d-inline-block d-lg-none f5 color-text-white no-underline border color-border-tertiary rounded-2 px-2 py-1 mr-3 mr-sm-5" data-hydro-click='{"event_type":"authentication.click","payload":{"location_in_page":"site header","repository_id":null,"auth_type":"SIGN_UP","originating_url":"https://github.com/","user_id":null}}' data-hydro-click-hmac="520d87e8f83281e6946b192f0f840552721c7fcba9b9c36d802e898a816314e2" href="/signup?ref_cta=Sign+up&amp;ref_loc=header+logged+out&amp;ref_page=%2F&amp;source=header-home">
                Sign up
...
```

_(*) this example gets the "a" tags of a web page_

---

We obtained a lot of information, and that is why we wanted to narrow the query to remove those that we do not need

```console
$ htmlq -u www.github.com "a[aria-label]"
<a aria-label="Homepage" class="mr-4" data-ga-click="(Logged out) Header, go to homepage, icon:logo-wordmark" href="https://github.com/">
          <svg aria-hidden="true" class="octicon octicon-mark-github color-text-white" data-view-component="true" height="32" version="1.1" viewBox="0 0 16 16" width="32">
    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" fill-rule="evenodd"></path>
</svg>
        </a><a aria-label="Go to GitHub homepage" class="color-text-primary" data-hydro-click='{"event_type":"analytics.event","payload":{"category":"Footer","action":"go to home","label":"text:home","originating_url":"https://github.com/","user_id":null}}' data-hydro-click-hmac="062d687e04e8668f63bed700cfd9281766aa03a46d1beb6c750d751f692a1442" href="/">
          <img alt="GitHub" class="footer-logo-mktg" decoding="async" height="30" loading="lazy" src="https://github.githubassets.com/images/modules/site/icons/footer/github-logo.svg" width="84"/>
        </a>
```

_(*) this example gets the link tags of a web page, but those that do have the attribute aria-label set_

---

But we only want to select the _a_ tag, without some of the inner tags

```console
$ htmlq -u www.github.com "a[aria-label]" --rm svg --rm img
<a aria-label="Homepage" class="mr-4" data-ga-click="(Logged out) Header, go to homepage, icon:logo-wordmark" href="https://github.com/">

        </a><a aria-label="Go to GitHub homepage" class="color-text-primary" data-hydro-click='{"event_type":"analytics.event","payload":{"category":"Footer","action":"go to home","label":"text:home","originating_url":"https://github.com/","user_id":null}}' data-hydro-click-hmac="062d687e04e8668f63bed700cfd9281766aa03a46d1beb6c750d751f692a1442" href="/">

        </a>
```

_(*) the --rm parameter enables to remove inner queries on each entry_

---

But we only need the value of the label attribute, one on each line:

```console
$ htmlq -u www.github.com "a[aria-label]" --rm svg --rm img -a aria-label -s "\n"
Homepage
Go to GitHub homepage
```

_(*) the -a parameter enables to obtain the values of the attributes for each resulting entry, and -s sets the separator between results_

---

Finally we want to get also the destination URL, with a pretty arrow:

```console
htmlq -u www.github.com "a[aria-label]" --rm svg --rm img -a aria-label -a href -s "\n" -S " -> "
Homepage -> https://github.com/
Go to GitHub homepage -> /
```

_(*) we may include multiple attributes (using multiple -a entries) and join them with specific connectors using -S_

## Detailed options

The usage syntax for `htmlq` is the next:

```console
htmlq [-h] [-f FILENAME] [-u URL] [-a ATTRIBUTE] [-r RMQUERY] [-s SEPARATOR] [-S FIELDSEPARATOR] [-n] [-N] [-1] [-U USER_AGENT] query
```

There are multiple options and flags for `htmlq` and here we try to explain each of them.

- __-f | --filename \<filename\>__ reads content of the file `filename`. It is possible to use the whole path to the file (e.g. `/path/to/my/file`) or use special paths (e.g. `~/myfile`). If no filename nor url is included, `htmlq` will read from the standard input.

- __-u | --url \<url\>__ retrieves the content to be parsed from the url. It is advisable to include the whole schema in the url (e.g. `https://my.url`). If not included, the `https` schema will be tried in first place, and if it fails, `http` will be tried. If a file is included in the commandline, this parameter will be ignored. If no filename nor url is included, `htmlq` will read from the standard input.

- __-a | --attr \<attribute list\>__ if a query obtains a set of tags as a result, the default behavior (if this parameter is not set) is to output the result of the whole obtained html fragments. Instead, if an attribute is queried (using _-a_) the output will be the values of each of these attributes for the entry. In case that an attribute is not in the html node, its output will be _blank_. It is possible to query multiple attributes by including multiple _-a_ entries (e.g. `-a href -a aria-label`). There is an special attribute (.) which refers to the text representation of the entry (i.e. `-a .`).

- __-r | --rm \<query\>__ the query to the html document may contain child nodes (e.g. \<ul\>\<li\>\<li\>\</ul\>). When querying for `<ul>`, the result will be the `<ul>` node along with its `<li>` child nodes. Using `-r` it is possible to delete the `<li>` nodes. It is possible to remove multiple child trees by including multiple `--rm` queries.

- __-s | --separator \<separator\>__ this is the string used to join the output of the result of the different entries. It is possible to include escaped strings (e.g. `\n`) or whole arbitraty strings (e.g. `\n ->`). The default value is `\0`.

- __-S | --field-separator \<separator\>__ this is the string used to join the values of the different attributes obtained from an entry, using `-a` parameter. It is possible to include escaped strings (e.g. `\n`) or whole arbitraty strings (e.g. `->`). The default value is `,`.

- __-n | --no-empty-lines__ using this flag, `htmlq` will not include empty lines (i.e. lines whose value is _blank_ as a result of the combination of attributes).

- __-N | --no-empty-attr__ using this flag, `htmlq` will not include the value of attributes that are empty (i.e. lines whose value is _blank_ as a result of the combination of attributes). Using this option, the number of resulting attributes may differ from the number of requested attributes (e.g. `-a href -a class -a id` may be converted to `/,mylink` if _class_ is not set for an entry).

- __-1 | --only-first__ if a query obtains multiple results, using this flag, `htmlq` will deal only with the first one (thus ignoring the rest).

- __-U | --user-agent \<user agent string\>__. Using this parameter, it is possible to set an arbitraty user agent string to retrieve the web page. You can check your user agent string in this web: https://www.whatsmyua.info

- __query__. This is the query string that wants to be retrieved from the html web page. It is possible to use queries that retrieve multiple trees. In this case, `htmlq` will consider them as individual entries and will deal with all of them (or only the first if using flag `-1`).

# urlf - format url

This command is an add-on to _htmlq_, as a command line application to deal with URLs and extracting information about them. 

The original purpose was to extract the values of variables in URLs, so that their values can be used in scripts. An example:

```console
$ urlf -v oq "https://www.google.com/search?q=github&oq=github&sourceid=chrome&ie=UTF-8"
github
```

_(*) This example gets the value of var **oq**._

Then the application has evolved to enable rewritting URLs, using the commandline as in the next example:

```console
$ urlf "https://www.google.com/search\?q=github&oq=github&sourceid=chrome&ie=UTF-8" -F "%s://%H?oq=%#oq#"
https://www.google.com?oq=github
```

_(*) This example rewrites the URL to build a new one that removes the path and just includes the value of var **oq**._

## Detailed options

There are multiple options and flags for `urlf` and here we try to explain each of them.

```console
usage: urlf [-h] [-U] [-s] [-u] [-w] [-H] [-p] [-P] [-q] [-m] [-f] [-v var name] [-j SEPARATOR] [-F format string] [-V] urls [urls ...]
```

- __-h, --help__: shows the help
- __-V, --version__: show program's version number and exit
- __-U, --url__: displays the URL as provided in the input.
- __-s, --scheme__: shows the scheme provided in the url (e.g. https)
- __-u, --username__: shows the username to accede to the url (i.e. user in https://user@pass:myserver.com)
- __-w, --password__: shows the password to accede to the url (i.e. pass in https://user@pass:myserver.com)
- __-H, --hostname__: shows the hostname in the url (i.e. myserver.com in https://myserver.com/my/path)
- __-p, --port__: shows the port in the url (i.e. 443 in https://myserver.com:443/my/path)
- __-P, --path__: shows the path in the url (i.e. my/path in https://myserver.com/my/path)
- __-q, --query__: shows the query in the url (i.e. q=1&r=2 in https://myserver.com/my/path?q=1&r=2)
- __-m, --parameters__: shows the parameters to accede to the url (i.e. param in https://myserver.com/my/path;param?q=1&r=2)
- __-f, --fragment__: shows the fragment in the url (i.e. sec1 in https://myserver.com/my/path#sec1)
- __-v var name, --var var name
                        show the value of a var in the query string (this parameter may appear multiple times, to get the values of multiple variables; they will appear in the same order than appeared in the commandline)
- __-j | --join-string \<SEPARATOR\>__: 
                        character (or string) used to separate the different fields (default: <blank space>)
- __-F | --format-string \<format string\>__: 
                        user defined format string to get a custom output of the URL parts. Any arbitrary field or character may appear in this string, and the fields are substituted using the letter in the shorthand flag of each parameter, preceded by symbol %. E.g. `urlf -H` is the same than `urlf -F "%H"`; e.g. `urlf -s -H` is the same than `urlf -F "%s%H"`, but you can use `urlf -F "%s://%H"` to obtain a better output. In the case of variables, the value is obtained by surrounding the name of the var by symbol # and prepending symbol %; e.g. `urlf -v q` is the same than `urlf -F "%#q#"`.

# A combined example (guessing wordpress version)
In case that we wanted to get the version of a wordpress installation, we could check meta tag and get the content:

```
$ htmlq -u www.grycap.upv.es 'meta[name="generator"]'
<meta content="WordPress 5.8.1" name="generator"/>
$ htmlq -u www.grycap.upv.es 'meta[name="generator"]' -a content
WordPress 5.8.1
```

But many plugins hide the version in the tag, so we can try to guess the version from the links:

```
$ htmlq -u www.grycap.upv.es 'link[href*="?ver="]' -s '\n'
<link href="https://www.grycap.upv.es/wp-includes/css/dist/block-library/style.min.css?ver=5.8.1" id="wp-block-library-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/style.css?ver=5.8.1" id="specia-style-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/colors/default.css?ver=5.8.1" id="specia-default-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/owl.carousel.css?ver=5.8.1" id="owl-carousel-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/bootstrap.css?ver=5.8.1" id="bootstrap-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/woo.css?ver=5.8.1" id="woo-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/form.css?ver=5.8.1" id="specia-form-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/typography.css?ver=5.8.1" id="specia-typography-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/media-query.css?ver=5.8.1" id="specia-media-query-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/widget.css?ver=5.8.1" id="specia-widget-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/animate.min.css?ver=5.8.1" id="animate-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/text-rotator.css?ver=5.8.1" id="specia-text-rotator-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/css/menus.css?ver=5.8.1" id="specia-menus-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/themes/specia/inc/fonts/font-awesome/css/font-awesome.min.css?ver=5.8.1" id="font-awesome-css" media="all" rel="stylesheet" type="text/css"/>
<link href="https://www.grycap.upv.es/wp-content/plugins/forget-about-shortcode-buttons/public/css/button-styles.css?ver=2.1.2" id="forget-about-shortcode-buttons-css" media="all" rel="stylesheet" type="text/css"/>
```

From the links, we see that wordpress includes the version of wordpress in the "ver" variable for any link; so we may get the value of such variable using `urlf`:

```
$ htmlq -u www.grycap.upv.es 'link[href*="?ver="]' -s '\n' -a href | ./urlf.py -v ver -
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
5.8.1
2.1.2
5.8.1
```

And now, if we get the most used value, it will probably be the one that refers to the wordpress version (because other plugins may also use that variable for its purposes):

```
$ htmlq -u www.grycap.upv.es 'link[href*="?ver="]' -s '\n' -a href | ./urlf.py -v ver - | sort | uniq -c | sort -k1 -n -r
  15 5.8.1
   1 2.1.2
```

And the first one will be the most voted version.

Now we can compare to the currently available wordpress version:

```
$ curl -s https://api.wordpress.org/core/version-check/1.7/ | jq ".offers[].version" | tr -d '"' | sort -V | tail -n 1
5.8.1
```

Our final script would be something like the next one:

```bash
#!/bin/bash
MYVERSION="$(htmlq -u www.grycap.upv.es 'link[href*="?ver="]' -s '\n' -a href | ./urlf.py -v ver - | sort | uniq -c | sort -k1 -n -r | head -n 1 | awk '{print $2}')"
CURRENTVERSION="$(curl -s https://api.wordpress.org/core/version-check/1.7/ | jq ".offers[].version" | tr -d '"' | sort -V | tail -n 1)"

LATESTVERSION="$(echo "$MYVERSION
$CURRENTVERSION" | sort -V -r | head -n 1)"
if [ "$LATESTVERSION" = "$MYVERSION" ]; then
        echo "you have the latest version of wordpress ($LATESTVERSION)"
else
        echo "you should update your wordpress version"
        exit 1
fi
exit 0
```