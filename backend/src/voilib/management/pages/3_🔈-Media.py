# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

import asyncio

import streamlit as st
from voilib import collection, models, routers, settings
from voilib.management import utils as m_utils


async def add_channel():
    st.header("Add new podcast")
    with st.form("my_form"):
        st.markdown(
            """Write below the RSS feed url from a podcast and click `ADD`
            to include it in the database. """
        )
        st.markdown(
            """After adding a new channel, you should

            """
        )
        channel_url = st.text_input("Channel RSS feed url")
        add_click = st.form_submit_button("Add channel", use_container_width=True)
        if add_click:
            with st.spinner("⌛ Adding new channel... Please, wait."):
                _, ch = await collection.get_or_create_channel(channel_url)
                settings.queue.enqueue(
                    collection.update_channel, ch, job_timeout="600m"
                )
            st.success(
                f"""Channel "{ch.title}" correctly added to the
                database.  Its episodes are being updated in a
                background task. This process can take a few minutes."""
            )


async def podcasts_and_episodes():
    st.header("Podcasts and episodes")

    col1, col2, col3 = st.columns(3)
    col1.metric("Channels", await models.Channel.objects.count())
    col2.metric(
        "Transcribed episodes",
        await models.Episode.objects.filter(transcribed=True).count(),
    )
    col3.metric(
        "Indexed episodes",
        await models.Episode.objects.filter(embeddings=True).count(),
    )
    with st.spinner("⌛ Loading channels..."):
        for ch in (await routers.analytics._media()).channels:
            with st.expander(
                f"**{ch.title}**. Indexed {ch.available_episodes}/{ch.total_episodes}"
            ):
                st.image(ch.image)
                st.markdown(ch.description)


async def main():
    st.set_page_config(page_title="Voilib", page_icon="🎧")
    st.title("📻 Media")
    authenticated = m_utils.login_message(st.session_state)
    if authenticated:
        await add_channel()
        st.divider()
        await podcasts_and_episodes()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
