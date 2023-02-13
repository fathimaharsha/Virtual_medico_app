from flask_mail import Mail
from flask import*
app=Flask(__name__)
import pymysql
app.secret_key="123"
con=pymysql.connect(host="localhost" ,user="root" ,password="" ,port=3306 ,db="virtual doctor")
cmd=con.cursor()

import smtplib
from email.mime.text import MIMEText

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'virtualmedicoo@gmail.com'
app.config['MAIL_PASSWORD'] = 'iam ironman'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


            # admin module


@app.route('/')
def main():
    return render_template("admin login.html")

@app.route('/home')
def home():
    cmd.execute("SELECT t1.count_1,t2.count_2 , t3.count_3 FROM ( SELECT COUNT(1) AS count_1 FROM `login` JOIN `hospital` ON `hospital`.`login_id`=`login`.`login_id` WHERE `user_type`='pending') AS t1, ( SELECT COUNT(1) AS count_2 FROM `login` JOIN `pharmacy` ON  `pharmacy`.`login_id`=`login`.`login_id` WHERE `user_type`='pending') AS t2, ( SELECT COUNT(1) AS count_3 FROM `login` JOIN `lab` ON `lab`.`login_id`=`login`.`login_id` WHERE `user_type`='pending') AS t3")
    s=cmd.fetchone()
    d=[s[0],s[1],s[2]]
    i=0
    while i<3:
        if d[i]<1:
            d[i]=""
        i+=1
    return render_template("admin home.html",val=d)


@app.route('/viewhospital')
def viewhospital():
    cmd.execute("SELECT `hospital`.* FROM `hospital` JOIN `login` ON `login`.`login_id`=`hospital`.`login_id` where user_type='hospital'")
    s=cmd.fetchall()
    return render_template("admin view hospital.html",val=s)


