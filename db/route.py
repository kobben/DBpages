#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# ----------------------------------------------------------
# ©2023 - Barend Köbben
# v4.4 May 2023 -- see changelist in README.md
## ----------------------------------------------------------

#################
# INIT
#################
import cgi
# to make sure Python creates a UTF-8 cgi output:
import codecs, sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# to enable debugging:
import cgitb
cgitb.enable()
print ('Content-Type: text/html;charset=utf-8')
print ('')

# print(sys.version)

# retrieve config from tableDefinition.py file
import tableDefinition as td

# import psycoppg2 DB connection lib see https://www.psycopg.org/
import psycopg2
import psycopg2.extras
# #avoid JSON parsing by registering a no-op function with register_default_json():
psycopg2.extras.register_default_json(loads=lambda x: x)

# import jinja templating and set environment, see http://jinja.pocoo.org
from jinja2 import Environment, FileSystemLoader, select_autoescape
# for WIN IIS an absolute path from the Inetpub root is needed:
# env = Environment(loader=FileSystemLoader('path_to_this_dir/templates'), autoescape=select_autoescape(['html']))
# for L/Unix Apache a relative path works:
env = Environment(loader=FileSystemLoader('../templates'), autoescape=select_autoescape(['html']))

# print('loaded')

###################
#  DB FUNCTIONS:
###################

def doSelect(dbConfig, theSelectStr):

    whereInStr = theSelectStr.find('ORDER')  # find ORDER clause
    if (whereInStr != -1):  # no ORDER clause, thus no processing needed:
        # insert default WHERE clause if present
        if (hasattr(td, 'defaultWhere') and td.defaultWhere != ''):
            theSelectStrArray = theSelectStr.split('ORDER')  # split on ORDER clause
            whereInStr = theSelectStrArray[0].find('WHERE')  # find WHERE clause
            if (whereInStr == -1): # no WHERE clause
                theSelectStr = theSelectStrArray[0] + ' WHERE ' + td.defaultWhere + ' ORDER' + theSelectStrArray[1]
            else:
                theWhereStrArray = theSelectStrArray[0].split('WHERE')
                theSelectStr = theWhereStrArray[0]  + ' WHERE ' + td.defaultWhere + ' AND ('+ theWhereStrArray[1] +') ORDER' + theSelectStrArray[1]
            # print(str(theSelectStr) + '<hr>')

    theSQL = 'SELECT ' + theSelectStr
    theSQL += ' LIMIT ' + str(dbConfig.resultLimit) + ';'

    # print(theSQL + '<hr>')

    conn = None
    try:
        # Get a database connection (a pgobject) for our database:
        conn = psycopg2.connect(database=dbConfig.theDB,host=dbConfig.theHOST,user=dbConfig.theUN,
                                password=dbConfig.thePW, port=dbConfig.thePort)
        # Get a cursor to be used:
        mycursor = conn.cursor()
        mycursor.execute(theSQL) # Get the results:
        queryresult = mycursor.fetchall()
        if (conn != None):
            conn.close()
        return queryresult
    except psycopg2.Error as e:
        if conn is None :
            showError('DB:',  'No connection established, is the database server running...?')
        else:
            showError('DB Select', str(e.pgerror))
        if (conn != None):
            conn.close()
        return None

def doInsert(dbConfig, theInsertStr):
    theSQL = 'INSERT ' + theInsertStr
    theSQL += ';'
    # print(theSQL + '<hr>')
    conn = None
    try:
        # Get a database connection (a pgobject) for our database:
        conn = psycopg2.connect(database=dbConfig.theDB,host=dbConfig.theHOST,user=dbConfig.theUN,
                                password=dbConfig.thePW, port=dbConfig.thePort)
        # Get a cursor to be used:
        mycursor = conn.cursor()
        mycursor.execute(theSQL) # do insert
        mycursor.close()
        conn.commit()
        if (conn != None):
            conn.close()
        return "InsertSucces"
    except psycopg2.Error as e:
        showError('DB Insert', str(e.pgerror))
        if (conn != None):
            conn.close()
        return None

def doUpdate(dbConfig, theUpdateStr):
    theSQL = 'UPDATE ' + theUpdateStr
    theSQL += ';'
    # print(theSQL + '<hr>')
    conn = None
    try:
        # Get a database connection (a pgobject) for our database:
        conn = psycopg2.connect(database=dbConfig.theDB, host=dbConfig.theHOST, user=dbConfig.theUN,
                                password=dbConfig.thePW, port=dbConfig.thePort)
        # Get a cursor to be used:
        mycursor = conn.cursor()
        mycursor.execute(theSQL)  # do insert
        mycursor.close()
        conn.commit()
        if (conn != None):
            conn.close()
        return "UpdateSucces"
    except psycopg2.Error as e:
        showError('DB Update', str(e.pgerror))
        if (conn != None):
            conn.close()
        return None

