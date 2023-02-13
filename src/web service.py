import os

from flask import*
from werkzeug.utils import secure_filename
from datetime import datetime
from src.myknn_can import prep1
from clasification import test_classifier
app=Flask(__name__)
from src.myknn import prep
import pymysql
con=pymysql.connect(host="localhost" ,user="root" ,password="" ,port=3306 ,db="virtual doctor")
cmd=con.cursor()




@app.route('/login',methods=['POST'])
def login():
    try:
        con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
        cmd = con.cursor()
        uname=request.form['username']
        passwd=request.form['password']
        cmd.execute("select * from login where username='"+uname+"' and password='"+passwd+"' and user_type='user'")
        s=cmd.fetchone()
        print(s)
        if s is  not None:
            id=s[0]
            print(id)
            return jsonify({'task':str(id)})
        else:
            return jsonify({'task':"error"})
    except Exception as e:
            print(str(e))
            return jsonify({'task':"error"})




@app.route('/register', methods=['get', 'post'])
def register():
   fname=request.form['fname']
   lname = request.form['lname']
   gender = request.form['gender']
   dob = request.form['dob']
   place = request.form['place']
   post = request.form['post']
   pin = request.form['pin']
   phone = request.form['phone']
   email = request.form['email']
   username=request.form['username']
   password = request.form['password']
   cmd.execute("select username from login where username='"+username+"' ")
   un=cmd.fetchone();
   if un is None:
       cmd.execute("insert into login values(null,'"+username+"','"+password+"','user')")
       id=con.insert_id()
       cmd.execute("insert into user_register values(null,'"+str(id)+"','"+fname+"','"+lname+"','"+gender+"','"+dob+"','"+place+"','"+post+"','"+pin+"','"+phone+"','"+email+"')")
       con.commit()
       return jsonify({'task': "success"})
   else:
       return jsonify({'task': "username already existing"})



@app.route('/alarm', methods=['get', 'post'])
def alarm():
   d=request.form['date']
   m = request.form['med']
   t1 = request.form['time']
   t2 = request.form['time2']
   t3 = request.form['time3']
   da = request.form['days']
   ti = request.form['times']
   p = request.form['prescription']
   u = request.form['uid']
   cmd.execute("insert into presrp_details values('"+str(u)+"','"+m+"','"+ti+"','"+t1+"','"+t2+"','"+t3+"','"+p+"','"+da+"','"+d+"')")
   con.commit()
   return jsonify({'task': "success"})




@app.route('/check', methods=['GET','post'])
def check():
    pid = request.form['l_id']
    print(pid)
    res=""
    cmd.execute("SELECT * FROM `presrp_details` WHERE `t1`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t2`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t3`=TIME_FORMAT(CURTIME(),'%h:%i:%p') and pid='"+pid+"'")
    print("SELECT * FROM `presrp_details` WHERE `t1`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t2`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t3`=TIME_FORMAT(CURTIME(),'%h:%i:%p') and pid='" + pid + "'")
    s=cmd.fetchone()
    print(s)
    if s is not None:
        print("SELECT * FROM `presrp_details` WHERE `t1`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t2`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t3`=TIME_FORMAT(CURTIME(),'%h:%i:%p') and pid='" + pid + "'")

        cmd.execute(
            "SELECT * FROM `presrp_details` WHERE `t1`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t2`=TIME_FORMAT(CURTIME(),'%h:%i:%p') OR `t3`=TIME_FORMAT(CURTIME(),'%h:%i:%p') and pid='" + pid + "'")
        s1=cmd.fetchall()
        if s1 is not None:
            for i in s1:
                res = res + str(i[0]) + "#" + str(i[1]) + "#" + str(i[2]) + "#" + str(i[3]) + "#" + str(i[4]) + "#" + str(i[5])+ "#" +str(i[6]) + "#" + str(i[7]) + "#" + str(i[8]) + "@"
            print(res)
            return jsonify({'task':res})
        else:
            print("invalid")
            return jsonify({'task':"invalid"})
    else:
        return jsonify({'task': "invalid"})



