from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'blend'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_blend_file():
    if request.method == 'POST':
        blend_file = request.files['blend_file']
        if blend_file and allowed_file(blend_file.filename):
            filename = secure_filename(blend_file.filename)
            blend_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            blend_file.save(blend_path)

            # Render the Blender file
            output_path = os.path.join('renders', f'{os.path.splitext(filename)[0]}.png')
            render_blend_file(blend_path, output_path)

            return redirect(url_for('index'))

    return redirect(url_for('index'))

def render_blend_file(blend_path, output_path):
    blender_command = f"blender -b {blend_path} -o {output_path} -f 1"

    try:
        subprocess.check_output(blender_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while rendering: {e.output}")

if __name__ == '__main__':
    app.run(debug=True)