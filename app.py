from flask import Flask, render_template, Response, request
import jinja2
from flask_httpauth import HTTPBasicAuth
import hashlib, os, binascii
import json
import numpy as np
import pandas as pd
from os import path
import datetime

app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "admin": "114663c78b2b270cd2e3492cc5f568f64d973d599797bccef4c66df06bd67bd22cd7beb0299eece84dd4a3dd7c3822334da0f1101e50365a4e37de137019535cd675b474909fd599ab97f4f4d1432414c7fe6c3edab6c97af75472c516de0d29",
    "test_user": "79f691e079a600b4ab0b95a7646962493feacab79495a792960413cc17e91323b6a3c2529cdf1c754429fdb6b54748eb54adf498c7c1e9a078cfd1b64a86591cdeeab6f64ff5878ae5f80281a0952c3c233d77c7556e79fa083784500c8d778d"
}

@auth.verify_password
def verify_password(username, provided_password):
    if username in users:
        stored_password=users.get(username)
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
            provided_password.encode('utf-8'), 
            salt.encode('ascii'), 
            100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    return False

@app.route('/')
@auth.login_required
def index_page():
    return render_template('index.html')



@app.route('/fick_room_air', methods=["POST","GET"])
@auth.login_required
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
            data_out=[[pat_id, str(vo2),str(hg),str(pv),str(pa),str(ao),str(mv),str(tp),str(ts),str(qp),str(qs),str(qpqs),str(pvr),str(svr),str(rprs)]]
            tables = pd.DataFrame(data = data_out, columns = ['patient_id','VO2','Hemoglobin','PV(sat)','PA(sat)','Ao(sat)','MV(sat)','TransPulmonary','TransSystemic','Qp (L/min/m^2)','QS (L/min/m^2)','Qp/Qs','PVR (U*m^2)','SVR (U*m^2)','Rp/Rs'])
            tables.to_csv('data/fick_room_air.csv', index=False)
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
@auth.login_required
def export_fick_room():
    df= pd.read_csv('data/fick_room_air.csv')
    csv=df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=fick_room_air.csv"})

@app.route('/fick_nitric_oxide', methods=["POST","GET"])
@auth.login_required
def fick_nitric_oxide(tables=None, err_msg=None, show_exp=False):
    if request.method == 'POST':
        if (request.form['pat_id'] and request.form['vo2'] and request.form['hg'] and request.form['pv'] and request.form['pv_paO2']
        and request.form['pa'] and request.form['pa_paO2'] and request.form['ao'] and request.form['ao_paO2']
        and request.form['mv'] and request.form['mv_paO2'] and request.form['tp'] and request.form['ts']):
            pat_id=request.form['pat_id']
            vo2=float(request.form['vo2'])
            hg=float(request.form['hg'])
            pv=float(request.form['pv'])*0.01
            pv_paO2=float(request.form['pv_paO2'])
            pa=float(request.form['pa'])*0.01
            pa_paO2=float(request.form['pa_paO2'])
            ao=float(request.form['ao'])*0.01
            ao_paO2=float(request.form['ao_paO2'])
            mv=float(request.form['mv'])*0.01
            mv_paO2=float(request.form['mv_paO2'])
            tp=float(request.form['tp'])
            ts=float(request.form['ts'])
            if (pv-pa)==0:
                qp="-"
            else: 
                qp=round(vo2/((13.6*hg*pv+(0.03*pv_paO2)-(13.6*hg*pa+(0.03*pa_paO2)))),2)
            if (ao-mv)==0:
                qs="-"
            else:
                qs=round(vo2/((13.6*hg*ao+(0.03*ao_paO2)-(13.6*hg*mv+(0.03*mv_paO2)))),2)
            qpqs=round(qp/qs,2)
            pvr=round(tp/qp,2)
            svr=round(ts/qs,2)
            rprs=round(pvr/svr,2)
            data_out=[[pat_id,str(vo2),str(hg),str(pv),str(pv_paO2),str(pa),str(pa_paO2),str(ao),str(ao_paO2),str(mv),str(mv_paO2),str(tp),str(ts),str(qp),str(qs),str(qpqs),str(pvr),str(svr),str(rprs)]]
            tables = pd.DataFrame(data = data_out, columns = ['patient_id','VO2','Hemoglobin','PV(sat)','PV_PaO2','PA(sat)','PA_PaO2','Ao(sat)','AO_PaO2','MV(sat)','MV_PaO2','TransPulmonary','TransSystemic','Qp (L/min/m^2)','QS (L/min/m^2)','Qp/Qs','PVR (U*m^2)','SVR (U*m^2)','Rp/Rs'])
            tables.to_csv('data/fick_nitric_oxide.csv', index=False)
            fra_out={}
            fra_out['out_qp']=qp
            fra_out['out_qs']=qs
            fra_out['out_qpqs']=qpqs
            fra_out['out_pvr']=pvr
            fra_out['out_svr']=svr
            fra_out['out_rprs']=rprs
            return render_template('fick_nitric_oxide.html', **fra_out, show_exp=True)
        return render_template('fick_nitric_oxide.html',  err_msg='fill all inputs')
    return render_template('fick_nitric_oxide.html')

