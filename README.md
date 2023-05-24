## PostgreSQL database access pages 

©2021 Barend Köbben - <a href="mailto:b.j.kobben@utwente.nl">b.j.kobben@utwente.nl</a> 

This web application creates a set of generic web pages that gives acces (for searching, displaying, creating and editing) to database tables in a web accesible database. It runs as a Python CGI application: 
- Standard Python modules used are sys, cgi (and cgitb for debugging)
- Python module for HTML templating: jinja2 [http://jinja.pocoo.org]
- Python module for DB access: psycopg2 [https://www.psycopg.org/]

The attributes of the access (editing/views/access rights) can be set by editing the configuration in the file TableDefinition.py
The styling of the resultant web pages can be changed in the file ../templates/tablepages.css
The content of the resultant web pages can be changed in the jinja templates in ../templates/*.html

[Code available on GitHub](https://github.com/kobben/DBpages)...

Licensed under GNU General Public License v3.0 (see https://choosealicense.com/licenses/gpl-3.0/)

SPDX-License-Identifier: GPL-3.0-only

#### Changelist:
    v4.4 May 2023 - now using AuthUserFile mechanism for passwords
    v4.3 Oct 2021 - added .FixTableHead  to get fixed header scrolling table
                  - removed bug (no sorting of fkarrays in templates showtable/showrec.html)
    v4.2 Aug 2021 - includes json type (for Postgres JSONB cols)
    v4.1 Mar 2020 - removed bug in date handling in template search.html & search_all_and_show.html
    v4.0 Oct 2019 - new styling, using CSS and (included) LatoLatin webfont in standard style
                  - extra security measures against SQL injection
    v3.6 May 2019 - included defaultRoute & defaultWhere parameter
    v3.5 Dec 2018 - implemented bool (boolean) column type
    v3.2 Dec 2017 - included img (image) type & simpleLightBox code
    v3.0 Oct 2017 - new implementation as Python CGI, with py config file
                  - HTML templating using Jinja2 module
    v2.1 May 2012 - includes txt type & sum columns & pw check
    v1.0 Apr 2011 - initial version, using Python ASP (Windows IIS)