@app.route('/add_complaint', methods=['get', 'post'])
def complaint():
   complaint=request.form['complaint']
   lid = request.form['lid']
   print(lid)
   cmd.execute("insert into complaint values(null,'"+str(lid)+"','" +complaint+ "',curdate(),'pending')")
   con.commit()
   return jsonify({'task': "success"})



@app.route('/feedback', methods=['get', 'post'])
def feedback():
   feedback=request.form['feedback']
   lid = request.form['lid']
   rate=request.form['rate']
   hid=request.form['hid']
   cmd.execute("insert into feedback values(null,'"+str(lid)+"','" +feedback+ "',curdate(),'"+str(hid)+"','"+rate+"')")
   con.commit()
   return jsonify({'task': "success"})




@app.route('/feedback1', methods=['get', 'post'])
def feedback1():
   feedback=request.form['feedback']
   lid = request.form['lid']
   rate=request.form['rate']
   cmd.execute("insert into feedback values(null,'"+str(lid)+"','" +feedback+ "',curdate(),0,'"+rate+"')")
   con.commit()
   return jsonify({'task': "success"})




@app.route('/room_booking', methods=['get','post'])
def room_booking():
    hid=request.form['hid']
    roomtype = request.form['rtype']
    date = request.form['date']
    uid = request.form['uid']
    cmd.execute("insert into room_booking values(null,'"+uid+"','"+hid+"','"+date+"','"+roomtype+"','pending')")
    con.commit()
    return jsonify({'task':'success'})




@app.route('/booking', methods=['get', 'post'])
def booking():
   date = request.form['date']
   did=request.form['did']
   print(did,"didddd")
   lid=request.form['lid']
   cmd.execute("insert into booking values(null,'"+str(did)+"','"+str(lid)+"','" +date+ "','pending')")
   con.commit()
   return jsonify({'task': "success"})




@app.route('/order', methods=['get', 'post'])
def order():
   did = request.form['mid']
   q=request.form['quatity']
   print(did, "didddd")
   lid = request.form['uid']
   cmd.execute("INSERT INTO `order` VALUES(null,'" + str(lid) + "','" + str(did) + "',curdate(),'pending','"+q+"')")
   con.commit()
   return jsonify({'task': "success"})


       # views


@app.route('/nearest_pharmacy', methods=['get','post'])
def nearest_pharmacy():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    latitude=request.form['latitude']
    longitude = request.form['longitude']
    cmd.execute("SELECT `pharmacy`.* , (3959 * ACOS ( COS ( RADIANS('" + str(latitude) + "') ) * COS( RADIANS( `location`.latitude) ) * COS( RADIANS( `location`.`longitude` ) - RADIANS('" + str(longitude) + "') ) + SIN ( RADIANS('" + str(latitude) + "') ) * SIN( RADIANS( `location`.`latitude` ) ))) AS user_distance FROM `location` JOIN `pharmacy` ON `pharmacy`.`login_id`=`location`.`login_id` WHERE `pharmacy`.`b_ub`='using' HAVING user_distance  < 6.2137")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)



@app.route('/pharmacy_profile', methods=['get','post'])
def pharmacy_profile():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    pid=request.form['pid']
    cmd.execute("select * from pharmacy where pharmacy_id='"+str(pid)+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)




@app.route('/nearest_lab', methods=['get','post'])
def nearest_lab():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    latitude=request.form['latitude']
    longitude = request.form['longitude']
    cmd.execute("SELECT `lab`.* , (3959 * ACOS ( COS ( RADIANS('" + str(latitude) + "') ) * COS( RADIANS( `location`.latitude) ) * COS( RADIANS( `location`.`longitude` ) - RADIANS('" + str(longitude) + "') ) + SIN ( RADIANS('" + str(latitude) + "') ) * SIN( RADIANS( `location`.`latitude` ) ))) AS user_distance FROM `location` JOIN `lab` ON `lab`.`login_id`=`location`.`login_id` WHERE `lab`.`b_ub`='using' HAVING user_distance  < 6.2137")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)



@app.route('/lab_profile', methods=['get','post'])
def lab_profile():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    lid=request.form['lid']
    cmd.execute("select * from lab where lab_id='"+str(lid)+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)



