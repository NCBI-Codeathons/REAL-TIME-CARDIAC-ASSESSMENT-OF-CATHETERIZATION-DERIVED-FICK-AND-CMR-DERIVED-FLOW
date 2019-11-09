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
def fick_room_air(tables=None, err_msg=None):
    if request.method == 'POST':
        if (request.form['vo2'] and request.form['hg'] and request.form['pv'] and request.form['lpa']
        and request.form['ao'] and request.form['mv'] and request.form['tp'] and request.form['ts']):
            vo2=float(request.form['vo2'])
            hg=float(request.form['hg'])
            pv=float(request.form['pv'])
            lpa=float(request.form['lpa'])
            ao=float(request.form['ao'])
            mv=float(request.form['mv'])
            tp=float(request.form['tp'])
            ts=float(request.form['ts'])
            if (pv-lpa)==0:
                qp="-"
            else: 
                qp=vo2/((13.6*hg)*(pv-lpa))
            if (ao-mv)==0:
                qs="-"
            else:
                qs=vo2/((13.6*hg)*(ao-mv))
            qpqs=qp/qs
            pvr=tp/qp
            svr=ts/qs
            rprs=pvr/svr
            data_out=[[str(qp),str(qs),str(qpqs),str(pvr),str(svr),str(rprs)]]
            tables = pd.DataFrame(data = data_out, columns = ['Qp','QS','Qp/Qs','PVR','SVR','Rp/Rs'])
            tables=tables.to_html(classes='data', index=False)
            return render_template('fick_room_air.html',  tables=[tables])
        return render_template('fick_room_air.html',  err_msg='fill all inputs')
    return render_template('fick_room_air.html')


if __name__ == '__main__':
    app.run(debug=True)


