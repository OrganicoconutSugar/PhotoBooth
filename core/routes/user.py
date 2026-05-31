from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from core.database import db
from core.models import Photo
import os
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    recent_photos = (
        Photo.query
        .filter_by(user_id=current_user.id)
        .order_by(Photo.id.desc())
        .limit(6)
        .all()
    )
    return render_template('dashboard.html', user=current_user, recent_photos=recent_photos)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        new_phone = request.form.get('phone', '').strip()
        new_bio = request.form.get('bio', '').strip()

        changed = False

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '':
                try:
                    ext = os.path.splitext(file.filename)[1].lower()
                    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                        ext = '.png'

                    filename = f"profile_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename) # Note: need current_app
                    file.save(file_path)

                    current_user.profile_pic = filename
                    changed = True
                except Exception as e:
                    flash(f'Gagal mengunggah foto profil: {str(e)}', 'error')

        if new_username:
            current_user.username = new_username
            current_user.phone = new_phone
            current_user.bio = new_bio
            changed = True
        else:
            flash('Username tidak boleh kosong.', 'error')

        if changed:
            try:
                db.session.commit()
                db.session.refresh(current_user)
                flash('Profil kamu berhasil diperbarui!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Gagal menyimpan perubahan: {str(e)}', 'error')

        return redirect(url_for('user.profile'))

    return render_template('profile.html', user=current_user)

@user_bp.route('/gallery')
@login_required
def gallery():
    if current_user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))

    user_photos = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.id.desc()).all()
    return render_template('gallery.html', photos=user_photos)