def doDelete(dbConfig, theDeleteStr):
    theSQL = 'DELETE ' + theDeleteStr
    theSQL += ';'
    # print(theSQL + '<hr>')
    conn = None
    try:
        # Get a database connection (a pgobject) for our database:
        conn = psycopg2.connect(database=dbConfig.theDB, host=dbConfig.theHOST, user=dbConfig.theUN,
                                password=dbConfig.thePW, port=dbConfig.thePort)
        # Get a cursor to be used:
        mycursor = conn.cursor()
        mycursor.execute(theSQL)  # do insert
        mycursor.close()
        conn.commit()
        if (conn != None):
            conn.close()
        return "DeleteSucces"
    except psycopg2.Error as e:
        showError('DB Delete', str(e.pgerror))
        if (conn != None):
            conn.close()
        return None
###################


###################
#  SHOW ERROR
###################
def showError(errorModule, errorMessage):

    page = env.get_template('error.html')
    vars = {
        "td": td,
        "errorModule": errorModule,
        "errorMessage": errorMessage
    }
    html = page.render(vars)
    print(html)


###################
#  SEARCH
###################
def search(theRequest):

    page = env.get_template('search.html')
    vars = {
        "pagetitle": 'SEARCH ' + td.theTable,
        "td": td
    }
    html = page.render(vars)
    print(html)

###################
#  SEARCH ALL & SHOW
###################
def searchAllAndShow(theRequest):

    page = env.get_template('search_all_and_show.html')
    vars = {
        "pagetitle": 'SEARCH & SHOW ' + td.theTable,
        "td": td
    }
    html = page.render(vars)
    print(html)


###################
#  EDIT REC
###################
def edit(theRequest):

    # Get the main table select SQL:
    whereStr = ''
    selectStr = ''
    for K in theRequest :
        if K == 'where' :
            whereStr = theRequest[K].value
    # and do the db-search select
    for i in range(td.numCols):
        if td.colTypeList[i] == 'date':
            selectStr += "to_char(" +td.colList[i] + ", 'DD/MM/YYYY') AS " + td.colList[i] + ", "
        else:
            selectStr += td.colList[i] + ', '
    selectStr = selectStr.rstrip(', ') #remove last ,
    selectStr += ' FROM ' + td.theTable + whereStr
    queryresult = doSelect(td, selectStr)

    page = env.get_template('edit_rec.html')
    vars = {
        "pagetitle": 'EDIT ' + td.theTable,
        "qr": queryresult,
        "ws": whereStr,
        "td": td
    }
    html = page.render(vars)
    print(html)

###################
#  SHOW REC
###################
def show_rec(theRequest):

    # Get the main table select SQL:
    whereStr = ''
    selectStr = ''
    for K in theRequest :
        if K == 'where' :
            whereStr = theRequest[K].value
    # and do the db-search select
    for i in range(td.numCols):
        if td.colTypeList[i] == 'date':
            selectStr += "to_char(" +td.colList[i] + ", 'DD/MM/YYYY') AS " + td.colList[i] + ", "
        else:
            selectStr += td.colList[i] + ', '
    selectStr = selectStr.rstrip(', ') #remove last ,
    selectStr += ' FROM ' + td.theTable + whereStr
    queryresult = doSelect(td, selectStr)

    page = env.get_template('show_rec.html')
    vars = {
        "pagetitle": 'DETAILS',
        "qr": queryresult,
        "ws": whereStr,
        "td": td
    }
    html = page.render(vars)
    print(html)


###################
#  DELETE
###################
def delete(theRequest):

    selectStr = None
    theDeleteStr = " FROM " + td.theTable
    for K in theRequest :
        if K == 'where' :
            theDeleteStr += theRequest[K].value
        if K == 'sql' :
            selectStr = theRequest[K].value
    # and do the db-search select

    queryresult = doDelete(td, theDeleteStr)
    if queryresult == "DeleteSucces" and selectStr != None:
        show_table(theRequest)

###################
#  UPDATE QUERY
###################
def update(theRequest):

    selectStr = None
    theUpdateStr = ''
    for K in theRequest:
        if K == 'updatesql':
            theUpdateStr = theRequest[K].value
        if K == 'sql':
            selectStr = theRequest[K].value
    # and do the db-search select

    queryresult = doUpdate(td, theUpdateStr)
    if queryresult == "UpdateSucces" and selectStr != None:
        # if td.recView:
        #   show_rec(theRequest)
        # else:
        #   show_table(theRequest)
        show_table(theRequest)


###################
#  SHOW TABLE
###################
def show_table(theRequest):

    # Get the main table select SQL:
    selectStr = ''
    for K in theRequest :
        if K == 'sql' :
            selectStr = theRequest[K].value
    # and do the db-search select
    queryresult = doSelect(td, selectStr)

    if queryresult != None:
        # sum columns where needed:
        for i in range(td.numCols):
            if td.colTypeList[i] == 'num' and td.sumCols[i] == True:
                for rows in queryresult:
                    if rows[i] != None: # no entry = 0
                        td.colSummed[i] = td.colSummed[i] + rows[i];
        page = env.get_template('show_table.html')
        vars = {
            "pagetitle": 'SHOW ' + td.theTable,
            "td": td,
            "originalsql": selectStr,
            "qr": queryresult
        }
        html = page.render(vars)
        print(html)


