# ----------------------------------------------------------
# Barend Köbben
# v3.5 Dec 2018 -- implemented bool (boolean) column type
#	v3.2 Dec 2017 -- included img (image) type & simpleLightBox code 
# v3.0 Oct 2017 -- now implemented as Python CGI, with py config file
# v2.1 May 2012 -- includes txt type & sum columns & pw check
# ----------------------------------------------------------
#
# ----------------------------------------------------------
# ---------EDIT the vars below to match your DB tables -----
# ----------------------------------------------------------

# 1: the DB connection params
theHOST = 'localhost'
thePort = 5432
theDB = 'electives'
theUN = 'electives'
thePW = 'electives'

# 2:  The name of the table to show and/or edit
theTable = 'elective'
# 3: Can the table be edited (True) or not (False)?
canEdit = False
# 4: Set a password, or "none" for free access:
PWfromParam = 'none'
# 5: maximum number of recs shown in result tables:
resultLimit = 750
# 6: only table view (False) or also detailed rec view (True)
recView = True

# DO NOT CHANGE:
theTableCols = [
###

# 7: Table column details
# Below set the names of the table columns you want in you edit pages.
# the format is an array of string arrays with internal ; delimiter:
# [0] = is the column name
# [1] = column display name (if empty => column name)
# [2] = used in tableview [true/false] (ignored if recView = False)
# [3] = matching column type for formatting and checking
#    possible vals are: none | str | txt | num | date | bool | uri | img | fk | fkarray
# [4] = matching table name that holds FK (null for none)
# [5] = matching column name for FK key (null for none)
# [6] = table name for FK or LUT content col (null for none)
# [7] = sum row values in output (true/false)

"id;;false;none;null;null;null;false",
"title;Title;true;str;null;null;null;false",
"description;Description;false;txt;null;null;null;false",
"learning_outcomes;LOs;false;txt;null;null;null;false",
"ec;EC;true;num;null;null;null;true",
"language;Language;true;fk;language;id;name;false",
"ut_period;UT Block;true;str;null;null;null;false",
"itc_quartile;ITC Quartile;true;str;null;null;null;false",
"atlas_semester;ATLAS Semester;true;fk;atlas_semester;id;name;false",
"date_begin;Start Date;true;date;null;null;null;false",
"date_end;End Date;true;date;null;null;null;false",
"atlas_level;ATLAS level;true;fk;atlas_level;id;name;false",
"atlas_type;ATLAS type;true;fk;atlas_type;id;name;false",
"prerequisites;EntryReqs;true;bool;null;null;null;false",
"prerequisites_text;Entry Requirements;false;str;null;null;null;false",
"university;University;true;fk;university;id;name;false",
"faculty;Faculty;true;fk;faculty;id;name;false",
"programme;Programme;true;fk;programme;id;name;false",
"programme_type;Type;true;fk;programme_type;id;name;false",
"coordinator;Coordinator;false;str;null;null;null;false",
"teachers;Teachers;false;str;null;null;null;false",
"osiris_code;Osiris code;true;num;null;null;null;false",
"itc_code;ITC code;false;str;null;null;null;false",
"internal_contact;Contact;false;str;null;null;null;false",
"internal_info_source;Source;false;str;null;null;null;false",
"internal_remarks;Remarks;false;str;null;null;null;false",
"publish;Published;true;bool;null;null;null;false"


### DO NOT CHANGE:
]
###

# the column name of the Primary Key:
myPK = 'id'

# the column name to order by default (can be overridden by user)
# format: "colName ASC" or "colName DESC"
# Add _date if its a date type! (eg. "colName_date DESC") :
defaultOrder = 'id DESC'
