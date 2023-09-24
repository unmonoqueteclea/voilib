# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

import streamlit as st

USERNAME_KEY = "logged_user_username"
TOKEN_KEY = "logged_user_token"


def login_message(session_state) -> bool:
    username = session_state.get(USERNAME_KEY)
    token = session_state.get(TOKEN_KEY)
    if not username or not token:
        st.error("👤 Unauthenticated user, please login first.")
        return False
    st.info(f"👋 Hello, {username}")
    return True
