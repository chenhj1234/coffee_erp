import functools
import mysql.connector
import click

from mysql.connector import Error
from flask import current_app, g
from flask.cli import with_appcontext
from . import erp_const as ERP

db_table_col = {}

def dbgprint(msg = '', opt = 'generic'):
    if(ERP.K_DEBUG_PRINT and ERP.dbgopt[opt]):
        print(msg)


def db_connect_required(funct):
    @functools.wraps(funct)
    def wrapped_view(*args,**kwargs):
        if 'db' not in g or not g.db.is_connected():
            print('DB not connected check by wrapper function, retry connect')
            get_db()
            if 'db' not in g or not g.db.is_connected():
                print('DB not connected check by wrapper function, retry failed')
                return ERP.K_RET_VAL_DB_NOT_CONNECTED

        return funct(*args,**kwargs)

    return wrapped_view

def get_db():
    try :
        if 'db' not in g or not g.db.is_connected():
            g.db = mysql.connector.connect(
                host='10.20.71.108',          # 主機名稱
                database = ERP.K_DB_NAME, # 資料庫名稱
                user='chenhj',        # 帳號
                password='holmas0228')  # 密碼
        return g.db
    except Error as e:
        print("資料庫連接失敗：", e)
        return ERP.K_RET_VAL_DB_NOT_CONNECTED
        


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@db_connect_required
def user_login(usernm = '', passwd = ''):
    if usernm == '' or passwd == '':
        return ERP.K_RET_INVALID_PARAM
    #if 'db' not in g or not g.db.is_connected():
    #    return ERP.K_RET_VAL_DB_NOT_CONNECTED
    query_str = "select * from %s where `user_name` = '%s' and `user_password` = '%s';" % (ERP.K_USER_TABLE_NAME, usernm, passwd)
    try:
        sqldb = g.db
        cursor = sqldb.cursor()
        cursor.execute(query_str)
        results = cursor.fetchall()
        if(len(results) > 0):
            return results[0][0]
        return ERP.K_RET_USER_LOGIN_FAILED
    except Error as e:
        print("資料庫連接失敗：", e)
        return ERP.K_RET_VAL_DB_CONNECTION_FAILED


@db_connect_required
def check_user(usernm = ''):
    if usernm == '':
        return ERP.K_RET_INVALID_PARAM
    #if 'db' not in g or not g.db.is_connected():
    #    return ERP.K_RET_VAL_DB_NOT_CONNECTED
    query_str = "select * from %s where `user_name` = '%s';" % (ERP.K_USER_TABLE_NAME,usernm)
    try:
        sqldb = g.db
        cursor = sqldb.cursor()
        cursor.execute(query_str)
        results = cursor.fetchall()
        if(len(results) > 0):
            return ERP.K_RET_USER_ALREADY_REGISTERED
        return ERP.K_RET_USER_NOT_REGISTERED
    except Error as e:
        print("資料庫連接失敗：", e)
        return ERP.K_RET_VAL_DB_CONNECTION_FAILED

@db_connect_required
def add_user(usernm = '', passwd = '', perm = 'admin'):
    if usernm == '' or passwd == '':
        return ERP.K_RET_INVALID_PARAM
    #if 'db' not in g or not g.db.is_connected():
    #    return ERP.K_RET_VAL_DB_NOT_CONNECTED
    if check_user(usernm) != ERP.K_RET_USER_NOT_REGISTERED:
        # User name already exist or data error
        return ERP.K_RET_USER_ALREADY_REGISTERED
    query_str = "insert into %s (`user_id`,`user_name`,`user_password`,`permission_level`) values (NULL, '%s', '%s', '%s');" % (ERP.K_USER_TABLE_NAME,usernm, passwd, perm)
    print(query_str)
    try:
        sqldb = g.db
        cursor = sqldb.cursor()
        cursor.execute(query_str)
        sqldb.commit()
        return ERP.K_RET_SUCCESS
    except Error as e:
        print("資料庫連接失敗：", e)
        return ERP.K_RET_VAL_DB_CONNECTION_FAILED

def gen_query_str(tabname = '', param_map = None):
    qstr = 'select * from %s' % tabname
    count = 0
    if(param_map != None and len(param_map) > 0):
        qstr = qstr + ' where '
        for key in param_map:
            if(count > 0):
                qstr = qstr + ' and '            
            if(isinstance(param_map[key], str)):
                qstr = qstr + (' `%s` = \'%s\' ' % (key, param_map[key]))
            elif(isinstance(param_map[key], int)):
                qstr = qstr + (' `%s` = %d ' % (key, param_map[key]))
            count += 1
    return qstr

