from flask import Flask, render_template
import sqlite3

app = Flask(__name__, static_folder='user_images/')

# Function to fetch all users from the database
def fetch_all_users():
    conn = sqlite3.connect('security_guard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, phone, image_path FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Route to display all users
@app.route('/users')
def show_users():
    users = fetch_all_users()
    return render_template('users.html', users=users)

@app.route('/user_images/<path>')
def get_user_image(path):
    return app.send_static_file(path)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
