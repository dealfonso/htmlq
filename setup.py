from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

from htmlq.version import VERSION

setup(
  name = 'htmlq',             # How you named your package folder
  packages = ['htmlq'],   
  version = VERSION,          # Start with a small number and increase it with every change you make
  license='Apache 2.0',       # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Script that enables querying an html input (file or url) as using jquery selector strings',
  long_description = README,
  long_description_content_type = 'text/markdown',
  author = 'Carlos A.',             # Type in your name
  author_email = 'caralla@upv.es',  # Type in your E-Mail
  url = 'https://github.com/dealfonso/htmlq',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/user/reponame/archive/v_011.tar.gz',
  keywords = ['html', 'command line', 'htmlquery', 'jquery', 'url' ],   # Keywords that define your package best
  install_requires=[           
          'bs4',
          'html5lib',
          'urllib3',
          'requests',
          'pathlib'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Intended Audience :: System Administrators',
    'Topic :: Utilities',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
  ],
  entry_points = {
    'console_scripts' : [ 
      'htmlq=htmlq:htmlq',
      'urlf=htmlq:urlf'
    ]
  }
)