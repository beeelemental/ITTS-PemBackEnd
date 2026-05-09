from flask import Flask, render_template

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Route utama "/"
@app.route('/')
def index():
    return render_template('index.html',
                           title='Hello World',
                           message='Hello, World!')

# Route tambahan "/about"
@app.route('/about')
def about():
    return render_template('index.html',
                           title='About',
                           message='Ini adalah aplikasi Flask sederhana.')

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)