def gen_insert_str(tabname = '', param_map = None):
    count = 0
    colstr = ""
    valstr = ""
    if(param_map != None and len(param_map) > 0):
        colstr = colstr + ' ( '
        valstr = valstr + ' ( '
        for key in param_map:
            if(count > 0):
                colstr = colstr + ' , '
                valstr = valstr + ' , '
            if(isinstance(param_map[key], str)):
                colstr = colstr + "%s" % key
                valstr = valstr + "'%s'" % param_map[key]
            elif(isinstance(param_map[key], int)):
                colstr = colstr + "%s" % key
                valstr = valstr + "%d" % param_map[key]
            elif param_map[key] is None:
                colstr = colstr + "%s" % key
                valstr = valstr + "NULL"
            count += 1
        valstr = valstr + ' ) '
        colstr = colstr + ' ) '
    ERP.dbgprint (colstr, ERP.K_DEBUG_DB)
    ERP.dbgprint (valstr, ERP.K_DEBUG_DB)
    qstr = 'insert into %s %s values %s' % (tabname, colstr, valstr)
    return qstr

def issue_query(query_str = '', do_commit = False):
    try:
        sqldb = g.db
        cursor = sqldb.cursor()
        cursor.execute(query_str)
        if(do_commit):
            sqldb.commit()
        results = cursor.fetchall()
        return results
    except Error as e:
        print("資料庫連接失敗：", e)
        return ERP.K_RET_VAL_DB_CONNECTION_FAILED


@db_connect_required
def get_rawbean(bean_id = None, bean_name = '', request_form = {}):
    param = {}
    if bean_id is not None:
        param['rawbean_id'] = bean_id
    if bean_name != '':
        param['rawbean_name'] = bean_name
    if len(request_form) > 0:
        for key in request_form:
            if request_form[key] != '':
                param[key] = request_form[key]
    dbgprint(param, opt='db')
    qstr = gen_query_str(ERP.K_RAWBEAN_TABLE_NAME, param)
    dbgprint(qstr)
    reslist = issue_query(qstr)
    dbgprint(reslist, opt='db')
    return reslist

def get_rawbean_table_col():
    return db_table_col[ERP.K_RAWBEAN_TABLE_NAME]

@db_connect_required
def add_rawbean(request_form = {}):
    param = {}
    cols = get_rawbean_table_col()
    print("here.................")
    for i in range(0, len(cols)):
        #if (request_form[cols[i]]):
        #param[cols[i]] = request_form[cols[i]]
        if cols[i] in request_form:
            #if (cols[i] == 'supplier_select'):
            #    continue
            if (request_form[cols[i]] == ''):
                param[cols[i]] = None
            else:
                param[cols[i]] = request_form[cols[i]]
        else:
            param[cols[i]] = None
    qstr = gen_insert_str(ERP.K_RAWBEAN_TABLE_NAME, param)
    issue_query(qstr, True)

@db_connect_required
def get_supplier(req_id = None, req_name = '', request_form = {}):
    param = {}
    if req_id is not None:
        param['supplier_id'] = req_id
    if req_name != '':
        param['supplier_name'] = req_name
    if len(request_form) > 0:
        for key in request_form:
            if request_form[key] != '':
                param[key] = request_form[key]
    dbgprint(param, opt='db')
    qstr = gen_query_str(ERP.K_SUPPLIER_TABLE_NAME, param)
    dbgprint(qstr, opt='db')
    reslist = issue_query(qstr)
    dbgprint(reslist)
    return reslist

def get_supplier_table_col():
    return db_table_col[ERP.K_SUPPLIER_TABLE_NAME]

@db_connect_required
def add_customer(request_form = {}):
    param = {}
    cols = get_customer_table_col()
    for i in range(0, len(cols)):
        #if (request_form[cols[i]]):
        #param[cols[i]] = request_form[cols[i]]
        if cols[i] in request_form:
            if (request_form[cols[i]] == ''):
                param[cols[i]] = None
            else:
                param[cols[i]] = request_form[cols[i]]
        else:
            param[cols[i]] = None
    qstr = gen_insert_str(ERP.K_CUSTOMER_TABLE_NAME, param)
    issue_query(qstr, True)

