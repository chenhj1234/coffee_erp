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

bp = Blueprint('rawbean', __name__, url_prefix='/rawbean')
@bp.route('/', methods=['GET', 'PUT', 'POST'])
def rawbean_handler():
    beanlist = db.get_rawbean()
    ERP.dbgprint (beanlist, ERP.K_DEBUG_RAWBEAN)
    if request.method == 'GET':
        if len(beanlist) <= 0:
            return 'No bean'
        return render_template('rawbean_list.html', beanlist= beanlist)
    elif request.method == 'POST':
        beanlist = db.get_rawbean(request_form = request.form)
        if not bool(beanlist):
            db.add_rawbean(request.form)
        else :
            ERP.dbgprint ('Record already exist', ERP.K_DEBUG_RAWBEAN)
        beanlist = db.get_rawbean()
        return redirect(url_for('rawbean.rawbean_handler'), code=302) #render_template('rawbean_list.html', beanlist= beanlist)

@bp.route('/addrawbean', methods=['GET'])
def addrawbean():
    beancol = db.get_rawbean_table_col()
    beancoldesc = ['豆名（例如：耶加雪菲）(*必填*)','產區（例如：非洲地區，肯亞）(非必填)','莊園(非必填)','分級（例如：G1)(非必填)','處理方式（例如：日曬）(非必填)','供貨商（例如：聯結咖啡）(非必填)','供貨商編號（需要供貨商相符）(非必填)'
        ,'均價(KG/NTD)(非必填，會根據下單價格自動計算)','庫存重量(KG)(非必填)','最早進貨日期(非必填)','最近進貨日期(非必填)','生豆品質（例如：品質優良，大小均衡）(非必填)','備註（例如：堅果、橘子、柳橙、茉莉花香、尾韻清甜）(非必填)']
    ERP.dbgprint (beancol, ERP.K_DEBUG_RAWBEAN)
    suppliers = db.get_supplier()
    if request.method == 'GET':
        return render_template('create_rawbean.html', len = len(beancoldesc), beancol = beancol, beancoldesc = beancoldesc, supplier_col = 6, suppliers = suppliers, supplier_len = len(suppliers))
    