@app.route('/export_fick_nitric')
@auth.login_required
def export_fick_nitric():
    df= pd.read_csv('data/fick_nitric_oxide.csv')
    csv=df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=fick_nitric_oxide.csv"})

@app.route('/MR_Flow', methods=["POST","GET"])
@auth.login_required
def MR_Flow(tables=None, err_msg=None):
    if request.method == 'POST':
        if (request.form['BSA'] and request.form['HR'] and request.form['AoV'] and request.form['DAo'] and request.form['SVC'] and request.form['IVC']
        and request.form['RPA'] and request.form['RPV'] and request.form['LPA'] and request.form['LPV']
        and request.form['RUPV'] and request.form['LUPV']):

            # Define the input variables input from the form
            pat_id = str(request.form['pat_id'])
            BSA = float(request.form['BSA'])
            HR = float(request.form['HR'])
            Aov=float(request.form['AoV'])
            DAo=float(request.form['DAo'])
            SVC=float(request.form['SVC'])
            IVC=float(request.form['IVC'])
            RPA=float(request.form['RPA'])
            RPV=float(request.form['RPV'])
            LPA=float(request.form['LPA'])
            LPV=float(request.form['LPV'])
            RUPV=float(request.form['RUPV'])
            LUPV=float(request.form['LUPV'])

            # Perform collateral related calculations
            collateralAmts, collateralPcnts1, collateralPcnts2 = calcCollateralAmt(HR, Aov, DAo, SVC, IVC, RPA, RPV, LPA, LPV, RUPV, LUPV)

            # Perform the flow related calculations
            calcFlowVars1, calcFlowVars2, calcFlowVars3, calcFlowVars4  = calcFlowVariables(HR, BSA, Aov, DAo, SVC, IVC, RPA, RPV, LPA, LPV, RUPV, LUPV, collateralAmts)

            # Collateral amounts output into data table, always 4 items
            collatAmounts =[str(collateralAmts[0]),str(collateralAmts[1]),str(collateralAmts[2]),str(collateralAmts[3])]

            # Build collateral output
            collat_out={}
            collat_out['collat_m1']= collatAmounts[0]
            collat_out['collat_m2']= collatAmounts[1]
            collat_out['collat_m3']= collatAmounts[2]
            collat_out['collat_m4']= collatAmounts[3]
            collat_out['collat_m1p1'] = collateralPcnts1[0]
            collat_out['collat_m2p1'] = collateralPcnts1[1]
            collat_out['collat_m3p1'] = collateralPcnts1[2]
            collat_out['collat_m4p1'] = collateralPcnts1[3]
            collat_out['collat_m1p2'] = collateralPcnts2[0]
            collat_out['collat_m2p2'] = collateralPcnts2[1]
            collat_out['collat_m3p2'] = collateralPcnts2[2]
            collat_out['collat_m4p2'] = collateralPcnts2[3]

            collat_out['qs_m1'] = calcFlowVars1[0]
            collat_out['qes_m1'] = calcFlowVars1[1]
            collat_out['qep_m1'] = calcFlowVars1[2]
            collat_out['qp_m1'] = calcFlowVars1[3]
            collat_out['qpqs_m1'] = calcFlowVars1[4]
            collat_out['qepqes_m1'] = calcFlowVars1[5]
            collat_out['qepqs_m1'] = calcFlowVars1[6]

            collat_out['qs_m2'] = calcFlowVars2[0]
            collat_out['qes_m2'] = calcFlowVars2[1]
            collat_out['qep_m2'] = calcFlowVars2[2]
            collat_out['qp_m2'] = calcFlowVars2[3]
            collat_out['qpqs_m2'] = calcFlowVars2[4]
            collat_out['qepqes_m2'] = calcFlowVars2[5]
            collat_out['qepqs_m2'] = calcFlowVars2[6]

            collat_out['qs_m3'] = calcFlowVars3[0]
            collat_out['qes_m3'] = calcFlowVars3[1]
            collat_out['qep_m3'] = calcFlowVars3[2]
            collat_out['qp_m3'] = calcFlowVars3[3]
            collat_out['qpqs_m3'] = calcFlowVars3[4]
            collat_out['qepqes_m3'] = calcFlowVars3[5]
            collat_out['qepqs_m3'] = calcFlowVars3[6]

            collat_out['qs_m4'] = calcFlowVars4[0]
            collat_out['qes_m4'] = calcFlowVars4[1]
            collat_out['qep_m4'] = calcFlowVars4[2]
            collat_out['qp_m4'] = calcFlowVars4[3]
            collat_out['qpqs_m4'] = calcFlowVars4[4]
            collat_out['qepqes_m4'] = calcFlowVars4[5]
            collat_out['qepqs_m4'] = calcFlowVars4[6]

            qp = calcFlowVars4[3]
            qep = calcFlowVars4[2]
            qs = calcFlowVars4[0]
            qes = calcFlowVars4[1]
            qpqs = calcFlowVars4[4]
            qepqes = calcFlowVars4[5]
            qepqs = calcFlowVars4[6]

            

            # Export data to local csv file
            
            data_out=[[str(pat_id), str(BSA), str(HR), str(Aov), str(DAo), str(SVC), str(IVC), str(RPA), str(RPV), str(LPA), str(LPV), str(RUPV), str(LUPV), str(qp), str(qep), str(qes),str(qs), str(qpqs),str(qepqs), str(qepqes)]]
            tables = pd.DataFrame(data = data_out, columns = ['patient_id', 'BSA', 'HR', 'Aov', 'DAo', 'SVC', 'IVC', 'RPA', 'RPV', 'LPA', 'LPV', 'RUPV', 'LUPV', 'Qp', 'Qep','Qes','Qs','Qp/Qs', 'Qep/Qs','Qep/Qes'])
            tables.to_csv('data/mr_flow.csv', index=False)

            return render_template('MR_Flow.html', **collat_out , show_exp=True)
        return render_template('MR_Flow.html',  err_msg='fill all inputs')
    return render_template('MR_Flow.html')