def get_customer_table_col():
    return db_table_col[ERP.K_CUSTOMER_TABLE_NAME]

@db_connect_required
def get_customer(req_id = None, req_name = '', request_form = {}):
    param = {}
    if req_id is not None:
        param['customer_id'] = req_id
    if req_name != '':
        param['customer_name'] = req_name
    if len(request_form) > 0:
        for key in request_form:
            if request_form[key] != '':
                param[key] = request_form[key]
    dbgprint(param, opt='db')
    qstr = gen_query_str(ERP.K_CUSTOMER_TABLE_NAME, param)
    dbgprint(qstr, opt='db')
    reslist = issue_query(qstr)
    dbgprint(reslist)
    return reslist

def get_purchase_table_col():
    return db_table_col[ERP.K_PURCHASE_TABLE_NAME]

@db_connect_required
def get_purchase(req_id = None, req_name = '', request_form = {}):
    param = {}
    if req_id is not None:
        param['purchase_id'] = req_id
    if req_name != '':
        param['purchase_name'] = req_name
    if len(request_form) > 0:
        for key in request_form:
            if request_form[key] != '':
                param[key] = request_form[key]
    dbgprint(param, opt=ERP.K_DEBUG_PURCHASE)
    qstr = gen_query_str(ERP.K_PURCHASE_TABLE_NAME, param)
    dbgprint(qstr, opt=ERP.K_DEBUG_PURCHASE)
    reslist = issue_query(qstr)
    print(reslist)
    dbgprint(reslist, opt=ERP.K_DEBUG_PURCHASE)
    return reslist

@db_connect_required
def add_purchase(request_form = {}):
    param = {}
    cols = get_purchase_table_col()
    for i in range(0, len(cols)):
        #if (request_form[cols[i]]):
        #param[cols[i]] = request_form[cols[i]]
        if cols[i] in request_form:
            if (request_form[cols[i]] == ''):
                param[cols[i]] = None
            else:
                param[cols[i]] = request_form[cols[i]]
        else:
            param[cols[i]] = None
    qstr = gen_insert_str(ERP.K_PURCHASE_TABLE_NAME, param)
    issue_query(qstr, True)

def init_app(app):
    app.teardown_appcontext(close_db)
    get_db()
    init_table()
    app.cli.add_command(init_db_command)

def add_to_table(tablename = '', collist = ''):
    cols = []
    for i,oneitem in enumerate(collist):
        cols.append(oneitem[0])
    db_table_col[tablename] = cols

def add_table_colume_list(table_name = ''):
    qstr = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='%s' AND `TABLE_NAME`='%s';" % (ERP.K_DB_NAME, table_name)
    res = issue_query(qstr)
    dbgprint(res, ERP.K_DEBUG_DB)
    add_to_table(tablename = table_name, collist = res)

class TblCol:
    def __init__(self, name = "", desc = ""):
        self.colname = name
        self.coldesc = desc
    def __str__(self):
        return "name:{name} description:{desc}".format(name = self.colname, desc=self.coldesc)
    def __unicode__(self):
        return u"name:{name} description:{desc}".format(name = self.colname, desc=self.coldesc)

def add_to_table_with_info(tablename = '', collist = ''):
    cols = []
    for i,oneitem in enumerate(collist):
        tblcol = TblCol(name = oneitem[0], desc=oneitem[8])
        cols.append(tblcol)
    db_table_col[tablename + "_info"] = cols

def add_table_colume_list_with_info(table_name = ''):
    qstr = "SHOW FULL COLUMNS FROM `{table_name}`;".format(table_name = table_name)
    res = issue_query(qstr)
    add_to_table_with_info(tablename=table_name,collist=res)


def init_table():
    add_table_colume_list(ERP.K_RAWBEAN_TABLE_NAME)
    add_table_colume_list(ERP.K_SUPPLIER_TABLE_NAME)
    add_table_colume_list(ERP.K_CUSTOMER_TABLE_NAME)
    add_table_colume_list(ERP.K_PURCHASE_TABLE_NAME)
    add_table_colume_list_with_info(ERP.K_PURCHASE_TABLE_NAME)
    dbgprint(db_table_col, ERP.K_DEBUG_DB)
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    cols = get_purchase_table_col()
    click.echo(cols)
    purchs = get_purchase()
    click.echo(purchs)

