## Generic PostgreSQL database access pages for web applications

©2018 Barend Köbben - <a href="mailto:b.j.kobben@utwente.nl">b.j.kobben@utwente.nl</a> 

This web application creates a set of generic web pages that gives acces (for searching, displaying, creating and editing) to database tables in a web accesible database. It runs as a Python CGI application: 
- Standard Python modules used are sys, codecs, cgi (and cgitb for debugging)
- Python module for HTML templating: jinja2 [http://jinja.pocoo.org]
- Python module for DB access: psycopg2 [http://initd.org/psycopg/]

The attributes of the access (editing/views/access rights) can be set by editing the configuration in the file TableDefinition.py
The styling of the resultant web pages can be changed in the file templates/tablepages.css

[Code available on GitHub](https://github.com/kobben/DBpages)...

Licensed under GNU General Public License v3.0 (see https://choosealicense.com/licenses/gpl-3.0/)

SPDX-License-Identifier: GPL-3.0-only

#### Changelist:
    v3.5 Dec 2018 -- implemented bool (boolean) column type
    v3.2 Dec 2017 -- included img (image) type & simpleLightBox code
    v3.0 Oct 2017 -- now implemented as Python CGI, with py config file
    v2.1 May 2012 -- includes txt type & sum columns & pw check