###################
#  ADD FORM:
###################
def add_form(theRequest):

    page = env.get_template('add_rec.html')
    vars = {
        "pagetitle": 'CREATE RECORD',
        "td": td
    }
    html = page.render(vars)
    print(html)



###################
#  INSERT QUERY:
###################
def insert(theRequest):

    # Get the main table insert SQL:
    insertStr = ''
    selectStr = ''
    for K in theRequest :
        if K == 'insertsql' :
            insertStr = theRequest[K].value
        if K == 'sql' :
            selectStr = theRequest[K].value
    # and do the db-search select
    queryresult = doInsert(td, insertStr)
    #print (queryresult)

    if queryresult == "InsertSucces" and selectStr != '':
        show_table(theRequest)

###################
#  MAIN:
# init and then route
###################

# initialise the table data:
td.numCols = len(td.theTableCols)
td.colList = []
td.colDisplayList = []
td.colInTableList = []
td.colTypeList = []
td.FKTableList = []
td.FKKeyColList = []
td.FKTargetColList = []
td.sumCols = []

td.colSummed = []
td.LUT = []
for line in td.theTableCols:
    tmpStr = line.split(";")
    td.colList.append(tmpStr[0])
    if tmpStr[1] == '': # no separate display name provided:
        td.colDisplayList.append(tmpStr[0].replace('_', ' '))  # just remove underscores for display name
    else:  #  display name provided in td:
        td.colDisplayList.append(tmpStr[1]) # get display name from td
    if tmpStr[2] == 'true':
        td.colInTableList.append(True)
    else:
        td.colInTableList.append(False)
    td.colTypeList.append(tmpStr[3])
    td.FKTableList.append(tmpStr[4])
    td.FKKeyColList.append(tmpStr[5])
    td.FKTargetColList.append(tmpStr[6])
    if tmpStr[7] == 'true':
        td.sumCols.append(True)
    else:
        td.sumCols.append(False)
    td.colSummed.append(0)
    td.LUT.append(None)


# fill LUTs for FK columns:
for i in range(td.numCols):
    if td.colTypeList[i] == 'fk' or td.colTypeList[i] == 'fkarray':
        # Create the LUT select SQL:
        selectStr = td.FKKeyColList[i] + ', ' + td.FKTargetColList[i]
        selectStr += ' FROM ' + td.FKTableList[i]
        td.LUT[i] = doSelect(td, selectStr)

theRequest = cgi.FieldStorage()
route = ''

for K in theRequest:
    if K == 'do':
        if theRequest[K].value == 'search':
            route = search(theRequest)
        elif theRequest[K].value == 'show':
            route = show_table(theRequest)
        elif theRequest[K].value == 'showrec':
            route = show_rec(theRequest)
        elif theRequest[K].value == 'add':
            if td.canEdit:
              route = add_form(theRequest)
            else:
              route='error'
              showError('Routing Module', 'Routing [' + theRequest[K].value + '] not allowed in No-Edit mode.')
        elif theRequest[K].value == 'insert':
            if td.canEdit:
              route = insert(theRequest)
            else:
              route='error'
              showError('Routing Module', 'Routing [' + theRequest[K].value + '] not allowed in No-Edit mode.')
        elif theRequest[K].value == 'edit':
            if td.canEdit:
              route = edit(theRequest)
            else:
              route='error'
              showError('Routing Module', 'Routing [' + theRequest[K].value + '] not allowed in No-Edit mode.')
        elif theRequest[K].value == 'update':
            if td.canEdit:
              route = update(theRequest)
            else:
              route='error'
              showError('Routing Module', 'Routing [' + theRequest[K].value + '] not allowed in No-Edit mode.')
        elif theRequest[K].value == 'delete':
            if td.canEdit:
              route = delete(theRequest)
            else:
              route='error'
              showError('Routing Module', 'Routing [' + theRequest[K].value + '] not allowed in No-Edit mode.')
        else:
            route = 'error'
            showError('Routing Module', 'No valid route detected [do == ' + theRequest[K].value + ']')

if route == '': # no routing in url request, use default routing from td:
    if td.defaultRoute == 'search':
      search(theRequest)
    elif td.defaultRoute == 'searchAllAndShow':
      searchAllAndShow(theRequest)
    elif td.defaultRoute == 'add':
      if td.canEdit:
        add_form(theRequest)
      else:
        showError('Routing Module', 'Routing [' + td.defaultRoute + '] not allowed in No-Edit mode.')
    else:
      showError('Routing Module', 'No valid route detected [' + td.defaultRoute  + ']')