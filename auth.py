import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import uuid
from typing import Dict, Optional, Tuple

class AuthenticationManager:
    """Enhanced authentication system with proper security"""
    
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self.users_data = self.load_users()
        
    def load_users(self) -> Dict:
        """Load users from JSON file or create default"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Create default users for demo
        default_users = {
            "demo": {
                "password_hash": self.hash_password("password123"),
                "email": "demo@example.com",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "is_active": True,
                "role": "user",
                "usage_stats": {
                    "content_generated": 0,
                    "last_generation": None
                }
            },
            "admin": {
                "password_hash": self.hash_password("admin123"),
                "email": "admin@example.com",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "is_active": True,
                "role": "admin",
                "usage_stats": {
                    "content_generated": 0,
                    "last_generation": None
                }
            }
        }
        
        self.save_users(default_users)
        return default_users
    
    def save_users(self, users_data: Dict = None) -> bool:
        """Save users data to JSON file"""
        try:
            data_to_save = users_data or self.users_data
            with open(self.users_file, 'w') as f:
                json.dump(data_to_save, f, indent=2, default=str)
            return True
        except Exception as e:
            st.error(f"Error saving user data: {str(e)}")
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == password_hash
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """Authenticate user credentials"""
        if username not in self.users_data:
            return False, None
        
        user_data = self.users_data[username]
        
        if not user_data.get("is_active", True):
            return False, {"error": "Account is deactivated"}
        
        if self.verify_password(password, user_data["password_hash"]):
            # Update last login
            self.users_data[username]["last_login"] = datetime.now().isoformat()
            self.save_users()
            return True, user_data
        
        return False, {"error": "Invalid password"}
    
    def register_user(self, username: str, password: str, email: str) -> Tuple[bool, str]:
        """Register new user"""
        # Validation
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if not email or "@" not in email:
            return False, "Please enter a valid email address"
        
        if username in self.users_data:
            return False, "Username already exists"
        
        # Check if email already exists
        for user_data in self.users_data.values():
            if user_data.get("email") == email:
                return False, "Email already registered"
        
        # Create new user
        self.users_data[username] = {
            "password_hash": self.hash_password(password),
            "email": email,
            "created_date": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True,
            "role": "user",
            "usage_stats": {
                "content_generated": 0,
                "last_generation": None
            }
        }
        
        if self.save_users():
            return True, "Registration successful!"
        else:
            return False, "Error saving user data"
    
    def update_user_stats(self, username: str, content_generated: bool = False):
        """Update user usage statistics"""
        if username in self.users_data:
            if content_generated:
                self.users_data[username]["usage_stats"]["content_generated"] += 1
                self.users_data[username]["usage_stats"]["last_generation"] = datetime.now().isoformat()
            self.save_users()
    
    def get_user_profile(self, username: str) -> Optional[Dict]:
        """Get user profile data"""
        if username in self.users_data:
            user_data = self.users_data[username].copy()
            # Remove sensitive data
            user_data.pop("password_hash", None)
            return user_data
        return None
    
    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        if username not in self.users_data:
            return False, "User not found"
        
        user_data = self.users_data[username]
        
        if not self.verify_password(old_password, user_data["password_hash"]):
            return False, "Current password is incorrect"
        
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long"
        
        self.users_data[username]["password_hash"] = self.hash_password(new_password)
        
        if self.save_users():
            return True, "Password changed successfully!"
        else:
            return False, "Error saving new password"

# Session management functions
def initialize_auth_session():
    """Initialize authentication-related session state"""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthenticationManager()
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'username' not in st.session_state:
        st.session_state.username = ""
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    
    if 'last_failed_login' not in st.session_state:
        st.session_state.last_failed_login = None

def render_enhanced_login():
    """Render enhanced login interface"""
    st.markdown("## 🔐 Secure Login")
    
    # Check for rate limiting
    if st.session_state.login_attempts >= 5:
        if st.session_state.last_failed_login:
            time_diff = datetime.now() - datetime.fromisoformat(st.session_state.last_failed_login)
            if time_diff < timedelta(minutes=15):
                st.error("Too many failed login attempts. Please try again in 15 minutes.")
                return
            else:
                # Reset attempts after cooldown
                st.session_state.login_attempts = 0
                st.session_state.last_failed_login = None
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["🚀 Login", "📝 Register"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_registration_form()

def render_login_form():
    """Render login form"""
    with st.form("login_form"):
        st.markdown("### Enter Your Credentials")
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        remember_me = st.checkbox("Remember me", key="remember_login")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            login_submitted = st.form_submit_button("🚀 Login", use_container_width=True)
        
        with col2:
            forgot_password = st.form_submit_button("🔑 Forgot?", use_container_width=True)
        
        if login_submitted:
            if username and password:
                auth_manager = st.session_state.auth_manager
                success, result = auth_manager.authenticate_user(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_data = result
                    st.session_state.login_attempts = 0
                    st.session_state.last_failed_login = None
                    
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    st.session_state.last_failed_login = datetime.now().isoformat()
                    
                    error_msg = result.get("error", "Invalid credentials") if result else "Invalid credentials"
                    st.error(f"❌ {error_msg}")
                    
                    if st.session_state.login_attempts >= 3:
                        st.warning(f"⚠️ {5 - st.session_state.login_attempts} attempts remaining before temporary lockout.")
            else:
                st.warning("⚠️ Please enter both username and password.")
        
        if forgot_password:
            st.info("🔑 Password recovery feature will be implemented in future updates.")

def render_registration_form():
    """Render registration form"""
    with st.form("registration_form"):
        st.markdown("### Create New Account")
        
        reg_username = st.text_input(
            "Username",
            placeholder="Choose a username (min 3 characters)",
            key="reg_username"
        )
        
        reg_email = st.text_input(
            "Email",
            placeholder="Enter your email address",
            key="reg_email"
        )
        
        reg_password = st.text_input(
            "Password",
            type="password",
            placeholder="Choose a password (min 6 characters)",
            key="reg_password"
        )
        
        reg_password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
            key="reg_password_confirm"
        )
        
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        register_submitted = st.form_submit_button("📝 Create Account", use_container_width=True)
        
        if register_submitted:
            if not all([reg_username, reg_email, reg_password, reg_password_confirm]):
                st.warning("⚠️ Please fill in all fields.")
            elif reg_password != reg_password_confirm:
                st.error("❌ Passwords do not match.")
            elif not agree_terms:
                st.warning("⚠️ Please agree to the Terms of Service.")
            else:
                auth_manager = st.session_state.auth_manager
                success, message = auth_manager.register_user(reg_username, reg_password, reg_email)
                
                if success:
                    st.success(f"✅ {message} You can now login with your credentials.")
                else:
                    st.error(f"❌ {message}")

def render_user_profile():
    """Render user profile page"""
    st.markdown("## 👤 User Profile")
    
    if not st.session_state.authenticated:
        st.error("Please login to view your profile.")
        return
    
    auth_manager = st.session_state.auth_manager
    profile_data = auth_manager.get_user_profile(st.session_state.username)
    
    if not profile_data:
        st.error("Profile data not found.")
        return
    
    # Profile information
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📊 Account Statistics")
        st.metric("Content Generated", profile_data["usage_stats"]["content_generated"])
        st.metric("Account Role", profile_data["role"].title())
        
        if profile_data["last_login"]:
            last_login = datetime.fromisoformat(profile_data["last_login"])
            st.metric("Last Login", last_login.strftime("%Y-%m-%d %H:%M"))
    
    with col2:
        st.markdown("### ⚙️ Account Settings")
        
        # Change password form
        with st.expander("🔑 Change Password"):
            with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password"):
                    if not all([current_password, new_password, confirm_password]):
                        st.warning("Please fill in all fields.")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match.")
                    else:
                        success, message = auth_manager.change_password(
                            st.session_state.username, current_password, new_password
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
        
        # Account information
        with st.expander("📝 Account Information"):
            st.text_input("Username", value=st.session_state.username, disabled=True)
            st.text_input("Email", value=profile_data["email"])
            st.text_input("Member Since", value=profile_data["created_date"][:10], disabled=True)
            
            if st.button("💾 Update Profile"):
                st.info("Profile update functionality will be implemented in future updates.")

def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.user_data = {}
    st.session_state.current_page = "home"
    st.success("Successfully logged out!")
    st.rerun()