@app.route('/export_MR_Flow')
@auth.login_required
def export_MR_Flow():
    df= pd.read_csv('data/mr_flow.csv')
    csv=df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=mr_flow.csv"})

def calcCollateralAmt(HR, Aov, DAo, SVC, IVC, RPA, RPV, LPA, LPV, RUPV, LUPV):

    method1 = method2 = method3 = method4 = method1p1 = method1p2 = method2p1 = method2p2 = method3p1 = method3p2 = method4p1 = method4p2 = 0.000

    # Various methods for calculating Collateral Amount
    # 5555 error code
    try: 
        method1 = round((Aov - (SVC + IVC)),2)
    except:
        method1 = 5555
    
    try:
        method2 = round(((RPV - RPA) + (LPV - LPA)),2)
    except:
        method2 = 5555

    try:    
        method3 = round((Aov - (SVC + DAo)),2)
    except:
        method3 = 5555
    
    try:
        method4 = round((Aov - (RPA + LPA + DAo)),2)
    except:
        method4 = 5555

    # Aggregate the methods inside a list to be returned to the main function
    collateralAmts = [method1, method2, method3, method4]

    # Corresponding percentages for the collateral amount calculation methods
    # Percentage Type 1

    if method1 != 5555: method1p1 = round(method1/Aov,2) 
    else: method1p1 = 5555

    if method2 != 5555: method2p1 = round(method2/Aov,2)
    else: method2p1 = 5555 

    if method3 != 5555: method3p1 = round(method3/Aov,2)
    else: method3p1 = 5555

    if method4 != 5555: method4p1 = round(method4/Aov,2)
    else: method4p1 = 5555

    # Aggregate the methods inside a list to be returned to the main function
    collateralPcnts1 = [method1p1, method2p1, method3p1, method4p1]

    # Percentage Type 2

    if method1 != 5555: method1p2 = round((method1/(Aov - method1)),2)
    else: method1p2 = 5555

    if method2 != 5555: method2p2 = round((method2/(Aov - method2)),2)
    else: method2p2 = 5555

    if method3 != 5555: method3p2 = round((method3/(Aov - method3)),2)
    else: method3p2 = 5555

    if method4 != 5555: method1p2 = round((method4/(Aov - method4)),2)
    else: method4p2 = 5555
    
    # Aggregate the methods inside a list to be returned to the main function
    collateralPcnts2 = [method1p2, method2p2, method3p2, method4p2]

    # Return values to the main function
    return collateralAmts, collateralPcnts1, collateralPcnts2

