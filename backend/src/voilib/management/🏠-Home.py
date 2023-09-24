# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

import streamlit as st

from voilib import __version__
from voilib.management import utils

st.set_page_config(page_title="Voilib", page_icon="🎧")
st.title("🎧 Voilib Management Dashboard")
authenticated = utils.login_message(st.session_state)

st.markdown(
    f"""**Management tools for Voilib deployments.**

- Voilib verson: `{__version__}`

Select one menu option from the sidebar. You will need an **admin** user
to retrieve the info.

![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
 You will find more info in the [official repository](https://github.com/unmonoqueteclea/voilib)


"""
)