@app.route('/delete')
def delete():
    id=request.args.get('id')
    cmd.execute("SELECT `hospital`.`email` FROM `hospital` JOIN `login` ON `login`.`login_id`=`hospital`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("delete from hospital where login_id='"+id+"'")
    cmd.execute("delete from doctor where hospital_id='"+id+"'")
    cmd.execute("delete from login where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your hospital account is no more available")
    print(msg)
    msg['Subject'] = 'account deleted'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('deleted');window.location='/viewhospital'</script>'''



@app.route('/block')
def block():
    id=request.args.get('id')
    cmd.execute("SELECT `hospital`.`email` FROM `hospital` JOIN `login` ON `login`.`login_id`=`hospital`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='pending' where login_id='"+id+"'")
    cmd.execute("update doctor set b_ub='blocked' where hospital_id='" + id + "'")


    cmd.execute("SELECT `doctor`.`login_id` FROM `doctor` JOIN `hospital` ON `doctor`.`hospital_id`=`hospital`.`login_id` WHERE `hospital`.`login_id`='" + id + "'")
    s = cmd.fetchall()
    for i in s:
        cmd.execute("update login set user_type='blocked' where login_id='" + str(i[0]) + "'")
        con.commit()
    cmd.execute("update hospital set b_ub='blocked' where login_id='" + id + "'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your hospital account is temporarily suspended")
    print(msg)
    msg['Subject'] = 'account blocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('account blocked');window.location='/viewhospital'</script>'''


@app.route('/unblock')
def unblock():
    id=request.args.get('id')
    cmd.execute("SELECT `hospital`.`email` FROM `hospital` JOIN `login` ON `login`.`login_id`=`hospital`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='hospital' where login_id='"+id+"'")
    cmd.execute("update doctor set b_ub='using' where hospital_id='" + id + "'")
    cmd.execute("SELECT `doctor`.`login_id` FROM `doctor` JOIN `hospital` ON `doctor`.`hospital_id`=`hospital`.`login_id` WHERE `hospital`.`login_id`='"+id+"'")
    s=cmd.fetchall()
    for i in s:
        cmd.execute("update login set user_type='doctor' where login_id='"+str(i[0])+"'")
        con.commit()
    cmd.execute("update hospital set b_ub='using' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your hospital account is reusable")
    print(msg)
    msg['Subject'] = 'account unblocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('unblocked');window.location='/viewhospital'</script>'''



@app.route('/viewpharmacy')
def viewpharmacy():
    cmd.execute("SELECT `pharmacy`.* FROM `pharmacy` JOIN `login` ON `login`.`login_id`=`pharmacy`.`login_id` where user_type='pharmacy'")
    s=cmd.fetchall()
    return render_template("admin view pharmacy.html",val=s)


@app.route('/deletepp')
def deletepp():
    id=request.args.get('id')
    cmd.execute("SELECT `pharmacy`.`email` FROM `pharmacy` JOIN `login` ON `login`.`login_id`=`pharmacy`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("delete from pharmacy where login_id='"+id+"'")
    cmd.execute("delete from login where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your pharmacy account is no more available")
    print(msg)
    msg['Subject'] = 'account deleted'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('deleted');window.location='/viewpharmacy'</script>'''


@app.route('/blockp')
def blockp():
    id=request.args.get('id')
    cmd.execute("SELECT `pharmacy`.`email` FROM `pharmacy` JOIN `login` ON `login`.`login_id`=`pharmacy`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='pending' where login_id='"+id+"'")
    cmd.execute("update pharmacy set b_ub='blocked' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your pharmacy account is temporarily suspended")
    print(msg)
    msg['Subject'] = 'account blocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('account blocked');window.location='/viewpharmacy'</script>'''


@app.route('/unblockp')
def unblockp():
    id=request.args.get('id')
    cmd.execute("SELECT `pharmacy`.`email` FROM `pharmacy` JOIN `login` ON `login`.`login_id`=`pharmacy`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='pharmacy' where login_id='"+id+"'")
    cmd.execute("update pharmacy set b_ub='using' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your pharmacy account is reusable")
    print(msg)
    msg['Subject'] = 'account unblocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('unblocked');window.location='/viewpharmacy'</script>'''



@app.route('/viewlab')
def viewlab():
    cmd.execute("SELECT `lab`.* FROM `lab` JOIN `login` ON `login`.`login_id`=`lab`.`login_id` where user_type='lab'")
    s=cmd.fetchall()
    return render_template("admin view lab.html",val=s)


@app.route('/deletela')
def deletela():
    id=request.args.get('id')
    cmd.execute("SELECT `lab`.`email` FROM `lab` JOIN `login` ON `login`.`login_id`=`lab`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("delete from lab where login_id='"+id+"'")
    cmd.execute("delete from login where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your lab account is no more available")
    print(msg)
    msg['Subject'] = 'account deleted'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('deleted');window.location='/viewlab'</script>'''



@app.route('/blockl')
def blockl():
    id=request.args.get('id')
    cmd.execute("SELECT `lab`.`email` FROM `lab` JOIN `login` ON `login`.`login_id`=`lab`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='pending' where login_id='"+id+"'")
    cmd.execute("update lab set b_ub='blocked' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your lab account is temporarily suspended")
    print(msg)
    msg['Subject'] = 'account blocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('account blocked');window.location='/viewlab'</script>'''


@app.route('/unblockl')
def unblockl():
    id=request.args.get('id')
    cmd.execute("SELECT `lab`.`email` FROM `lab` JOIN `login` ON `login`.`login_id`=`lab`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='lab' where login_id='"+id+"'")
    cmd.execute("update lab set b_ub='using' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your lab account is reusable")
    print(msg)
    msg['Subject'] = 'account unblocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('unblocked');window.location='/viewlab'</script>'''


@app.route('/notification')
def notification():
    return render_template("admin notification.html")

@app.route('/noti', methods=['get', 'post'])
def noti():
    id=0
    notification=request.form['notification']
    cmd.execute("insert into notification values(null,'"+notification+"',curdate(),'"+str(id)+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/home'</script>'''



@app.route('/view_notification')
def view_notification():
    cmd.execute("select*from notification where hospital_id=0")
    s = cmd.fetchall()
    return render_template("admin view notification.html", val=s)



@app.route('/deletenoti')
def deletenoti():
    id=request.args.get('id')
    cmd.execute("delete from notification where notification_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/view_notification'</script>'''



@app.route('/hospitala')
def hospitala():
    cmd.execute("SELECT `hospital`.* FROM `hospital` JOIN `login` ON `hospital`.`login_id`=`login`.`login_id` WHERE `login`.`user_type`='pending'")
    res=cmd.fetchall()
    return render_template("admin approve hospital.html",val=res)



@app.route('/deleteh')
def deleteh():
    id=request.args.get('id')
    cmd.execute("SELECT `hospital`.`email` FROM `hospital` JOIN `login` ON `login`.`login_id`=`hospital`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("delete from hospital where login_id='"+id+"'")
    cmd.execute("delete from login where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("sorry! there is some troubleshoot in your hospital registration."
                   "please try to register again.")
    print(msg)
    msg['Subject'] = 'registration rejected'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('rejected');window.location='/hospitala'</script>'''



@app.route('/approveh')
def approveh():
    id=request.args.get('id')
    cmd.execute("SELECT `hospital`.`email` FROM `hospital` JOIN `login` ON `login`.`login_id`=`hospital`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email=em[0]
    print(email)
    cmd.execute("update login set user_type='hospital' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("welcome to virtual medico family."
                   "now onwards you can use your hospital account by using your username and password.")
    print(msg)
    msg['Subject'] = 'registration approved'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully approved');window.location='/hospitala'</script>'''



@app.route('/pharmacy')
def pharmacy():
    cmd.execute("SELECT `pharmacy`.* FROM `pharmacy` JOIN `login` ON `pharmacy`.`login_id`=`login`.`login_id` WHERE `login`.`user_type`='pending'")
    res=cmd.fetchall()
    return render_template("admin approve pharmacy.html",val=res)


@app.route('/deletep')
def deletep():
    id=request.args.get('id')
    cmd.execute("SELECT `pharmacy`.`email` FROM `pharmacy` JOIN `login` ON `login`.`login_id`=`pharmacy`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("delete from pharmacy where login_id='"+id+"'")
    cmd.execute("delete from login where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("sorry! there is some troubleshoot in your pharmacy registration."
                   "please try to register again.")
    print(msg)
    msg['Subject'] = 'registration rejected'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('rejected');window.location='/pharmacy'</script>'''


@app.route('/approvep')
def approvep():
    id=request.args.get('id')
    cmd.execute("SELECT `pharmacy`.`email` FROM `pharmacy` JOIN `login` ON `login`.`login_id`=`pharmacy`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email=em[0]
    print(email)
    cmd.execute("update login set user_type='pharmacy' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("welcome to virtual medico family."
                   "now onwards you can use your pharmacy account by using your username and password.")
    print(msg)
    msg['Subject'] = 'registration approved'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully approved');window.location='/pharmacy'</script>'''


@app.route('/alab')
def alab():
    cmd.execute("SELECT `lab`.* FROM `lab` JOIN `login` ON `lab`.`login_id`=`login`.`login_id` WHERE `login`.`user_type`='pending'")
    res=cmd.fetchall()
    return render_template("admin approve lab.html",val=res)

@app.route('/deletel')
def deletel():
    id=request.args.get('id')
    cmd.execute("SELECT `lab`.`email` FROM `lab` JOIN `login` ON `login`.`login_id`=`lab`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("delete from lab where login_id='"+id+"'")
    cmd.execute("delete from login where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("sorry! there is some troubleshoot in your lab registration."
                   "please try to register again.")
    print(msg)
    msg['Subject'] = 'registration rejected'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('rejected');window.location='/alab'</script>'''


@app.route('/approvel')
def approvel():
    id=request.args.get('id')
    cmd.execute("SELECT `lab`.`email` FROM `lab` JOIN `login` ON `login`.`login_id`=`lab`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email=em[0]
    print(email)
    cmd.execute("update login set user_type='lab' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("welcome to virtual medico family."
                   "now onwards you can use your lab account by using your username and password.")
    print(msg)
    msg['Subject'] = 'registration approved'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully approved');window.location='/alab'</script>'''


@app.route('/admin_wfeed')
def admin_wfeed():
    return render_template("admin who's feed.html")


@app.route('/admin_feedback')
def admin_feedback():
    type=request.args.get('type')
    if type=='hospital':
        cmd.execute("SELECT `feedback`.`date`,`hospital`.`name`,`feedback`.`feedback` FROM  `feedback` JOIN `hospital` ON `hospital`.`login_id`=`feedback`.`login_id`")
        s=cmd.fetchall()
        return render_template("admin view feedback.html", val=s)

    elif type=="pharmacy":
        cmd.execute("SELECT `feedback`.`date`,`pharmacy`.`name`,`feedback`.`feedback` FROM  `feedback` JOIN `pharmacy` ON `pharmacy`.`login_id`=`feedback`.`login_id`")
        s = cmd.fetchall()
        return render_template("admin view feedback.html", val=s)

    elif type == "lab":
        cmd.execute("SELECT `feedback`.`date`,`lab`.`name`,`feedback`.`feedback` FROM  `feedback` JOIN `lab` ON `lab`.`login_id`=`feedback`.`login_id`")
        s = cmd.fetchall()
        return render_template("admin view feedback.html", val=s)

    elif type == "user":
        cmd.execute("SELECT `feedback`.`date`,`user_register`.`fname`,`feedback`.`feedback` FROM  `feedback` JOIN `user_register` ON `user_register`.`login_id`=`feedback`.`login_id` where to_id=0")
        s = cmd.fetchall()
        return render_template("admin view feedback.html", val=s)






@app.route('/admin_complaint')
def admin_complaint():
        cmd.execute("SELECT `complaint`.`date`,`complaint`,`user_register`.`fname`,complaint.`complaint_id` FROM  `complaint` JOIN `user_register` ON `user_register`.`login_id`=`complaint`.`login_id` where `complaint`.`reply`='pending' ")
        s = cmd.fetchall()
        return render_template("admin manage complaint.html", val=s)






@app.route('/admin_replay',methods=['get'])
def admin_replay():
    id=request.args.get('id')
    session['id']=id
    return render_template("admin replay.html")



@app.route('/adreplay', methods=['get','post'])
def adreplay():
    id=session['id']
    replay=request.form['replay']
    cmd.execute("update complaint set reply='"+replay+"' where complaint_id='"+str(id)+"'")
    con.commit()
    return '''<script>alert('successfully added');window.location='/home'</script>'''



            # doctor module


@app.route('/doctor')
def doctor():
    id = session['lid']
    cmd.execute("select count(booking_id) as numberofbooking from booking WHERE `booking`.`doctor_id`='"+str(session['lid'])+"' and status='pending'")
    s=cmd.fetchone()
    b=[s[0]]
    if b[0]<1:
        b[0]=""
    return render_template("doctor home.html",val=b)

@app.route('/new_profile')
def new_profile():
    id=session['lid']
    print(id)
    cmd.execute("select *from doctor where login_id='"+str(id)+"'")
    s=cmd.fetchone()
    print("it is here"+str(s))
    return render_template("doctor new profile.html",val=s)


@app.route('/newprofile', methods=['get','post'])
def newprofile():
    fname=request.form['fname']
    lname=request.form['lname']
    photo=request.files['photo']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/dr/"+fn)
    gender=request.form['gender']
    qualification=request.form['qualification']
    specialization=request.form['specialization']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    duty = request.form['duty']
    lid=session['lid']
    cmd.execute("update doctor set fname='"+fname+"',lname='"+lname+"',gender='"+gender+"',qualification='"+qualification+"',specialization='"+specialization+"',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',phone='"+phone+"',dob='"+dob+"',profile_photo='"+fn+"',duty_time='"+duty+"' where login_id='"+str(lid)+"'")
    con.commit()
    return '''<script>alert('successfully updated');window.location='/doctor'</script>'''


@app.route('/patient')
def patient():
    cmd.execute("SELECT `user_register`.*,`booking`.`booking_id` FROM`user_register`JOIN`booking`ON`booking`.`user_id`=`user_register`.`login_id`WHERE `booking`.`doctor_id`='"+str(session['lid'])+"' AND `booking`.`status`='not_consulted'")
    s=cmd.fetchall()
    return render_template("doctor view patient.html",val=s)


@app.route('/mpatient')
def mpatient():
    cmd.execute("SELECT `user_register`.* FROM`user_register`JOIN`booking`ON`booking`.`user_id`=`user_register`.`login_id`WHERE `booking`.`doctor_id`='"+str(session['lid'])+"' AND `booking`.`status`='consulted'")
    s=cmd.fetchall()
    return render_template("doctor my patients.html",val=s)



@app.route('/doctor_booking')
def doctor_booking():
    print(session['lid'])
    cmd.execute("SELECT `user_register`.`fname`,`user_register`.`lname`,`booking`.* FROM `booking` JOIN `user_register` ON `user_register`.`login_id`=`booking`.`user_id` WHERE `booking`.`doctor_id`='"+str(session['lid'])+"' AND `booking`.`status`='pending'")
    s=cmd.fetchall()
    print(s)
    return render_template("doctor view booking.html",val=s)

#do

@app.route('/deleteb')
def deleteb():
    id=request.args.get('id')
    did = session['lid']
    cmd.execute("SELECT `doctor`.`fname`,`doctor`.`lname`,`hospital`.`name` FROM `hospital` JOIN `doctor` ON `doctor`.`hospital_id`=`hospital`.`login_id` WHERE `doctor`.`login_id`='"+str(did)+"'")
    s=cmd.fetchone()
    cmd.execute("SELECT `booking`.*,`user_register`.`fname`,`user_register`.`lname`,`user_register`.`email` FROM `user_register` INNER JOIN `booking` ON `booking`.`user_id`=`user_register`.`login_id` WHERE `booking`.`doctor_id`='"+str(did)+"' AND `booking`.`status`='pending'")
    print("SELECT user_register.* FROM `user_register` JOIN `login` ON `login`.`login_id`=`user_register`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    print("dfghjkl;",em)
    print(em[7],"email")
    cmd.execute("delete from booking where booking_id='" + id + "'")
    con.commit()
    # print(email)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com','iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your appointment with our doctor was denied due certain issues"+"\n"+"by :"+s[0]+"."+s[1]+"\n"+" from :"+s[2])
    print(msg)
    msg['Subject'] = 'doctor booking denied'
    msg['To'] = str(em[7])
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully rejected');window.location='/doctor_booking'</script>'''


#do


@app.route('/approveb')
def approveb():
    did=session['lid']
    print(did,"===========")
    id = request.args.get('id')
    cmd.execute("SELECT `doctor`.`fname`,`doctor`.`lname`,`hospital`.`name` FROM `hospital` JOIN `doctor` ON `doctor`.`hospital_id`=`hospital`.`login_id` WHERE `doctor`.`login_id`='"+str(did)+"'")
    s=cmd.fetchone()
    print(s,"ssssssssssss")
    cmd.execute("SELECT `booking`.*,`user_register`.`fname`,`user_register`.`lname`,`user_register`.`email` FROM `user_register` INNER JOIN `booking` ON `booking`.`user_id`=`user_register`.`login_id` WHERE `booking`.`doctor_id`='"+str(did)+"' AND `booking`.`status`='pending'")
    print("SELECT user_register.* FROM `user_register` JOIN `login` ON `login`.`login_id`=`user_register`.`login_id` WHERE `login`.`login_id`='" + id + "'")
    em = cmd.fetchone()
    print(em)
    print(em[7], "email")
    cmd.execute("update booking set status='not_consulted' where booking_id='" + id + "'")
    con.commit()
    # print(email)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your appointment with our doctor is accepted"+"\n"+"by :"+s[0]+"."+s[1]+"\n"+" from :"+s[2])
    print(msg)
    msg['Subject'] = 'booking approved'
    msg['To'] = str(em[7])
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully approved');window.location='/doctor_booking'</script>'''





@app.route('/con_d')
def con_d():
    id=request.args.get('id')
    print(id)
    cmd.execute("update booking set status='consulted' where booking_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully added');window.location='/patient'</script>'''


@app.route('/ncon_d')
def ncon_d():
    id=request.args.get('id')
    print(id)
    cmd.execute("update booking set status='not_visited' where booking_id='"+id+"'")
    con.commit()
    return '''<script>alert('done');window.location='/patient'</script>'''


@app.route('/doctor_complaint')
def doctor_complaint():
    return render_template("doctor add complaint.html")

@app.route('/complaint',methods=['get','post'])
def complaint():
    complaint=request.form['comp']
    cmd.execute("insert into complaint values(null,'"+str(session['lid'])+"','"+complaint+"',curdate(),'pending')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/doctor'</script>'''


@app.route('/doctor_replay')
def doctor_replay():
    cmd.execute("select * from complaint where login_id='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("doctor view replay.html",val=s)



@app.route('/vfd')
def vfd():
    cmd.execute("SELECT `user_register`.`fname`,`lname`,`feedback`.* FROM `feedback` JOIN `user_register` ON `feedback`.`login_id`=`user_register`.`login_id` WHERE `feedback`.`to_id`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("doctor view feedback.html",val=s)



@app.route('/vn')
def vn():
    cmd.execute("SELECT `notification`.* FROM `notification` JOIN `hospital` ON `hospital`.`login_id`=`notification`.`hospital_id`  JOIN `doctor` ON `doctor`.`hospital_id`=`hospital`.`login_id` WHERE `doctor`.`login_id`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    print(s)
    return render_template("doctor view notification.html",val=s)


        # hospital module


@app.route('/hospital_home')
def hospital_home():
    id = session['lid']
    cmd.execute("SELECT COUNT(`room_booking_id`) AS numberofbooking  FROM`room_booking` WHERE `hospital_id`='"+str(session['lid'])+"' AND STATUS='pending'")
    s = cmd.fetchone()
    d = [s[0]]
    if d[0] < 1:
        d[0] = ""
    return render_template("hospital home.html",val=d)


@app.route('/hospital')
def hospital():
    return render_template("admin add hospital.html")


@app.route('/hospital_register', methods=['get', 'post'])
def hospital_register():
    name=request.form['name']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    photo=request.files['proof']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/proof/"+fn)
    username=request.form['username']
    password=request.form['password']
    cmd.execute("select username from login where username='"+username+"' ")
    un=cmd.fetchone();
    if un is None:
        cmd.execute("insert into login values(null,'" + username + "','" + password + "','pending')")
        lid = con.insert_id()
        cmd.execute("insert into hospital values(null,'"+str(lid)+"','"+name+"','"+place+"','"+post+"','" + pin + "','" + email + "','" + phone + "','" + fn + "','using')")
        con.commit()
        return '''<script>alert('successfully added');window.location='/'</script>'''
    else:
        return '''<script>alert('Username already existing!!');window.location='/hospital'</script>'''


@app.route('/hospital_new_profile')
def hospital_new_profile():
    id=session['lid']
    print(id)
    cmd.execute("select*from hospital where login_id='"+str(id)+"'")
    s=cmd.fetchone()
    print(s)
    return render_template("hospital new pro.html",val=s)




@app.route('/hospital_location')
def hospital_location():
    return render_template("hospital add location.html")



@app.route('/hospital_add_location', methods=['get','post'])
def hospital_add_location():
    latitude=request.form['latitude']
    longitude=request.form['longitude']
    place=request.form['place']
    lid =session['lid']
    cmd.execute("insert into location values(null,'"+str(lid)+"','"+latitude+"','"+longitude+"','"+place+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''





@app.route('/ehosp', methods=['get','post'])
def ehosp():
    name=request.form['name']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    photo=request.files['proof']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/proof/"+fn)
    lid=session['lid']
    cmd.execute("update hospital set name='"+name+"',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',phone='"+phone+"',proof='"+fn+"' where login_id='"+str(lid)+"'")
    con.commit()
    return '''<script>alert('successfully updated');window.location='/hospital_home'</script>'''



@app.route('/add_doctor')
def add_doctor():
    return render_template("hospital add doctor.html")


@app.route('/adddoctor', methods=['get','post'])
def adddoctor():
    fname=request.form['fname']
    lname=request.form['lname']
    photo=request.files['photo']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/dr/"+fn)
    dob=request.form['dob']
    gender=request.form['gender']
    qualification=request.form['qualification']
    specialization=request.form['specialization']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phoneno = request.form['phonenumber']
    duty= request.form['duty']
    print(phoneno)
    username = request.form['username']
    password = request.form['password']
    cmd.execute("select username from login where username='"+username+"'")
    un=cmd.fetchone();
    if un is None:
        cmd.execute("insert into login values(null,'" + username + "','" + password + "','doctor')")
        lid = con.insert_id()
        cmd.execute("insert into doctor values(null,'"+str(lid)+"','"+fname+"','"+lname+"','"+gender+"','"+qualification+"','"+specialization+"','"+place+"','"+post+"','"+pin+"','"+email+"','"+phoneno+"','"+dob+"','"+str(session['lid'])+"','using','"+fn+"','"+duty+"')")
        con.commit()
        return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''
    else:
        return '''<script>alert('Username already existing!!');window.location='/add_doctor'</script>'''



@app.route('/manage_doctor')
def manage_doctor():
    id=request.args.get('id')
    cmd.execute("select*from doctor WHERE `hospital_id`='"+str(session['lid'])+"'")
    s = cmd.fetchall()
    return render_template("hospital manage doctor.html", val=s)

#do

@app.route('/blockd')
def blockd():
    ids = session['lid']
    id=request.args.get('id')
    cmd.execute("select name from hospital where login_id='"+str(ids)+"'")
    s = cmd.fetchone()
    print(s, "ssssssssssss")
    cmd.execute("SELECT `doctor`.`email` FROM `doctor` JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='pending' where login_id='"+id+"'")
    cmd.execute("update doctor set b_ub='blocked' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your doctor account is temporarily suspended "+"\n"+"by :"+s[0])
    print(msg)

    msg['Subject'] = 'account blocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('account blocked');window.location='/manage_doctor'</script>'''

#do

@app.route('/unblockd')
def unblockd():
    ids = session['lid']
    id = request.args.get('id')
    cmd.execute("select name from hospital where login_id='"+str(ids)+"'")
    s = cmd.fetchone()
    print(s, "ssssssssssss")
    cmd.execute("SELECT `doctor`.`email` FROM `doctor` JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("update login set user_type='doctor' where login_id='"+id+"'")
    cmd.execute("update doctor set b_ub='using' where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your doctor account is reusable"+"\n"+"by :"+s[0])
    print(msg)
    msg['Subject'] = 'account unblocked'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('unblocked');window.location='/manage_doctor'</script>'''





@app.route('/edit_doctor')
def edit_doctor():
    id = request.args.get('id')
    session['hid']=id
    cmd.execute("select *from doctor where doctor_id='"+id+"'")
    s=cmd.fetchone()
    return render_template("hospital edit doctor.html",val=s)


@app.route('/editdoctor', methods=['get','post'])
def editdoctor():
    fname=request.form['fname']
    lname=request.form['lname']
    photo=request.files['photo']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/dr/"+fn)
    dob=request.form['dob']
    gender=request.form['gender']
    qualification=request.form['qualification']
    specialization=request.form['specialization']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    duty = request.form['duty']
    id = session['hid']
    cmd.execute("update doctor set fname='"+fname+"',lname='"+lname+"',gender='"+gender+"',qualification='"+qualification+"',specialization='"+specialization+"',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',phone='"+phone+"',dob='"+dob+"',profile_photo='"+fn+"',duty_time='"+duty+"' where doctor_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully edited');window.location='/hospital_home'</script>'''

#do

@app.route('/deletedoctor')
def deletedoctor():
    ids = session['lid']
    id = request.args.get('id')
    cmd.execute("select name from hospital where login_id='" + str(ids) + "'")
    s = cmd.fetchone()
    print(s, "ssssssssssss")
    cmd.execute("SELECT `doctor`.`email` FROM `doctor` JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`login_id`='"+id+"'")
    em=cmd.fetchone()
    email = em[0]
    print(email)
    cmd.execute("delete from doctor where login_id='"+id+"'")
    cmd.execute("delete from login where login_id='"+id+"'")
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com', 'iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your doctor account is no more available it is deleted "+"\n"+"by :"+s[0])
    print(msg)
    msg['Subject'] = 'account deleted'
    msg['To'] = email
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/manage_doctor'</script>'''


@app.route('/add_staff')
def add_staff():
    return render_template("hospital add staff.html")

@app.route('/addstaff', methods=['get','post'])
def addstaff():
    fname=request.form['fname']
    lname=request.form['lname']
    gender = request.form['gender']
    dob=request.form['dob']
    qualification=request.form['qualification']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    lid = con.insert_id()
    cmd.execute("insert into staff values(null,'"+str(lid)+"','"+fname+"','"+lname+"','"+gender+"','"+dob+"','"+qualification+"','"+place+"','"+post+"','"+pin+"','"+email+"','"+phone+"','"+str(session['lid'])+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''


@app.route('/manage_staff')
def manage_staff():
    id=request.args.get('id')
    cmd.execute("select*from staff WHERE `hospital_id`='"+str(session['lid'])+"'")
    m=cmd.fetchall()
    return render_template("hospital manage staff.html", val=m)

@app.route('/edit_staff')
def edit_staff():
    id = request.args.get('id')
    session['hid']=id
    cmd.execute("select *from staff where staff_id='"+id+"'")
    s=cmd.fetchone()
    return render_template("hospital edit staff.html",val=s)


@app.route('/editstaff', methods=['get','post'])
def editstaff():
    fname=request.form['fname']
    lname=request.form['lname']
    dob=request.form['dob']
    gender=request.form['gender']
    qualification=request.form['qualification']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    id = session['hid']
    cmd.execute("update staff set fname='"+fname+"',lname='"+lname+"',gender='"+gender+"',qualification='"+qualification+"',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',phone='"+phone+"',dob='"+dob+"' where staff_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully edited');window.location='/hospital_home'</script>'''



@app.route('/deletestaff')
def deletestaff():
    id=request.args.get('id')
    cmd.execute("delete from staff where login_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/manage_staff'</script>'''


@app.route('/add_facility')
def add_facility():
    return render_template("hospital add facility.html")

@app.route('/facility',methods=['get','post'])
def facility():
    facility = request.form['facility']
    description = request.form['description']
    cmd.execute("insert into facility values(null,'"+str(session['lid'])+"','"+facility+"','"+description+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''

@app.route('/view_facility')
def view_facility():
    cmd.execute("select*from facility where login_id='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("hospital view facility.html", val=s)

@app.route('/edit_facility')
def edit_facility():
    id = request.args.get('id')
    session['hid']=id
    cmd.execute("select *from facility where facility_id='"+id+"'")
    s=cmd.fetchone()
    return render_template("hospital edit facility.html",val=s)



@app.route('/editfacility',methods=['get','post'])
def editfacility():
    facility = request.form['facility']
    description = request.form['description']
    id = session['hid']
    cmd.execute("update facility set facility='"+facility+"',description='"+description+"' where facility_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully edited');window.location='/hospital_home'</script>'''


@app.route('/deletefacility')
def deletefacility():
    id=request.args.get('id')
    cmd.execute("delete from facility where facility_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/view_facility'</script>'''


@app.route('/add_department')
def add_department():
    return render_template("hospital add department.html")

@app.route('/add_dept',methods=['get','post'])
def add_dept():
    name = request.form['dept name']
    description = request.form['description']
    lid = session['lid']
    cmd.execute("insert into department values(null,'"+str(lid)+"','"+name+"','"+description+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''


@app.route('/view_department')
def view_department():
    cmd.execute("select*from department where hospital_id='"+str(session['lid'])+"'")
    s = cmd.fetchall()
    return render_template("hospital view department.html", val=s)

@app.route('/edit_department')
def edit_department1():
    id = request.args.get('id')
    session['hid']=id
    cmd.execute("select *from department where department_id='"+id+"'")
    s=cmd.fetchone()
    return render_template("hospital edit department.html",i=s)

@app.route('/edit_dept',methods=['get','post'])
def edit_dept():
    name = request.form['deptname']
    description = request.form['description']
    id=session['hid']
    cmd.execute("update department set name='"+name+"',description='"+description+"' where department_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully updated');window.location='/hospital_home'</script>'''

@app.route('/deletedept')
def deletedept():
    id=request.args.get('id')
    cmd.execute("delete from department where department_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/view_department'</script>'''


@app.route('/hospital_manage_complaint')
def hospital_manage_complaint():
    cmd.execute("SELECT `complaint`.`date`,`complaint`,`doctor`.`fname`,complaint.`complaint_id` FROM  `complaint` JOIN `doctor` ON `doctor`.`login_id`=`complaint`.`login_id` WHERE `hospital_id`='"+str(session['lid'])+"' AND `reply`='pending'")
    s = cmd.fetchall()
    return render_template("hospital manage complaint.html",val=s)



@app.route('/view_booking')
def view_booking():
    cmd.execute("SELECT`doctor`.`fname`,`doctor`.`lname`,`user_register`.`fname`,`user_register`.`lname`,`booking`.`date`,`status`,`booking`.`booking_id` FROM `doctor` JOIN`booking` ON`doctor`.`login_id`=`booking`.`doctor_id` JOIN`user_register` ON `user_register`.`login_id`=`booking`.`user_id` WHERE (`booking`.`status`='not_visited' or `booking`.`status`='consulted') AND `doctor`.`hospital_id`='"+str(session['lid'])+"'")
    res=cmd.fetchall()
    return render_template("hospital view booking.html",val=res)



@app.route('/view_feedb')
def view_feedb():
    cmd.execute("SELECT `user_register`.`fname`,`lname`,`feedback`.* FROM `feedback` JOIN `user_register` ON `feedback`.`login_id`=`user_register`.`login_id` WHERE `feedback`.`to_id`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("hospital view feedback.html",val=s)


@app.route('/addn')
def addn():
    return render_template("Hospital add notification.html")


@app.route('/notif', methods=['get', 'post'])
def notif():
    notification=request.form['notification']
    cmd.execute("insert into notification values(null,'"+notification+"',curdate(),'"+str(session['lid'])+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''


@app.route('/m_noti')
def m_noti():
    cmd.execute("select * from notification where hospital_id='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("Hospital manage notification.html",val=s)



@app.route('/view_not')
def view_not():
    cmd.execute("select * from notification where hospital_id=0")
    s=cmd.fetchall()
    return render_template("Hospital view notification.html",val=s)



@app.route('/add_fee')
def add_fee():
    return render_template("hospital add feedback.html")


@app.route('/hfeedback', methods=['get','post'])
def hfeedback():
    feedback = request.form['feedback']
    lid = con.insert_id()
    cmd.execute("insert into feedback values(null,'"+str(session['lid'])+"','"+feedback+"',curdate(),'0',null)")
    con.commit()
    return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''


@app.route('/view_rb')
def view_rb():
    print(session['lid'])
    cmd.execute("SELECT `room_booking`.`date`,`room_booking`.`room_type`,`user_register`.*,`room_booking`.`room_booking_id`FROM`room_booking`JOIN`user_register`ON`room_booking`.`login_id`=`user_register`.`login_id` JOIN `hospital` ON `hospital`.`login_id`=`room_booking`.`hospital_id` WHERE `room_booking`.`status`='pending'" )
    s=cmd.fetchall()
    print(s)
    return render_template("hospital view room booking.html",val=s)

#do

@app.route('/deleter',methods=['get'])
def deleter():
    idr = session['lid']
    id = request.args.get('id')
    cmd.execute("select name from hospital where login_id='" + str(idr) + "'")
    s = cmd.fetchone()
    print(s, "ssssssssssss")
    cmd.execute("SELECT `user_register`.* FROM `room_booking` JOIN `user_register` ON `room_booking`.`login_id`=`user_register`.`login_id` WHERE `room_booking`.`room_booking_id`='"+str(id)+"'")
    em=cmd.fetchone()
    print(em)
    print(em[10],"email")
    cmd.execute("delete from room_booking where room_booking_id='"+str(id)+"'")
    con.commit()
    # print(email)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com','iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your room booking was denied by"+"\n"+"by :"+s[0])
    print(msg)
    msg['Subject'] = 'room booking denied'
    msg['To'] = str(em[10])
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully denied');window.location='/view_rb'</script>'''

#do

@app.route('/approver',methods=['get'])
def approver():
    idr = session['lid']
    id = request.args.get('id')
    cmd.execute("select name from hospital where login_id='" + str(idr) + "'")
    s = cmd.fetchone()
    print(s, "ssssssssssss")
    cmd.execute("SELECT `user_register`.* FROM `room_booking` JOIN `user_register` ON `room_booking`.`login_id`=`user_register`.`login_id` WHERE `room_booking`.`room_booking_id`='"+str(id)+"'")
    em=cmd.fetchone()
    print(em)
    print(em[10],"email")
    cmd.execute("update room_booking set status='accepted' where room_booking_id='"+str(id)+"'")
    con.commit()
    # print(email)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com','iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your room booking accepted"+"\n"+"by :"+s[0])
    print(msg)
    msg['Subject'] = 'room booking approved'
    msg['To'] = str(em[10])
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully approved');window.location='/view_rb'</script>'''




@app.route('/hospital_replay', methods=['get'])
def hospital_replay():
    id = request.args.get('id')
    session['id'] = id
    return render_template("hospital replay.html")

@app.route('/horeplay', methods=['get', 'post'])
def horeplay():
    id = session['id']
    replay = request.form['replay']
    cmd.execute("update complaint set reply='" + replay + "' where complaint_id='" + str(id) + "'")
    con.commit()
    return '''<script>alert('successfully added');window.location='/hospital_home'</script>'''



@app.route('/deln', methods=['get', 'post'])
def deln():
    id = request.args.get('id')
    cmd.execute("delete from notification where hospital_id='" + str(id) + "'")
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/m_noti'</script>'''



@app.route('/deleteacchosp')
def deleteacchosp():
    id = session['lid']
    print(id)
    cmd.execute("SELECT `doctor`.`login_id` FROM `doctor` JOIN `hospital` ON `doctor`.`hospital_id`=`hospital`.`login_id` WHERE `hospital`.`login_id`='"+str(id)+"'")
    s=cmd.fetchall()
    cmd.execute("delete from department where hospital_id='" + str(id) + "'")
    cmd.execute("delete from feedback where to_id='" + str(id) + "'")
    cmd.execute("delete from location where login_id='" + str(id) + "'")
    cmd.execute("delete from notification where hospital_id='" + str(id) + "'")
    cmd.execute("delete from room_booking where hospital_id='" + str(id) + "'")
    cmd.execute("delete from staff where hospital_id='" + str(id) + "'")
    for i in s:
        print(i,"====================")
        cmd.execute("delete from login where login_id='" + str(i[0]) + "'")
        con.commit()
    cmd.execute("delete from doctor where hospital_id='" + str(id) + "'")
    cmd.execute("delete from hospital where login_id='" + str(id) + "'")
    cmd.execute("delete from login where login_id='" + str(id) + "'")
    cmd.execute("delete from facility where login_id='" + str(id) + "'")
    con.commit()
    return '''<script>alert('account deleted');window.location='/'</script>'''





        # pharmacy module


@app.route('/pharmacy_home')
def pharmacy_home():
    cmd.execute("SELECT COUNT(order_id) FROM `order` JOIN `user_register` ON `user_register`.`login_id`=`order`.`user_id` JOIN `medicine` ON `medicine`.`medicine_id`=`order`.`medicine_id` AND `order`.`status`='pending' AND `medicine`.`pharmacy_id`='"+str(session['lid'])+"'")
    s = cmd.fetchone()
    d=[s[0]]
    if d[0]<1:
        d[0]=""
    return render_template("pharmacy home.html",val=d)

@app.route('/register')
def register():
    return render_template("pharmacy register.html")


@app.route('/pharmacyregisterr', methods=['get', 'post'])
def pharmacyregisterr():
    name=request.form['name']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email=request.form['email']
    phone=request.form['phone']
    photo=request.files['proof']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/proof/"+fn)
    username = request.form['username']
    password = request.form['password']
    cmd.execute("select username from login where username='"+username+"'")
    un=cmd.fetchone();
    if un is None:
        cmd.execute("insert into login values(null,'" + username + "','" + password + "','pending')")
        lid = con.insert_id()
        cmd.execute("insert into pharmacy values(null,'"+str(lid)+"','"+name+"','"+place+"','"+post+"','" + pin + "','" + email + "','" + phone + "','" + fn + "','using')")
        con.commit()
        return '''<script>alert('successfully added');window.location='/'</script>'''
    else:
        return '''<script>alert('Username already existing!!');window.location='/register'</script>'''




@app.route('/location')
def location():
    return render_template("pharmacy add location.html")


@app.route('/addlocation', methods=['get', 'post'])
def addlocation():
    latitude=request.form['latitude']
    longitude=request.form['longitude']
    place=request.form['place']
    cmd.execute("insert into location values(null,'"+str(session['lid'])+"','"+latitude+"','"+longitude+"','"+place+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/pharmacy_home'</script>'''


@app.route('/new_pharmacy_profile')
def new_pharmacy_profile():
    id=session['lid']
    print(id)
    cmd.execute("select*from pharmacy where login_id='"+str(id)+"'")
    s=cmd.fetchone()
    return render_template("pharmacy new profile.html",val=s)


@app.route('/pharmacyregister', methods=['get','post'])
def pharmacyregister():
    name=request.form['name']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    photo=request.files['proof']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/proof/"+fn)
    lid=session['lid']
    cmd.execute("update pharmacy set name='"+name+"',place='"+place+"',post='"+post+"',post='"+pin+"',email='"+email+"',phone='"+phone+"',photo='"+fn+"' where login_id='"+str(lid)+"'")
    con.commit()
    return '''<script>alert('successfully updated');window.location='/lab'</script>'''


@app.route('/medicine')
def medicine():
    return render_template("pharmacy add medicine.html")


@app.route('/addmedicine', methods=['get', 'post'])
def addmedicine():
    medicinename=request.form['name']
    description=request.form['description']
    photo=request.files['photo']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/medimg/"+fn)
    price=request.form['price']
    expdate=request.form['date']
    dosage= request.form['dosage']
    cmd.execute("insert into medicine values(null,'"+str(session['lid'])+"','"+medicinename+"','"+description+"','"+fn+"','"+price+"','"+expdate+"','"+dosage+"')")
    con.commit()
    return'''<script>alert('successfully added');window.location='/pharmacy_home'</script>'''




@app.route('/view_medicine')
def view_medicine():
    cmd.execute("select*from medicine where pharmacy_id='"+str(session['lid'])+"' ")
    s = cmd.fetchall()
    return render_template("pharmacy view medicine.html",val=s)




@app.route('/edit_medicine')
def edit_medicine():
    id=request.args.get('id')
    session['mid']=id
    cmd.execute("select * from medicine where medicine_id='"+str(id)+"'")
    s=cmd.fetchone()
    return render_template("pharmacy edit medicine.html",val=s)


@app.route('/editmed',methods=['get','post'])
def editmed():
    medicinename=request.form['name']
    description=request.form['description']
    photo=request.files['photo']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/medimg/"+fn)
    price=request.form['price']
    expdate= request.form['date']
    dosage= request.form['dosage']
    mid=session['mid']
    cmd.execute("update medicine set medicine_name='"+medicinename+"',description='"+description+"',photo='"+fn+"',price='"+price+"',exp_date='"+expdate+"',dosage='"+dosage+"' where medicine_id='"+str(mid)+"'")
    con.commit()
    return '''<script>alert('successfully updated');window.location='/view_medicine'</script>'''


@app.route('/deletemedi')
def deletemedi():
    id=request.args.get('id')
    cmd.execute("delete from medicine where medicine_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/view_medicine'</script>'''


@app.route('/view_order')
def view_order():
    cmd.execute("SELECT `medicine`.`medicine_name`,`user_register`.`user_id`,`fname`,`lname`,`order`.`date`,`order`.`quantity`, `order`.`order_id`,`user_register`.`login_id` FROM `order` JOIN `user_register` ON `user_register`.`login_id`=`order`.`user_id` JOIN `medicine` ON `medicine`.`medicine_id`=`order`.`medicine_id` AND `order`.`status`='pending' AND `medicine`.`pharmacy_id`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("pharmacy view order.html",val=s)




#do


@app.route('/deleteo')
def deleteo():
    id=request.args.get('uid')
    print(id,"idddd")
    ido = session['lid']
    print(ido)
    cmd.execute("select * from pharmacy where login_id='" + str(ido) + "'")
    s1 = cmd.fetchone()
    print(s1, "ssssssssssss")
    lid = request.args.get('oid')
    logi=request.args.get('loginid')
    cmd.execute("SELECT user_register.* FROM `user_register` JOIN `login` ON `login`.`login_id`=`user_register`.`login_id` WHERE `login`.`login_id`='"+logi+"'")
    print("SELECT user_register.* FROM `user_register` JOIN `login` ON `login`.`login_id`=`user_register`.`login_id` WHERE `login`.`login_id`='"+logi+"'")
    em=cmd.fetchone()
    print("dfghjkl;",em)
    print(em[10],"email")
    print("SELECT * FROM `order` WHERE `order_id`='"+str(lid)+"'")
    cmd.execute("SELECT * FROM `order` WHERE `order_id`='"+str(lid)+"'")
    s=cmd.fetchone()
    mid=s[2]
    qty=s[5]
    cmd.execute("select * from medicine where medicine_id='"+str(mid)+"'")
    p=cmd.fetchone()
    prc=p[5]
    amt=int(qty)*int(prc)
    cmd.execute("select amount from bank where user_id='"+str(logi)+"'")
    a=cmd.fetchone()
    print(a,"=================")
    am=a[0]
    finalamount=int(am)+int(amt)
    cmd.execute("update bank set `amount`='"+str(finalamount)+"' where `user_id`='"+str(logi)+"'")
    cmd.execute("DELETE FROM `order` WHERE `order_id`='"+str(lid)+"'")
    con.commit()
    # print(email)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com','iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your medicine booking denied"+"\n"+"by :"+s1[2])
    print(msg)
    msg['Subject'] = 'medicine booking denied'
    msg['To'] = str(em[10])
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully rejected');window.location='/view_order'</script>'''

#do

@app.route('/approveo')
def approveo():
    id=request.args.get('id')
    ido = session['lid']
    cmd.execute("select name from pharmacy where login_id='" + str(ido) + "'")
    s = cmd.fetchone()
    print(s, "ssssssssssss")
    lid = request.args.get('lid')
    cmd.execute("SELECT user_register.* FROM `user_register` JOIN `login` ON `login`.`login_id`=`user_register`.`login_id` WHERE `login`.`login_id`='"+lid+"'")
    print("SELECT user_register.* FROM `user_register` JOIN `login` ON `login`.`login_id`=`user_register`.`login_id` WHERE `login`.`login_id`='"+lid+"'")
    em=cmd.fetchone()
    print(em)
    print(em[10],"email")
    cmd.execute("UPDATE `order` SET `status`='accepted' WHERE `order_id`='"+id+"'")
    con.commit()
    # print(email)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('virtualmedicoo@gmail.com','iam ironman')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("your medicine booking accepted"+"\n"+"by :"+s[0])
    print(msg)
    msg['Subject'] = 'medicine booking accepted'
    msg['To'] = str(em[10])
    msg['From'] = 'virtualmedicoo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert('successfully approved');window.location='/view_order'</script>'''



@app.route('/pharmacy_feedback')
def pharmacy_feedback():
    return render_template("pharmacy add feedback.html")


@app.route('/feedback', methods=['get', 'post'])
def feedback():
    feedback = request.form['feedback']
    lid = con.insert_id()
    cmd.execute("insert into feedback values(null,'"+str(session['lid'])+"','"+feedback+"',curdate(),'0',null)")
    con.commit()
    return '''<script>alert('successfully added');window.location='/pharmacy_home'</script>'''



@app.route('/vf')
def vf():
    cmd.execute("SELECT `user_register`.`fname`,`lname`,`feedback`.* FROM `feedback` JOIN `user_register` ON `feedback`.`login_id`=`user_register`.`login_id` WHERE `feedback`.`to_id`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("pharmacy view feedback.html",val=s)



@app.route('/deletepharm')
def deletepharm():
    id = session['lid']

    cmd.execute("SELECT DISTINCT `order`.`medicine_id` FROM `medicine` JOIN `pharmacy` ON `pharmacy`.`login_id`=`medicine`.`pharmacy_id` JOIN `order` ON `order`.`medicine_id`=`medicine`.`medicine_id` WHERE `medicine`.`pharmacy_id`='"+str(id)+"'")
    s=cmd.fetchall()
    cmd.execute("delete from pharmacy where login_id='"+str(session['lid'])+"'")
    cmd.execute("delete from login where login_id='"+str(session['lid'])+"'")
    cmd.execute("delete from feedback where to_id='"+str(session['lid'])+"'")
    cmd.execute("delete from location where login_id='"+str(session['lid'])+"'")
    for i in s:
        print(i,"====================")
        cmd.execute("delete from `order` where medicine_id='" + str(i[0]) + "'")
        con.commit()
        cmd.execute("delete from medicine where pharmacy_id='"+str(session['lid'])+"'")
        con.commit()
    return '''<script>alert('account deleted');window.location='/'</script>'''



    # return '''<script>return confirm('are you sure');window.location='/'</script>'''


        #lab module


@app.route('/lab')
def lab():
    return render_template("lab home.html")


@app.route('/lab_register')
def lab_register():
    return render_template("lab register.html")



@app.route('/labregisterr', methods=['get', 'post'])
def labregisterr():
    name=request.form['name']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email=request.form['email']
    phoneno=request.form['phone']
    photo=request.files['proof']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/proof/"+fn)
    username = request.form['username']
    password = request.form['password']
    cmd.execute("select username from login where username='"+username+"'")
    un=cmd.fetchone();
    if un is None:
        cmd.execute("insert into login values(null,'" + username + "','" + password + "','pending')")
        lid = con.insert_id()
        cmd.execute("insert into lab values(null,'"+str(lid)+"','"+name+"','"+place+"','"+post+"','" + pin + "','" + email + "','" + phoneno + "','" + fn + "','using')")
        con.commit()
        return '''<script>alert('successfully added');window.location='/'</script>'''
    else:
        return '''<script>alert('Username already existing!!');window.location='/lab_register'</script>'''


@app.route('/lab_new_profile')
def lab_new_profile():
    id=session['lid']
    print(id)
    cmd.execute("select*from lab where login_id='"+str(id)+"'")
    s=cmd.fetchone()
    return render_template("lab_new_pro.html",val=s)


@app.route('/lab_pro', methods=['get','post'])
def lab_pro():
    name=request.form['name']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']
    photo=request.files['proof']
    from datetime import datetime
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("static/proof/"+fn)
    lid=session['lid']
    cmd.execute("update lab set name='"+name+"',place='"+place+"',post='"+post+"',post='"+pin+"',email='"+email+"',phone='"+phone+"',photo='"+fn+"' where login_id='"+str(lid)+"'")
    con.commit()
    return '''<script>alert('successfully updated');window.location='/lab'</script>'''



@app.route('/lab_location')
def lab_location():
    return render_template("lab add location.html")



@app.route('/lab_add_location', methods=['get','post'])
def lab_add_location():
    latitude=request.form['latitude']
    longitude=request.form['longitude']
    place=request.form['place']
    lid =session['lid']
    cmd.execute("insert into location values(null,'"+str(lid)+"','"+latitude+"','"+longitude+"','"+place+"')")
    con.commit()
    return '''<script>alert('successfully added');window.location='/lab'</script>'''


@app.route('/lab_feedback')
def lab_feedback():
    return render_template("lab add feedback.html")


@app.route('/lfeedback', methods=['get','post'])
def lfeedback():
    feedback = request.form['feedback']
    lid = con.insert_id()
    cmd.execute("insert into feedback values(null,'"+str(session['lid'])+"','"+feedback+"',curdate(),'0',null)")
    con.commit()
    return '''<script>alert('successfully added');window.location='/lab'</script>'''


@app.route('/ltest')
def ltest():
    return render_template("lab test.html")



@app.route('/TEST', methods=['get', 'post'])
def TEST():
    Testname=request.form['name']
    description=request.form['description']
    price=request.form['price']
    lid=session['lid']
    cmd.execute("insert into test values(null,'"+str(lid)+"','"+Testname+"','"+description+"','"+price+"')")
    con.commit()
    return'''<script>alert('successfully added');window.location='/lab'</script>'''



@app.route('/lab_test_edit')
def lab_test_edit():
    cmd.execute("select*from test where lab_id='" + str(session['lid']) + "' ")
    s = cmd.fetchall()
    return render_template("lab edit test.html",val=s)


@app.route('/edit_test')
def edit_test():
    id=request.args.get('id')
    session['tid']=id
    cmd.execute("select * from test where test_id='"+str(id)+"'")
    s=cmd.fetchone()
    return render_template("lab edit testt.html",val=s)


@app.route('/editest',methods=['get','post'])
def editest():
    testname=request.form['name']
    description=request.form['description']
    price=request.form['price']
    id=session['tid']
    cmd.execute("update test set test_name='"+testname+"',description='"+description+"',price='"+price+"' where test_id='"+str(id)+"'")
    con.commit()
    return '''<script>alert('successfully updated');window.location='/lab_test_edit'</script>'''


@app.route('/deletetest')
def deletetest():
    id=request.args.get('id')
    cmd.execute("delete from test where test_id='"+id+"'")
    con.commit()
    return '''<script>alert('successfully deleted');window.location='/lab_test_edit'</script>'''






@app.route('/vfe')
def vfe():
    cmd.execute("SELECT `user_register`.`fname`,`lname`,`feedback`.* FROM `feedback` JOIN `user_register` ON `feedback`.`login_id`=`user_register`.`login_id` WHERE `feedback`.`to_id`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("lab view feedback.html",val=s)



@app.route('/deleteacclab')
def deleteacclab():
    id = session['lid']
    cmd.execute("delete from lab where login_id='"+str(id)+"'")
    cmd.execute("delete from test where lab_id='"+str(id)+"'")
    cmd.execute("delete from login where login_id='" + str(id) + "'")
    cmd.execute("delete from location where login_id='" + str(id) + "'")
    cmd.execute("delete from feedback where to_id='" + str(id) + "'")
    con.commit()
    return '''<script>alert('account deleted');window.location='/'</script>'''



@app.route('/login', methods=['get','post'])
def login():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="virtual doctor")
    cmd = con.cursor()
    username=request.form['username']
    password=request.form['password']
    cmd.execute("select * from login where username='"+username+"' and password='"+password+"'")
    s=cmd.fetchone()
    print(s)
    if s is not None:
        type=s[3]
        print(type)
        if type=="admin":
            return '''<script>alert('login successful');window.location='/home'</script>'''
        elif type=="doctor":
            session['lid']=s[0]

            return '''<script>alert('login successful');window.location='/doctor'</script>'''
        elif type == "hospital":
            session['lid']=s[0]
            return '''<script>alert('login successful');window.location='/hospital_home'</script>'''
        elif type == "pharmacy":
            session['lid']=s[0]

            return '''<script>alert('login successful');window.location='/pharmacy_home'</script>'''
        elif type == "lab":
            session['lid']=s[0]

            return '''<script>alert('login successful');window.location='/lab'</script>'''
        else:
            return '''<script>alert('invalid username');window.location='/'</script>'''
    else:
       return  '''<script>alert('invalid username');window.location='/'</script>'''



if __name__=='__main__':
    app.run(debug=True)

