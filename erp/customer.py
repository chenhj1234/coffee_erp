import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from erp import db
from erp.erp_const import K_RET_USER_LOGGED_IN
from erp import erp_const as ERP
def get_request(req = None, field = '', defval = None):
    if req is None or field == '':
        return defval
    return req[field]    

bp = Blueprint('customer', __name__, url_prefix='/customer')
@bp.route('/', methods=['GET', 'PUT', 'POST'])
def customer_handler():
    reslist = db.get_customer()
    ERP.dbgprint (reslist, ERP.K_DEBUG_SUPPLIER)
    if request.method == 'GET':
        per_rec_list_len = 0
        if len(reslist) > 0:
            per_rec_list_len = len(reslist[0])
        return render_template('customer_list.html', reslist= reslist, len = per_rec_list_len, descbegin = 2, handler = 'customer.addcustomer')
    elif request.method == 'POST':
        reslist = db.get_customer(request_form = request.form)
        if not bool(reslist):
            db.add_customer(request.form)
        else :
            ERP.dbgprint ('Record already exist', ERP.K_DEBUG_customer)
        reslist = db.get_customer()
        per_rec_list_len = 0
        if len(reslist) > 0:
            per_rec_list_len = len(reslist[0])
        return render_template('customer_list.html', reslist= reslist, len = per_rec_list_len, descbegin = 2, handler = 'customer.addcustomer')


@bp.route('/addcustomer', methods=['GET'])
def addcustomer():
    cols = db.get_customer_table_col()
    colsdesc = ['客戶名',
        '下單次數',
        '下單總量(KG)',
        '最遠下單日期',
        '最近下單日期',
        '下單頻率',
        '評價',
        '備註']
    ERP.dbgprint (cols, ERP.K_DEBUG_CUSTOMER)
    if request.method == 'GET':
        return render_template('customer_add.html', len = len(colsdesc), cols = cols, colsdesc = colsdesc, handler = 'customer.customer_handler')
    
