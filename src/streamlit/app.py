import streamlit as st
from crew import PropertyHunterCrew, PropertyDetails
from utils import stream_data

ICONS = {"assistant": "./house.png", "human": None}

def init_chat_history():
    """
    Create a st.session_state.messages list to store chat messages if none exist.
    """

    if "messages" not in st.session_state:
        clear_chat_history()


def clear_chat_history():
    """
    Reset session_state.messages to greeting message.
    """
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey. I'm Proppy, an agent designed to find rental properties in your area that fit all your needs. Try asking me about properties in your area.",
        }
    ]


def display_chat_messages():
    """
    Display all messages in st.session_state.messages,
    for example after a reset.
    """

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=ICONS[message["role"]]):
            st.write(message["content"])


def display_chat_message(role: str, message: str):
    """
    Displays a chat message with the specified role and message content.

    Parameters:
        role (str): The role of the chat message. Can be either "assistant" or "human".
        message (str): The content of the chat message.

    Returns:
        None
    """

    message_stream = stream_data(message)

    with st.chat_message(role, avatar=ICONS[role]):
        st.write_stream(message_stream)


def display_sidebar_ui():
    """
    Displays the sidebar user interface for the app.
    """

    st.sidebar.title("Property Hunter")
    st.sidebar.subheader("Model inputs")

    st.sidebar.text_input("Location", key="location", placeholder="Washington D.C.")
    st.sidebar.number_input(
        "No. of rooms", min_value=1, key="no_rooms", placeholder="1"
    )
    st.sidebar.slider(
        "Budget",
        min_value=0,
        max_value=10000,
        value=(0, 10000),
        step=100,
        key="budget",
    )

    if st.sidebar.button("Kickoff Crew"):
        kickoff_crew()

    st.sidebar.button("Reset", on_click=clear_chat_history(), type="primary")

    st.sidebar.subheader("About")
    st.sidebar.caption("Built by Grant Armstrong and Ethan O'Mahony")

    # Uncomment to show debug info
    # st.subheader("Debug")
    # st.write(st.session_state)


def kickoff_crew():
    inputs = {
        "location": st.session_state.location if st.session_state.location else "Washington D.C.",
        "no_rooms": st.session_state.no_rooms,
        "budget_min": st.session_state.budget[0],
        "budget_max": st.session_state.budget[1],
    }

    human_message = f"""
    I'm looking for a property in {inputs["location"]} with {inputs["no_rooms"]} rooms.
    My budget is between {inputs["budget_min"]} and {inputs["budget_max"]} per month.
    """

    display_chat_message("human", human_message)
    st.session_state.messages.append({"role": "human", "content": human_message})

    result = PropertyHunterCrew().crew().kickoff(inputs=inputs)

    display_chat_message("assistant", result)
    st.session_state.messages.append({"role": "assistant", "content": result})


def main():
    """Execution starts here."""
    init_chat_history()
    display_chat_messages()
    display_sidebar_ui()


if __name__ == "__main__":
    main()
