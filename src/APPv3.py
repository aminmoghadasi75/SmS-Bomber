import streamlit as st
from SmSBoomberv3 import SMSBomber
import pickle
import os



# Define the user data file and comments file
USER_DATA_FILE = 'user_data.pkl'
COMMENTS_FILE = 'comments.pkl'

# Load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return []

# Save user data
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

# Load comments
def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return []

# Save comments
def save_comments(comments):
    with open(COMMENTS_FILE, 'wb') as f:
        pickle.dump(comments, f)

# Initialize session state variables
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# Load existing user data and comments
user_data = load_user_data()
comments = load_comments()

# Ensure user_data is a list of dictionaries
if not all(isinstance(user, dict) for user in user_data):
    user_data = []

# Ask for username
if not st.session_state.is_logged_in:
    
    st.header('Login')
    username = st.text_input('Enter your Instagram ID:')
    login_button = st.button('Login')
    if login_button :
        st.write('Double click on the Login button to continue.')

    if login_button:
        st.session_state.username = username
        if username == 'thekingfoo':
            password = st.text_input('Enter password:', type='password')
            if password == '123':
                st.session_state.is_logged_in = True
                st.success('Logged in as admin.')
            else:
                st.error('Incorrect password.')
        else:
            st.session_state.is_logged_in = True
            st.success(f'Logged in as {username}.')

        # Save the username to the user data if not admin
        if username != 'thekingfoo':
            if not any(user.get('username') == username for user in user_data):
                user_data.append({'username': username, 'phone_numbers': [], 'comments': []})
                save_user_data(user_data)
else:
    # Show the product
    st.title('SMS Bomber :boom:')
    st.header('What is SMS Bomber?')
    st.write('''
    SMS Bomber is a tool designed to send multiple SMS messages to a given phone number repeatedly. 
    This can be used for testing purposes or to verify phone number handling on various websites.

    **Disclaimer**: Use this tool responsibly. Sending unsolicited messages to individuals without their consent is illegal and unethical. Ensure you have permission to send messages to the phone number you enter.
    ''')

    st.warning('Use this tool responsibly.')

    phone_number = st.text_input('Enter Phone Number:')
    repeat = int(st.select_slider('How many times do you want to send?', [4, 8, 12, 16, 20, 24, 28, 32, 36, 40])) // 4

    if st.button('Start bombing'):
        if not phone_number:
            st.error('Please enter a valid phone number.')
        elif phone_number == '09017295436':
            st.error('کثافت شماره خودمو نده اسکل :)')
        else:
            # Update user data with the phone number used
            for user in user_data:
                if user.get('username') == st.session_state.username:
                    user['phone_numbers'].append(phone_number)
                    save_user_data(user_data)
                    break

            sms_bomber = SMSBomber(phone_number=phone_number, repeat=repeat)
            with st.spinner('Sending SMS...'):
                try:
                    sms_bomber.run()
                    st.success('SMS bombing completed successfully.')
                except Exception as e:
                    st.error(f'An error occurred: {e}')
    else:
        st.write('Enter a phone number to start.')

    # Comment section
    st.header('Leave a Comment')
    comment = st.text_area('Your Comment:')
    if st.button('Submit Comment'):
        if comment:
            comments.append({'user': st.session_state.username, 'comment': comment})
            save_comments(comments)
            st.success('Comment submitted.')

            # Update user data with the comment
            for user in user_data:
                if user.get('username') == st.session_state.username:
                    user['comments'].append(comment)
                    save_user_data(user_data)
                    break
        else:
            st.error('Please enter a comment.')

    # Admin section to show the list of users and their comments
    if st.session_state.username == 'thekingfoo':
        st.header('Admin Panel')
        st.write('List of users who have used the product:')
        for user in user_data:
            st.write(f"**Username:** {user.get('username')}")
            st.write(f"**Phone Numbers Used:** {', '.join(user.get('phone_numbers', []))}")
            st.write(f"**Comments:** {', '.join(user.get('comments', []))}")
            st.write('---')

    # Logout button
    if st.button('Logout'):
        st.session_state.is_logged_in = False
        st.session_state.username = ''
        st.experimental_rerun()
