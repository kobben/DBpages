#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# -*- coding: UTF-8 -*-
# -- use !/usr/bin/python3 for python3 on gip.itc.utwente.nl
# -- use !/usr/bin/python for python 2.7
# -- use !/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 for python 3.6 on MacOS

# to make sure UTF-8 cgi output works also on win IIS:
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import cgi, cgitb
cgitb.enable()


# retrieve config from tableDefinition.py file
import tableDefinition as td

# import jinja templating and set environment
from jinja2 import Environment, FileSystemLoader, select_autoescape
# for WIN IIS a path from the Inetpub root is needed:
# env = Environment(loader=FileSystemLoader('pvileden/templates'), autoescape=select_autoescape(['html']))
# for L/Unix Apache a relative path works:
env = Environment(loader=FileSystemLoader('templates'), autoescape=select_autoescape(['html']))

import psycopg2

print('Content-Type: text/html')
print('')

###################
#  DB FUNCTIONS:
###################

def doSelect(dbConfig, theSelectStr):
  theSQL = 'SELECT ' + theSelectStr
  theSQL += ' LIMIT ' + str(dbConfig.resultLimit) + ';'
  # print(theSQL + '<hr>')
  try:
    # Get a database connection (a pgobject) for our database:
    conn = psycopg2.connect(database=dbConfig.theDB,host=dbConfig.theHOST,user=dbConfig.theUN,
               password=dbConfig.thePW, port=dbConfig.thePort)
    # Get a cursor to be used:
    mycursor = conn.cursor()
    mycursor.execute(theSQL) # Get the results:
    queryresult = mycursor.fetchall()
    conn.close()
    return queryresult
  except psycopg2.Error as e:
    conn.close()
    showError('DB Select', str(e.pgerror))
    return None

def doInsert(dbConfig, theInsertStr):
  theSQL = 'INSERT ' + theInsertStr
  theSQL += ';'
  # print(theSQL + '<hr>')
  try:
    # Get a database connection (a pgobject) for our database:
    conn = psycopg2.connect(database=dbConfig.theDB,host=dbConfig.theHOST,user=dbConfig.theUN,
               password=dbConfig.thePW, port=dbConfig.thePort)
    # Get a cursor to be used:
    mycursor = conn.cursor()
    mycursor.execute(theSQL) # do insert
    mycursor.close()
    conn.commit()
    conn.close()
    return "InsertSucces"
  except psycopg2.Error as e:
    conn.close()
    showError('DB Insert', str(e.pgerror))
    return None

def doUpdate(dbConfig, theUpdateStr):
  theSQL = 'UPDATE ' + theUpdateStr
  theSQL += ';'
  # print(theSQL + '<hr>')
  try:
    # Get a database connection (a pgobject) for our database:
    conn = psycopg2.connect(database=dbConfig.theDB, host=dbConfig.theHOST, user=dbConfig.theUN,
                            password=dbConfig.thePW, port=dbConfig.thePort)
    # Get a cursor to be used:
    mycursor = conn.cursor()
    mycursor.execute(theSQL)  # do insert
    mycursor.close()
    conn.commit()
    conn.close()
    return "UpdateSucces"
  except psycopg2.Error as e:
    conn.close()
    showError('DB Update', str(e.pgerror))
    return None

def doDelete(dbConfig, theDeleteStr):
  theSQL = 'DELETE ' + theDeleteStr
  theSQL += ';'
  # print(theSQL + '<hr>')
  try:
    # Get a database connection (a pgobject) for our database:
    conn = psycopg2.connect(database=dbConfig.theDB, host=dbConfig.theHOST, user=dbConfig.theUN,
                            password=dbConfig.thePW, port=dbConfig.thePort)
    # Get a cursor to be used:
    mycursor = conn.cursor()
    mycursor.execute(theSQL)  # do insert
    mycursor.close()
    conn.commit()
    conn.close()
    return "DeleteSucces"
  except psycopg2.Error as e:
    conn.close()
    showError('DB Delete', str(e.pgerror))
    return None
###################


###################
#  SHOW ERROR
###################
def showError(errorModule, errorMessage):

  page = env.get_template('error.html')
  vars = {
    "td": td,
    "PWfromParam": curPW,
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
    "PWfromParam": curPW,
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
  # and do the db select
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
    "PWfromParam": curPW,
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
  # and do the db select
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
    "PWfromParam": curPW,
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
  # and do the db select

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
  # and do the db select

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
  # and do the db select
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
      "PWfromParam": curPW,
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
    "PWfromParam": curPW,
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
  # and do the db select
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
PWneeded = True
curPW = 'none'
if td.PWfromParam == 'none':
  PWneeded = False
else:
  for K in theRequest:
    if K == 'PWfromParam':
      curPW = theRequest[K].value
      if curPW == td.PWfromParam:
        PWneeded = False

if PWneeded:
  page = env.get_template('pw.html')
  vars = {}
  html = page.render(vars)
  print(html)
else:
  for K in theRequest:
    if K == 'do':
      if theRequest[K].value == 'search':
        route = search(theRequest)
      elif theRequest[K].value == 'show':
        route = show_table(theRequest)
      elif theRequest[K].value == 'showrec':
        route = show_rec(theRequest)
      elif theRequest[K].value == 'add':
        route = add_form(theRequest)
      elif theRequest[K].value == 'insert':
        route = insert(theRequest)
      elif theRequest[K].value == 'edit':
        route = edit(theRequest)
      elif theRequest[K].value == 'update':
        route = update(theRequest)
      elif theRequest[K].value == 'delete':
        route = delete(theRequest)
      else:
        showError('Routing Module', 'No valid route detected [do == ' + theRequest[K].value + ']')
        route = 'error'
  if route == '': # default routing = search
    search(theRequest)