@app.route('/hospital_profile', methods=['get','post'])
def hospital_profile():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    hid=request.form['hid']
    cmd.execute("select * from hospital where hospital_id='"+str(hid)+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)



@app.route('/viewall', methods=['get','post'])
def viewall():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    print(latitude,longitude)
    cmd.execute("SELECT `hospital`.* , (3959 * ACOS ( COS ( RADIANS('" + str(latitude) + "') ) * COS( RADIANS( `location`.latitude) ) * COS( RADIANS( `location`.`longitude` ) - RADIANS('" + str(longitude) + "') ) + SIN ( RADIANS('" + str(latitude) + "') ) * SIN( RADIANS( `location`.`latitude` ) ))) AS user_distance FROM `location` JOIN `hospital` ON `hospital`.`login_id`=`location`.`login_id` WHERE `hospital`.`b_ub`='using' HAVING user_distance  < 6.2137")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)




@app.route('/viewlocation', methods=['get','post'])
def viewlocation():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    id= request.form['hid']
    print(id)
    cmd.execute("select * from location where login_id='"+id+"'")
    s = cmd.fetchone()
    print(s)
    return jsonify({'lati':s[2],'longi':s[3]})




@app.route('/view_hospital', methods=['get','post'])
def view_hospital():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    print(latitude,longitude)
    hospitalname = request.form['name']
    cmd.execute("select * from hospital where name like '%"+hospitalname+"%' and `b_ub`='using'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)





@app.route('/view_department', methods=['get','post'])
def view_department():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    hospital_id=request.form['hospital_id']
    cmd.execute("select*from department where hospital_id='"+hospital_id+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)





@app.route('/view_facility', methods=['get','post'])
def view_facility():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()

    hospital_id=request.form['hospital_id']
    print(hospital_id)
    cmd.execute("select*from facility where login_id='"+hospital_id+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)





@app.route('/view_replay', methods=['get','post'])
def view_replay():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    user_id=request.form['uid']
    cmd.execute("select*from complaint where login_id='"+user_id+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)





@app.route('/doctor_profile', methods=['get','post'])
def doctor_profile():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    doc_id=request.form['did']
    cmd.execute("select*from doctor where hospital_id='"+doc_id+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)




@app.route('/viewdoctor', methods=['get','post'])
def viewdoctor():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    hid = request.form['hospital_id']
    print(hid)
    cmd.execute("select * from doctor where hospital_id='"+hid+"' ")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)



@app.route('/viewfeedback', methods=['get','post'])
def viewfeedback():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    tid=request.form['hid']
    print(tid,"tidddd")
    cmd.execute("select * from feedback where to_id='"+tid+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)




@app.route('/location', methods=['get','post'])
def location():
    lab_id=request.form['lid']
    cmd.execute("select*from location where pharmacy_id='"+lab_id+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)








@app.route('/available_test', methods=['get','post'])
def available_test():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    lab_id=request.form['laid']
    print(lab_id,"lllllllllll")
    cmd.execute("select*from test where lab_id='"+lab_id+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)





@app.route('/view_booking_status', methods=['get','post'])
def view_booking_status():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    uid=request.form['uid']
    cmd.execute("SELECT `doctor`.`fname`,`lname`,`booking`.`date`,`status` FROM `booking` JOIN `doctor` ON `doctor`.`login_id`=`booking`.`doctor_id` WHERE `booking`.`user_id`='"+uid+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)\





@app.route('/view_order_status', methods=['get','post'])
def view_order_status():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    uid=request.form['uid']
    cmd.execute("SELECT `pharmacy`.`name`,`order`.`status`,`medicine`.* FROM `pharmacy` JOIN `medicine` ON `medicine`.`pharmacy_id`=`pharmacy`.`login_id` JOIN `order` ON `medicine`.`medicine_id`=`order`.`medicine_id` WHERE `order`.`user_id`='"+uid+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)



