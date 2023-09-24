# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

import asyncio
import datetime

import streamlit as st
from voilib import collection, settings, tasks, utils
from voilib.management import utils as m_utils


async def load_default_channels():
    st.header("1. Load default channel list (only once)")
    st.markdown(
        """Voilib comes with a predefined list of podcasts `RSS`
        feeds.  If you import them, the system will transcribe and
        index them. This is, usually, the first task that is performed
        in a new installation. Alternatively, you can also provide
        your own urls for `RSS` feeds. **You should run this task only
        once** """
    )
    st.info("This action may take up to 4 minutes.")
    with st.expander("Show the list of channels"):
        lines = [f"- {item['name']}" for item in collection.default_channels()]
        st.markdown("\n".join(lines))
    import_default = st.button("⚙️ Import default channels", use_container_width=True)
    if import_default:
        with st.spinner("⌛ Loading default channels... Please, wait."):
            await collection.add_default_channels()
        st.success("Default list of channels correctly added")


async def update_channels():
    st.header("2. Update channel episodes")
    st.markdown(
        """After loading channels to the system, you will need to
        **update the list of eposides of each one**. This task crawls the
        list of imported feeds to find new episodes (that will be
        transcribed and indexed when requested.  """
    )
    if last_execution := utils.get_event("event_update_start"):
        last_execution_time = float(last_execution["time"])
        date = datetime.datetime.fromtimestamp(last_execution_time).strftime("%c")
        st.markdown(f"**Last execution**: `{date}`")
    update_channels = st.button("⚙️ Update channels", use_container_width=True)
    if update_channels:
        settings.queue.enqueue(tasks.update_channels)
        st.success("Channels started to update in the background")


async def transcribe_pending():
    st.header("3. Transcribe episodes")
    st.markdown(
        """Trigger the **transcription process** that will take
        episodes from the last `number of days` and transcribe them in
        random order. When transcriptions finish, the episodes won't
        be ready yet for queries, you should **index** them first (see
        next tasks). """
    )
    if last_execution := utils.get_event("event_transcription_start"):
        last_execution_time = float(last_execution["time"])
        date = datetime.datetime.fromtimestamp(last_execution_time).strftime("%c")
        st.markdown(f"**Last execution**: `{date}`: {last_execution['info']}")

    days = st.number_input("Number of days", min_value=1, step=1)
    start = st.button("🎧 Start transcription process", use_container_width=True)
    if start:
        total = await tasks.transcribe_episodes(days)  # type: ignore
        st.success(f"Started transcription of {total} episodes in a background process")


async def store_pending():
    st.header("4. Index episodes")
    st.markdown(
        """Trigger the process that will index all finished
        transcriptions so that users can query them """
    )
    if last_execution := utils.get_event("event_store_start"):
        last_execution_time = float(last_execution["time"])
        date = datetime.datetime.fromtimestamp(last_execution_time).strftime("%c")
        st.markdown(f"**Last execution**: `{date}`: {last_execution['info']}")

    start = st.button("💾 Start indexing process", use_container_width=True)
    if start:
        settings.queue.enqueue(tasks.store_episodes_embeddings)
        st.success("Started indexing in a background process")


async def main():
    st.set_page_config(page_title="Voilib", page_icon="🎧")
    st.title("⚙️ Tasks")
    authenticated = m_utils.login_message(st.session_state)
    if authenticated:
        await load_default_channels()
        st.divider()
        await update_channels()
        st.divider()
        await transcribe_pending()
        st.divider()
        await store_pending()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
