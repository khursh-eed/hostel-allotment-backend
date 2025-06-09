from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main  # we import our blueprint here
from app.auth.forms import ReceiptUploadForm
from app.auth.forms import StudentProfileForm
from app.auth.forms import Roomid
from werkzeug.utils import secure_filename
import os
from app import db
from flask import current_app
from app.models import Student, Allotment 
from flask import request



@main.route('/')
def index():
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required  # This makes sure only logged-in users can see this page
def dashboard():
    # current_user is the logged-in user object
    return render_template('main/dashboard.html', user=current_user)

@main.route('/uploadreceipt',methods=['GET', 'POST'])
@login_required
def uploadreceipt():
    form = ReceiptUploadForm()

    if form.validate_on_submit():  #(after the form has been uploaded by uder)
        file = form.receipt.data   #storing the uploaded file
        filename = secure_filename(file.filename)   #getting the name of the file and sanitize it (Remove dangerouse char lik "/")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        # we use current_app instead of app.config (to get the folder path) - is a flask proxy
        file.save(filepath)
        
        # Update user with receipt
        current_user.receipt_filename = filename
        current_user.receipt_status = "Pending"
        db.session.commit()
        
        flash("Receipt uploaded successfully! Awaiting verification.", "success")
        return redirect(url_for('main.dashboard'))


    return render_template('main/uploadreceipt.html',form=form, user=current_user)

@main.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    
    form = StudentProfileForm()
    # adding the profile only once
    if current_user.student:  
        flash("Profile already submitted.", "info")
        return redirect(url_for('main.dashboard'))

    if form.validate_on_submit():
        new_profile = Student(
            student_id=current_user.id,  #from the user table
            name=current_user.name,      #from the user table
            branch=form.branch.data,
            gender=form.gender.data,
            category=form.category.data,
            academic_year=form.academic_year.data,
            program=form.program.data
        )
        db.session.add(new_profile)
        db.session.commit()
        flash("Profile submitted successfully!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('main/update_profile.html', form=form)

@main.route('/choose-room', methods=['GET', 'POST'])
@login_required
def choose_room():
    student = Student.query.filter_by(student_id=current_user.id).first()

    if not student:
        flash("Please complete your profile first.", "warning")
        return redirect(url_for('main.update_profile'))

    if current_user.receipt_status != "Verified" and student.category != "EWS":
        flash("You are not eligible for room allotment. Fee not verified.", "danger")
        return redirect(url_for('main.dashboard'))

    category = "NON-DASA" if student.category != "DASA" else "DASA"

    rooms = db.session.execute("""
        SELECT r.room_id, r.floor, r.room_number, r.capacity, COUNT(a.student_id) AS occupancy, h.name AS hostel_name
        FROM Room r
        JOIN Hostel h ON r.hostel_id = h.hostel_id
        LEFT JOIN Allotment a ON r.room_id = a.room_id
        WHERE h.category = :category AND h.gender = :gender AND h.program = :program AND h.year = :year
        GROUP BY r.room_id
        HAVING r.capacity > occupancy
    """, {
        'category': category,
        'gender': student.gender,
        'program': student.program,
        'year': student.academic_year
    }).fetchall()

    form = Roomid()
    # adding chocies to the drop down before seletecting
    form.roomid.choices = [(r.room_id, f"{r.hostel_name} - {r.room_number} (Floor {r.floor})") for r in rooms]

    if form.validate_on_submit():
        room_id = form.roomid.data

        if not room_id:
            flash("Please select a room.", "warning")
        else:
            existing = Allotment.query.filter_by(student_id=current_user.id).first()
            if existing:
                flash("You have already been allotted a room.", "info")
            else:
                new_allotment = Allotment(student_id=current_user.id, room_id=room_id)
                db.session.add(new_allotment)
                db.session.commit()
                flash("Room successfully allotted", "success")
                return redirect(url_for('main.dashboard'))

    return render_template('choose_room.html',form=form)

