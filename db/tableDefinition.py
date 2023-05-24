# ----------------------------------------------------------
# © 2023 - Barend Köbben
# v4.4 May 2023 -- see changelist in README.md
# ----------------------------------------------------------
# ----EDIT the vars below to match your DB tables ----------
# ----------------------------------------------------------

# 1: the DB connection params
theHOST = 'localhost'
thePort = 5434
theDB = 'dbpages_test'
theUN = 'dbpages_test_un'
thePW = 'dbpages_test_pw'

# 2:  The name of the table to show and/or edit
theTable = 'leden'

# 3: Can the table be edited (True) or not (False)?
canEdit = False

# 4: maximum number of recs shown in result tables:
resultLimit = 250

# 5: only table view (False) or also detailed rec view (True)
recView = False

# DO NOT CHANGE:
theTableCols = [
###
# 6: Table column details
###
# Below set the names of the table columns you want in you edit pages.
# the format is an array of string arrays with ; delimiter:
# [0] = is the column name
# [1] = column display name (if empty => column name)
# [2] = in tableview [true/false] (ignored if recView = False)
# [3] = matching column type for formatting and checking
#       possible vals are: none | str | num | date | uri | img | fk | fkarray
# [4] = matching table name that holds FK (null for none)
# [5] = matching column name for FK key (null for none)
# [6] = table name for FK or LUT content col (null for none)
# [7] = sum row values in output (true/false)
"leden_id;id;true;none;null;null;null;false",
"voornaam;first name;true;str;null;null;null;false",
"achternaam;last name;true;str;null;null;null;false",
"categorie;category;true;fk;categorien;id;categorie;false",
"betaald;payed;false;fkarray;jaren;jaar;jaar;false"


### DO NOT CHANGE:
]
###

# 7: the column name of the Primary Key:
myPK = 'leden_id'

# 8: a default SQL Filter, that is later combined with other search criteria
# of the user; should be a valid filter in SQL WHERE clause ("e.g. name='John') :
defaultWhere = ''

# 9: the column name to order by default (can be overridden by user)
# format: "colName ASC" or "colName DESC"
# Add _date if its a date type! (eg. "colName_date DESC") :
defaultOrder = 'achternaam ASC'

# 10: default routing - the route that route.py executes if no
# do=route is include in the url/request. Possible values are
# search / searchAllAndShow / add
defaultRoute = 'search'

# 11: interfaceHasXXX: defines possibilities of interface:
# expressed as booleans:
interfaceHasSearch = True
interfaceHasTablecopy = True
interfaceHasHomebutton = False