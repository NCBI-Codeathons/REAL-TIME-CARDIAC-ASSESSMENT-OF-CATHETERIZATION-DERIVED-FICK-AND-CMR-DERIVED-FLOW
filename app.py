from flask import Flask, render_template, Response, request
import jinja2
# from flask_httpauth import HTTPBasicAuth
import hashlib, os, binascii
import json
import numpy as np
import pandas as pd

app = Flask(__name__)
# auth = HTTPBasicAuth()

# users = {
#     "admin": "114663c78b2b270cd2e3492cc5f568f64d973d599797bccef4c66df06bd67bd22cd7beb0299eece84dd4a3dd7c3822334da0f1101e50365a4e37de137019535cd675b474909fd599ab97f4f4d1432414c7fe6c3edab6c97af75472c516de0d29",
#     "test_user": "79f691e079a600b4ab0b95a7646962493feacab79495a792960413cc17e91323b6a3c2529cdf1c754429fdb6b54748eb54adf498c7c1e9a078cfd1b64a86591cdeeab6f64ff5878ae5f80281a0952c3c233d77c7556e79fa083784500c8d778d"
# }

# @auth.verify_password
# def verify_password(username, provided_password):
#     if username in users:
#         stored_password=users.get(username)
#         salt = stored_password[:64]
#         stored_password = stored_password[64:]
#         pwdhash = hashlib.pbkdf2_hmac('sha512', 
#             provided_password.encode('utf-8'), 
#             salt.encode('ascii'), 
#             100000)
#         pwdhash = binascii.hexlify(pwdhash).decode('ascii')
#         return pwdhash == stored_password
#     return False


@app.route('/fick_room_air', methods=["POST","GET"])
# @auth.login_required
def fick_room_air(fra_out={}, err_msg=None, show_exp=False):
    if request.method == 'POST':
        if (request.form['pat_id'] and request.form['vo2'] and request.form['hg'] and request.form['pv'] and request.form['pa']
        and request.form['ao'] and request.form['mv'] and request.form['tp'] and request.form['ts']):
            pat_id=request.form['pat_id']
            vo2=float(request.form['vo2'])
            hg=float(request.form['hg'])
            pv=float(request.form['pv'])*0.01
            pa=float(request.form['pa'])*0.01
            ao=float(request.form['ao'])*0.01
            mv=float(request.form['mv'])*0.01
            tp=float(request.form['tp'])
            ts=float(request.form['ts'])
            if (pv-pa)==0:
                qp="-"
            else: 
                qp=round(vo2/((13.6*hg)*(pv-pa)),2)
            if (ao-mv)==0:
                qs="-"
            else:
                qs=round(vo2/((13.6*hg)*(ao-mv)),2)
            qpqs=round(qp/qs,2)
            pvr=round(tp/qp,2)
            svr=round(ts/qs,2)
            rprs=round(pvr/svr,2)
            data_out=[[pat_id,str(qp),str(qs),str(qpqs),str(pvr),str(svr),str(rprs)]]
            tables = pd.DataFrame(data = data_out, columns = ['patient_id','Qp (L/min/m^2)','QS (L/min/m^2)','Qp/Qs','PVR (U*m^2)','SVR (U*m^2)','Rp/Rs'])
            tables.to_csv('fick_room_air.csv', index=False)
            fra_out={}
            fra_out['out_qp']=qp
            fra_out['out_qs']=qs
            fra_out['out_qpqs']=qpqs
            fra_out['out_pvr']=pvr
            fra_out['out_svr']=svr
            fra_out['out_rprs']=rprs

            return render_template('fick_room_air.html', **fra_out , show_exp=True)
        return render_template('fick_room_air.html',  err_msg='fill all inputs')
    return render_template('fick_room_air.html')

@app.route('/export_fick_room_air')
# @auth.login_required
def export_fick_room():
    df= pd.read_csv('fick_room_air.csv')
    csv=df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=fick_room_air.csv"})

if __name__ == '__main__':
    app.run(debug=True)


