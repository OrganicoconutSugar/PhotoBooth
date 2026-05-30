from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from core.database import db
from core.models import User, Photo
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Akses ditolak! Anda bukan Admin.', 'error')
        return redirect(url_for('user.dashboard'))

    all_users = User.query.all()

    # Hitung hanya foto yang file fisiknya MASIH ADA (bukan orphan/sampah)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    all_photos = Photo.query.all()
    valid_photos_count = sum(
        1 for p in all_photos
        if os.path.exists(os.path.join(upload_folder, p.file_path))
    )

    return render_template('admin.html', user=current_user, users=all_users, total_photos=valid_photos_count)

@admin_bp.route('/admin/user/<int:user_id>/details')
@login_required
def user_details(user_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Akses ditolak!'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User tidak ditemukan.'}), 404

    # Ambil list foto dan skor senyuman miliknya
    # HANYA foto yang file fisiknya MASIH ADA — foto yang dihapus user tidak ditampilkan
    upload_folder = current_app.config['UPLOAD_FOLDER']
    photos_list = []
    orphan_records = []  # Record yang file-nya sudah tidak ada

    for p in user.photos:
        file_full_path = os.path.join(upload_folder, p.file_path)
        if os.path.exists(file_full_path):
            photos_list.append({
                'id': p.id,
                'file_path': p.file_path,
                'smile_score': p.smile_score,
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M') if p.created_at else '-'
            })
        else:
            # File fisik tidak ada tapi record masih di DB — otomatis bersihkan (orphan cleanup)
            orphan_records.append(p)

    # Hapus record orphan secara otomatis dari DB
    if orphan_records:
        for orphan in orphan_records:
            db.session.delete(orphan)
        db.session.commit()

    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'phone': user.phone or 'Belum mencantumkan nomor HP',
            'bio': user.bio or 'Belum menuliskan deskripsi bio.',
            'profile_pic': user.profile_pic
        },
        'photos': photos_list,
        'cleaned_orphans': len(orphan_records)  # Info berapa record sampah dibersihkan
    })

@admin_bp.route('/admin/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Akses ditolak!'}), 403

    if current_user.id == user_id:
        return jsonify({'success': False, 'message': 'Anda tidak dapat menghapus akun Anda sendiri!'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User tidak ditemukan.'}), 404

    try:
        # Hapus file foto fisik milik user ini
        for photo in user.photos:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.delete(photo)

        # Hapus file foto profil jika ada
        if user.profile_pic:
            profile_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user.profile_pic)
            if os.path.exists(profile_path):
                os.remove(profile_path)

        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': f'Akun {user.username} berhasil dihapus secara permanen!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Gagal menghapus user: {str(e)}'}), 500


@admin_bp.route('/admin/cleanup-orphans', methods=['POST'])
@login_required
def cleanup_orphan_photos():
    """Endpoint untuk membersihkan semua record foto orphan (file fisik sudah tidak ada) dari DB."""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Akses ditolak!'}), 403

    upload_folder = current_app.config['UPLOAD_FOLDER']
    all_photos = Photo.query.all()
    cleaned = 0

    try:
        for photo in all_photos:
            file_full_path = os.path.join(upload_folder, photo.file_path)
            if not os.path.exists(file_full_path):
                db.session.delete(photo)
                cleaned += 1

        db.session.commit()
        return jsonify({'success': True, 'message': f'{cleaned} record foto sampah berhasil dibersihkan dari database.', 'cleaned': cleaned})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Gagal cleanup: {str(e)}'}), 500