@app.route('/view_room_booking_status', methods=['get','post'])
def view_room_booking_status():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    uid=request.form['uid']
    cmd.execute("SELECT `hospital`.`name`,`room_booking`.* FROM `hospital` JOIN `room_booking` ON `room_booking`.`hospital_id`=`hospital`.`login_id` WHERE `room_booking`.`login_id`='"+uid+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)






@app.route('/medicine', methods=['get','post'])
def medicine():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    uid=request.form['uid']
    print(uid)
    cmd.execute("select * from medicine where pharmacy_id='"+str(uid)+"'")
    s = cmd.fetchall()
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)




@app.route('/view_amount', methods=['get','post'])
def view_amount():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    mid=request.form['mid']
    qty= request.form['qty']
    cmd.execute("SELECT `price` FROM `medicine` WHERE `medicine_id`='"+mid+"'")
    s = cmd.fetchone()
    pr=s[0]
    amt=int(pr)*int(qty)
    print(amt)
    return jsonify({'task':amt})




@app.route('/check_payment', methods=['get','post'])
def check_payment():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    ifsc=request.form['ifsc_code']
    pin= request.form['pin']
    accno = request.form['account_no']
    amt = request.form['amount']
    print("select * from bank where ifsc_code='"+ifsc+"' and pin='"+pin+"'and account_no='"+accno+"' ")
    cmd.execute("select * from bank where ifsc_code='"+ifsc+"' and pin='"+pin+"'and account_no='"+accno+"' ")
    s = cmd.fetchone()
    print(s)
    if s is None:
        return jsonify({'task':'invalid account'})
    else:
        amt1=s[5]
        id=s[0]
        if int(amt1)>int(amt):
            blce=int(amt1)-int(amt)
            cmd.execute("update bank set amount='"+str(blce)+"' where bank_id='"+str(id)+"'")
            con.commit()
        else:
            return jsonify({'task': 'insufficient amount'})
        return jsonify({'task':'success'})




@app.route('/prediction', methods=['get','post'])
def prediction():
    fil = request.files['files']
    fn = secure_filename(fil.filename)
    fil.save(os.path.join("/static/prediction", fn))
    return "ok"




@app.route('/viewsymptoms', methods=['POST'])
def viewsymptoms():

   cmd.execute("SELECT DISTINCT `Symptoms` FROM `symptoms`")
   row_headers = [x[0] for x in cmd.description]
   results = cmd.fetchall()
   print(results)
   json_data = []
   for result in results:
       json_data.append(dict(zip(row_headers, result)))
   con.commit()
   print(json_data)
   return jsonify(json_data)




@app.route('/disease_predict',methods=['GET','POST'])
def disease_predict():
    con = pymysql.connect(host='localhost', port=3306, user='root', password='', db='virtual doctor')
    cmd = con.cursor()
    data = request.form['symptoms'].lower()
    print("aaa",data)
    data = str(data).split('#')
    print(data)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!",len(data))
    if len(data)>3:
        print(data[0],data[1])
        if data[0]!=data[1]:
            cmd.execute("select distinct Symptoms from symptoms order by id")
            s = cmd.fetchall()
            listdata = []
            for r in s:
                listdata.append(r[0].lower())
            row = []
            print(data,"=====================>")
            for r in listdata:
                print(r,"**************************")
                if r in data:
                    row.append(1.0)
                else:
                    row.append(0.0)
            print(row)
            res = prep(row)
            cmd.execute("select * from disease where id=" + str(res))
            s = cmd.fetchone()
            print("result",s)
            disease=s[1]
            des=s[2]
            medicine=s[3]
            return jsonify({"task":disease+"#"+des+"#"+medicine})
        else:
            print("same")
            return jsonify({"task": "same"})
    else:
        return jsonify({"task": "Normal"})





@app.route('/lcp',methods=['GET','POST'])
def lcp():
    img=request.files['files']
    fn=datetime.now().strftime("%Y%d%m%H%M%S")+",jpg"
    img.save("static/lcp/"+fn)
    res=prep1("static/lcp/"+fn)
    if str(res[0])=="1":
        print(res)
        return jsonify({"task": "Cancer Detected"})
    else:
        print(res)
        return jsonify({"task": "Normal"})



if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)