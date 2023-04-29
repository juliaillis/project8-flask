from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient, DESCENDING
import bcrypt

#to use bcrypt you need to install it using pip install bcrypt.

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Establish connection with MongoDB
client = MongoClient()
db = client['user_management']
users_collection = db['users']

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        # Get old password and new passwords from form
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        retyped_password = request.form['retyped_password']
        
        # Get username from session
        username = session['username']
        
        # Find user in MongoDB by username
        user = users_collection.find_one({'username': username})
        
        # Check if old password is correct
        if bcrypt.checkpw(old_password.encode('utf-8'), user['password']):
            # Check if new passwords match
            if new_password == retyped_password:
                # Hash new password
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                
                # Update user's password in MongoDB
                users_collection.update_one({'username': username}, {'$set': {'password': hashed_password}})
                
                # Redirect to success page
                return redirect('/password_changed')
            else:
                # Display error message if new passwords don't match
                error = "New passwords don't match"
                return render_template('change_password.html', error=error)
        else:
            # Display error message if old password is incorrect
            error = "Old password is incorrect"
            return render_template('change_password.html', error=error)
    else:
        # Render the change password form
        return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True)