def calcFlowVariables(HR, BSA, Aov, DAo, SVC, IVC, RPA, RPV, LPA, LPV, RUPV, LUPV, collatAmounts):

    counter = 0

    # Predefine calc flow variables
    calcFlowVars1 = calcFlowVars2 = calcFlowVars3 = calcFlowVars4 = []
    
    for collateral in collatAmounts:

        selectedC = collateral

        # Current collateral amount
        # print('Current collateral ', selectedC)

        # Flow variables
        Qs = round((( Aov * HR ) / BSA),2)
        Qes = round((((Aov - selectedC) * HR) / BSA),2)
        Qep = round((((RPA + LPA)*HR) / BSA),2)
        Qp = round((((RPA + LPA)*HR)/ BSA),2)

        # Ratios
        QpQs = round((Qp/Qs),2)
        QepQes = round((Qep / Qes),2)
        QepQs = round((Qep / Qes),2)

        # Return values to the main function
        calcFlowVars = [Qs, Qes, Qep, Qp, QpQs, QepQes, QepQs]

        # Assign value to one of the calc flow vars
        if counter == 0:
            calcFlowVars1 = calcFlowVars
        if counter == 1:
            calcFlowVars2 = calcFlowVars
        if counter == 2:
            calcFlowVars3 = calcFlowVars
        if counter == 3:
            calcFlowVars4 = calcFlowVars

        counter = counter + 1


    return calcFlowVars1, calcFlowVars2, calcFlowVars3, calcFlowVars4

@app.route('/zone4')
@auth.login_required
def zone4():
    stream_all=get_live_data_src()
    # print('****')
    # print(stream_all["fra_qp"])
    return render_template('zone4.html',**stream_all)

@app.route('/timer',  methods=["POST","GET"])
@auth.login_required
def timer():


    if request.method == 'POST':

        if request.form['submit']=='New Patient':
            
            if (path.exists("./data/fick_room_air.csv")):
                os.remove("./data/fick_room_air.csv")
            if (path.exists("./data/fick_nitric_oxide.csv")):
                os.remove("./data/fick_nitric_oxide.csv")
            if (path.exists("./data/mr_flow.csv")):
                os.remove("./data/mr_flow.csv")
        
    return render_template('timer.html')

@app.route('/get_live_data')
@auth.login_required
def get_live_data():
    stream_all=get_live_data_src()
    stream_all=str(stream_all).replace("\'", "\"")
    # print(stream_all)
    return stream_all

