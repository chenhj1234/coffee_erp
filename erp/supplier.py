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

bp = Blueprint('supplier', __name__, url_prefix='/supplier')
@bp.route('/', methods=['GET', 'PUT', 'POST'])
def supplier_handler():
    reslist = db.get_supplier()
    ERP.dbgprint (reslist, ERP.K_DEBUG_SUPPLIER)
    if request.method == 'GET':
        per_rec_list_len = 0
        if len(reslist) > 0:
            per_rec_list_len = len(reslist[0])
        return render_template('supplier_list.html', reslist= reslist, len = per_rec_list_len, descbegin = 2)
    elif request.method == 'POST':
        reslist = db.get_supplier(request_form = request.form)
        if not bool(reslist):
            db.add_supplier(request.form)
        else :
            ERP.dbgprint ('Record already exist', ERP.K_DEBUG_SUPPLIER)
        reslist = db.get_supplier()
        per_rec_list_len = 0
        if len(reslist) > 0:
            per_rec_list_len = len(reslist[0])
        return render_template('supplier_list.html', reslist= reslist, len = per_rec_list_len, descbegin = 2)

@bp.route('/addsupplier', methods=['GET'])
def addsupplier():
    suppliercol = db.get_supplier_table_col()
    suppliercoldesc = ['供應商名(必填)',
    '下單次數(可不填)',
    '下單總量(KG)(可不填)',
    '最早下單日期(可不填)',
    '最近下單日期(可不填)',
    '下單頻率(可不填)',
    '評價(可不填)',
    '備註(可不填)']
    ERP.dbgprint (suppliercol, ERP.K_DEBUG_SUPPLIER)
    if request.method == 'GET':
        return render_template('supplier_add.html', len = len(suppliercoldesc), cols = suppliercol, colsdesc = suppliercoldesc)
    
