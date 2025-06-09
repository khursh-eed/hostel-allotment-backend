from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import admin
from app import db
from sqlalchemy import text

@admin.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if not current_user.is_admin:
        abort(403)

    unverified_students = db.session.execute(text("""
    SELECT u.id, u.email, s.name, s.branch, s.category
    FROM User u
    JOIN Student s ON u.id = s.student_id
    WHERE u.receipt_status = 'Pending'
    """)).fetchall()

    
    return render_template('admin/dashboard.html', students= unverified_students)

@admin.route('/verify/<int:user_id>', methods=['POST'])
@login_required
def verify_student(user_id):
    if not current_user.is_admin:
        abort(403)

    user = current_user.query.get(user_id)
    if user:
        user.receipt_status = "Verified"
        db.session.commit()
        flash(f"{user.email} has been verified.", "success")
    else:
        flash("User not found.", "danger")

    return redirect(url_for('admin.dashboard'))

@admin.route('/students')
@login_required
def view_students():
    if not current_user.is_admin:
        abort(403)

    students = db.session.execute(text("""
        SELECT u.email, s.name, s.branch, s.gender, s.category, s.academic_year, s.program
        FROM User u
        JOIN Student s ON u.id = s.student_id
    """)).fetchall()

    return render_template('admin/view_students.html', students=students)

@admin.route('/allotments')
@login_required
def view_allotments():
    if not current_user.is_admin:
        abort(403)

    allotments = db.session.execute(text("""
        SELECT u.email, s.name, r.room_number, r.floor, h.name AS hostel_name
        FROM Allotment a
        JOIN Student s ON a.student_id = s.student_id
        JOIN User u ON u.id = s.student_id
        JOIN Room r ON a.room_id = r.room_id
        JOIN Hostel h ON r.hostel_id = h.hostel_id
    """)).fetchall()

    return render_template('admin/view_allotments.html', allotments=allotments)