def get_live_data_src():
    stream_all={}
    if (path.exists("./data/fick_room_air.csv")):
        df_fra = pd.read_csv("./data/fick_room_air.csv")
        stream_all["fra_qp"]=str(df_fra["Qp (L/min/m^2)"][0])
        stream_all["fra_qs"]=str(df_fra["QS (L/min/m^2)"][0])
        stream_all["fra_qpqs"]=str(df_fra["Qp/Qs"][0])
        stream_all["fra_pvr"]=str(df_fra["PVR (U*m^2)"][0])
        stream_all["fra_svr"]=str(df_fra["SVR (U*m^2)"][0])
        stream_all["fra_rprs"]=str(df_fra["Rp/Rs"][0])
        stream_all["fra_tp"]=str(df_fra["TransPulmonary"][0])
        stream_all["fra_ts"]=str(df_fra["TransSystemic"][0])
    else:
        stream_all["fra_qp"]="-"
        stream_all["fra_qs"]="-"
        stream_all["fra_qpqs"]="-"
        stream_all["fra_pvr"]="-"
        stream_all["fra_svr"]="-"
        stream_all["fra_rprs"]="-"
        stream_all["fra_tp"]="-"
        stream_all["fra_ts"]="-"
    if (path.exists("./data/fick_nitric_oxide.csv")):
        df_fno = pd.read_csv("./data/fick_nitric_oxide.csv")
        stream_all["fno_qp"]=str(df_fno["Qp (L/min/m^2)"][0])
        stream_all["fno_qs"]=str(df_fno["QS (L/min/m^2)"][0])
        stream_all["fno_qpqs"]=str(df_fno["Qp/Qs"][0])
        stream_all["fno_pvr"]=str(df_fno["PVR (U*m^2)"][0])
        stream_all["fno_svr"]=str(df_fno["SVR (U*m^2)"][0])
        stream_all["fno_rprs"]=str(df_fno["Rp/Rs"][0])
        stream_all["fno_tp"]=str(df_fno["TransPulmonary"][0])
        stream_all["fno_ts"]=str(df_fno["TransSystemic"][0])
    else:
        stream_all["fno_qp"]="-"
        stream_all["fno_qs"]="-"
        stream_all["fno_qpqs"]="-"
        stream_all["fno_pvr"]="-"
        stream_all["fno_svr"]="-"
        stream_all["fno_rprs"]="-"
        stream_all["fno_tp"]="-"
        stream_all["fno_ts"]="-"
    if (path.exists("./data/mr_flow.csv")):
        df_fl = pd.read_csv("./data/mr_flow.csv")
        stream_all["fl_qp"]=str(df_fl["Qp"][0])
        stream_all["fl_qep"]=str(df_fl["Qep"][0])
        stream_all["fl_qs"]=str(df_fl["Qs"][0])
        stream_all["fl_qes"]=str(df_fl["Qes"][0])
        stream_all["fl_qpqs"]=str(df_fl["Qp/Qs"][0])
        stream_all["fl_qepqes"]=str(df_fl["Qep/Qes"][0])
        stream_all["fl_qepqs"]=str(df_fl["Qep/Qs"][0])
        if stream_all["fra_tp"]!="-" and stream_all["fl_qp"]!='0':
            stream_all["fl_pvr"]=str(round((float(df_fra["TransPulmonary"][0])/float(df_fl["Qp"][0])),2))
        else:
            stream_all["fl_pvr"]="-"
        if stream_all["fra_ts"]!="-" and stream_all["fl_qs"]!='0':
            stream_all["fl_svr"]=str(round((float(df_fra["TransSystemic"][0])/float(df_fl["Qs"][0])),2))
        else:
            stream_all["fl_svr"]="-"
        if stream_all["fl_svr"]!="-" and stream_all["fl_pvr"]!="-":
            stream_all["fl_rprs"]= str(round((float(stream_all["fl_pvr"])/float(stream_all["fl_svr"])),2))
        else:
            stream_all["fl_rprs"]= "-"
    else:
        stream_all["fl_qp"]="-"
        stream_all["fl_qep"]="-"
        stream_all["fl_qs"]="-"
        stream_all["fl_qes"]="-"
        stream_all["fl_qpqs"]="-"
        stream_all["fl_qepqes"]="-"
        stream_all["fl_qepqs"]="-"
        stream_all["fl_pvr"]="-"
        stream_all["fl_svr"]="-"
        stream_all["fl_rprs"]="-"
    return stream_all


if __name__ == '__main__':
    app.run(debug=True)


