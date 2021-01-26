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

bp = Blueprint('purchase', __name__, url_prefix='/purchase')
@bp.route('/', methods=['GET', 'PUT', 'POST'])
def purchase_handler():
    itemlist = db.get_purchase()
    print('-------')
    ERP.dbgprint (itemlist, ERP.K_DEBUG_PURCHASE)
    print('-------')
    if request.method == 'GET':
        return render_template('purchase_list.html', itemlist= itemlist)
    elif request.method == 'POST':
        itemlist = db.get_purchase(request_form = request.form)
        if not bool(itemlist):
            db.add_purchase(request.form)
        else :
            ERP.dbgprint ('Record already exist', ERP.K_DEBUG_PURCHASE)
        itemlist = db.get_purchase()
        return redirect(url_for('purchase.purchase_handler'), code=302) #render_template('purchase_list.html', itemlist= itemlist)

@bp.route('/addpurchase', methods=['GET'])
def addpurchase():
    itemcol = db.get_purchase_table_col()
    itemcoldesc = ['發票號','製單人，根據當下登入人自動寫入','製單人名稱','生豆號','生豆名','供應商號','供應商名','單價公斤','總重量/公斤','總價','下單日','到貨日','有效期限','已驗收','進貨品質','備註']
    suppliers = db.get_supplier()
    rawbeans = db.get_rawbean()
    rawbean_selection_fix = {
        'value' : 0,
        'text' : 1,
        'modifier' : 'adddummy'
    }
    print(g.user)
    itemcol_fix_content = {
        'user_id' : { 'value' : g.user['userid'], 'modifier' : 'fixed'},
        'user_name' : { 'value' : g.user['username'], 'modifier' : 'fixed'},
        "rawbean_id" : {'modifier' : 'hidden'},
        "rawbean_name" : {'modifier' : 'hidden_rawbean_option'},
        "supplier_id" : {'modifier' : 'hidden'},
        "supplier_name" : {'modifier' : 'hidden_supplier_option'},
        "order_date" : {'modifier' : 'hidden_date'},
    }
    ERP.dbgprint (itemcol, ERP.K_DEBUG_PURCHASE)
    print(rawbeans)
    if request.method == 'GET':
        return render_template('create_purchase.html', len = len(itemcoldesc), itemcol = itemcol, itemcoldesc = itemcoldesc, itemfix = itemcol_fix_content, 
            rawbeans = rawbeans, rawbean_len = len(rawbeans), suppliers = suppliers, supplier_len = len(suppliers))
    
