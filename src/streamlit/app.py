import streamlit as st
import os
from crew import PropertyHunterCrew


def init_chat_history():
    """Create a st.session_state.messages list to store chat messages"""
    if "messages" not in st.session_state:
        clear_chat_history()


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hey. I'm Proppy, an agent designed to find rental properties in your area that fit all your needs. Try asking me about properties in your area."}]
    st.session_state.chat_aborted = False


def display_chat_messages():
    # Set assistant icon to Snowflake logo
    icons = {"assistant": "./house.png", "human": None}

    # Display the messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.write(message["content"])


def display_sidebar_ui():
    # with st.sidebar:
    st.sidebar.title('Property Hunter')
    st.sidebar.subheader("Model inputs")

    st.sidebar.text_input("Location", key="location", placeholder="Washington D.C.")
    st.sidebar.number_input("No. of rooms", min_value=1, key="no_rooms", placeholder="1")
    st.sidebar.slider("Budget", min_value=0, max_value=10000, value=(0, 10000), step=100, key="budget", )

    if st.sidebar.button("Kickoff Crew"):
        kickoff_crew()
        
    # st.sidebar.button("Reset", on_click=clear_chat_history(), type="primary")
    # st.sidebar.caption("Built by Grant Armstrong and Ethan O'Mahony")

    st.sidebar.subheader("About")
    st.sidebar.caption("Built by Grant Armstrong and Ethan O'Mahony")

        # # # Uncomment to show debug info
    # st.subheader("Debug")
    # st.write(st.session_state)


def kickoff_crew():
    inputs={
        "location": st.session_state.location, 
        "no_rooms": st.session_state.no_rooms,
        "budget": (st.session_state.budget[0], st.session_state.budget[1])
    }

    # PropertyHunterCrew().crew().kickoff(inputs=inputs)

    # st.session_state.messages.append({"role": "user", "content": str(inputs)})
    # st.write(inputs)
    # display_chat_message("user", inputs)
    # st.session_state

    st.chat_message("user").write(inputs)
    st.session_state.messages.append({"role": "user", "content": inputs})


def display_chat_message(role, content):
    icons = {"assistant": "./house.png", "user": "⛷️"}
    with st.chat_message(role, avatar=icons[role]):
        st.write_stream(content)


def get_and_process_prompt():
    """Get the user prompt and process it"""
    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="./house.png"):
            response = generate_response()
            st.write_stream(response)

    if st.session_state.chat_aborted:
        # st.button('Reset chat', on_click=clear_chat_history, key="clear_chat_history")
        st.chat_input(disabled=True)
    # elif prompt := st.chat_input():
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     st.rerun()


def generate_response():
    """String generator for the Snowflake Arctic response."""
    # for dict_message in st.session_state.messages:
    #     if dict_message["role"] == "user":
    #         topic = dict_message["content"]
    
    # chat_completion = generate_article(topic)

    # st.session_state.messages.append({"role": "assistant", "content": ""})
    # st.session_state.messages[-1]["content"] += str(chat_completion)

    # yield str(chat_completion)
    # Final safety check...
    # if not check_safety():
    #     abort_chat("I cannot answer this question.")


def main():
    """Execution starts here."""
    init_chat_history()
    display_chat_messages()
    display_sidebar_ui()


if __name__ == "__main__":
    main()
