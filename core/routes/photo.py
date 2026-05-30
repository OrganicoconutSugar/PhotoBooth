from flask import Blueprint, render_template, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from core.database import db
from core.models import Photo
import os
import base64
from datetime import datetime

photo_bp = Blueprint('photo', __name__)

@photo_bp.route('/photobooth')
@login_required
def photobooth():
    if current_user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('photobooth.html', user=current_user)

@photo_bp.route('/save-photo', methods=['POST'])
@login_required
def save_photo():
    data = request.get_json()
    if not data or 'image' not in data:
        return {'success': False, 'message': 'Data foto tidak ditemukan'}, 400

    try:
        smile_score = int(data.get('smile_score', 0))
        image_data = data['image'].split(',')[1]

        filename = f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        with open(file_path, "wb") as fh:
            fh.write(base64.b64decode(image_data))

        new_photo = Photo(user_id=current_user.id, file_path=filename, smile_score=smile_score)  # type: ignore
        db.session.add(new_photo)
        db.session.commit()

        return {'success': True, 'filename': filename, 'message': 'Foto senyummu berhasil disimpan! ✨'}
    except Exception as e:
        return {'success': False, 'message': 'Gagal memproses penyimpanan foto'}, 500

@photo_bp.route('/delete-photo/<filename>', methods=['DELETE'])
@login_required
def delete_photo(filename):
    try:
        safe_filename = os.path.basename(filename)
        photo = Photo.query.filter_by(file_path=safe_filename).first()

        if not photo:
            return jsonify({'success': False, 'message': 'Foto tidak ditemukan di database'}), 404

        if photo.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Anda tidak memiliki izin untuk menghapus foto ini'}), 403

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(photo)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Foto berhasil dihapus permanen'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
