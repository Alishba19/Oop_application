import streamlit as st
from datetime import datetime
import pickle
import os



# ------------------ Classes ------------------ #

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.skills_offered = []
        self.skills_wanted = []
        self.sessions = []
        self.balance = 100  # Starting SkillCoins

    def add_skill_offered(self, skill):
        self.skills_offered.append(skill)

    def add_skill_wanted(self, skill):
        self.skills_wanted.append(skill)

    def book_session(self):
        if self.balance >= 20:
            self.balance -= 20
            self.sessions.append(datetime.now())
            return True
        else:
            return False

    def buy_coins(self, amount):
        self.balance += amount




# ------------------ Helper Functions ------------------ #

USER_DATA_FILE = "users.pkl"

def save_users():
    with open(USER_DATA_FILE, "wb") as f:
        pickle.dump(st.session_state.users, f)

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "rb") as f:
            st.session_state.users = pickle.load(f)
    else:
        st.session_state.users = {}



# ------------------ App Functions ------------------ #

def register():
    st.title("🔐 SkillSwap - Register")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")

    if st.button("Register"):
        if username in st.session_state.users:
            st.error("🚫 Username already exists.")
        else:
            st.session_state.users[username] = User(username, password)
            save_users()
            st.success("✅ Registered successfully! Please login now.")

def login():
    st.title("🔐 SkillSwap - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users:
            user = st.session_state.users[username]
            if user.password == password:
                st.session_state.user = user
                st.success(f"✅ Welcome, {username}!")
            else:
                st.error("🚫 Invalid password.")
        else:
            st.error("🚫 Username not found. Please register.")

def dashboard():
    st.title("📘 SkillSwap Dashboard")
    user = st.session_state.user
    st.write(f"👋 Welcome, **{user.username}**")

    st.subheader("💰 Your SkillCoin Balance:")
    st.write(f"🪙 {user.balance} SkillCoins")

    if st.button("🎓 Book a Skill Session (20 Coins)"):
        if user.book_session():
            save_users()
            st.success("✅ Session booked successfully! 20 Coins deducted.")
        else:
            st.error("🚫 Not enough SkillCoins!")

    if st.button("💳 Buy 100 SkillCoins (Simulated)"):
        user.buy_coins(100)
        save_users()
        st.success("✅ 100 SkillCoins added.")

    skill_offer = st.text_input("💡 Skill you can teach:")
    skill_want = st.text_input("🎯 Skill you want to learn:")

    if st.button("Add Skills"):
        if skill_offer:
            user.add_skill_offered(skill_offer)
        if skill_want:
            user.add_skill_wanted(skill_want)
        save_users()
        st.success("✅ Skills updated!")

    st.subheader("📚 Skills You Offer:")
    st.write(user.skills_offered or "No skills added yet.")

    st.subheader("🧠 Skills You Want:")
    st.write(user.skills_wanted or "No skills added yet.")

def business_plan():
    st.title("📈 SkillSwap Business Plan")
    st.image("https://plus.unsplash.com/premium_photo-1664298390030-d78b64465662?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", width=120)
    st.markdown("""
    **💡 Name:** SkillSwap  
    **🌐 Domain:** [skillswaphub.com](http://skillswaphub.com) *(suggested, not yet registered)* 
    **🖼️ Logo:** [Logo] (https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80)     
    **🎯 Startup Vision:** A global peer-to-peer learning platform where users exchange skills using virtual currency (SkillCoins).

    **💰 Revenue Plan:**
    - Users start with 100 free SkillCoins.
    - Can buy more SkillCoins (simulated here, real payments in future).
    - Example: 100 Coins = $5.

    **📢 Marketing:**
    - Partner with universities and student communities.
    - Use social media reels, referrals, and testimonials.

    **📥 User Acquisition:**
    - Referral bonuses.
    - Skill challenges and leaderboards.
    """)



# ------------------ Main App ------------------ #

def main():
    st.set_page_config(page_title="SkillSwap", layout="centered")
    st.sidebar.image("https://plus.unsplash.com/premium_photo-1668902224071-e5fb23354d25?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZnJlZSUyMFNraWxsU3dhcCUyMFNTfGVufDB8fDB8fHww", width=100)
    st.sidebar.title("SkillSwap Menu")
    menu = st.sidebar.radio("Navigate", ["Home", "Register", "Login", "Dashboard", "Business Plan"])

    load_users()

    if "user" not in st.session_state:
        st.session_state.user = None

    if menu == "Home":
        st.title("🤝 Welcome to SkillSwap")
        st.markdown("### Exchange your skills with others. Learn and grow together!")
        st.image("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80", use_container_width=True)

    elif menu == "Register":
        register()

    elif menu == "Login":
        login()

    elif menu == "Dashboard":
        if st.session_state.user:
            dashboard()
        else:
            st.warning("⚠️ Please login to access the dashboard.")

    elif menu == "Business Plan":
        business_plan()

if __name__ == "__main__":
    main()
