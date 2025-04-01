"""Learning Objectives Chatbot Application."""

import streamlit as st
from streamlit_chat import message
import pandas as pd

from learning_objectives_chatbot.utils import (
    generate_response,
    get_sample_objectives,
    analyze_objective,
    suggest_improvements
)


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="Learning Objectives Chatbot",
        page_icon="🎯",
        layout="wide"
    )

    st.title("Learning Objectives Chatbot")
    st.write(
        """
        Welcome to the Learning Objectives Assistant! This tool will help you create
        effective learning objectives through guided conversation. Whether you're an
        educator, trainer, or instructional designer, this chatbot will ask you relevant
        questions to refine your learning objectives.
        """
    )

    # Initialize session state variables if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your Learning Objectives Assistant. What subject or skill are you creating learning objectives for?"}
        ]
    
    if "current_objective" not in st.session_state:
        st.session_state.current_objective = ""
    
    if "objective_history" not in st.session_state:
        st.session_state.objective_history = []

    # Create two columns for layout
    col1, col2 = st.columns([2, 1])

    # Chat interface in the first column
    with col1:
        st.subheader("Chat")
        
        # Display chat messages
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "assistant":
                message(msg["content"], key=f"assistant_{i}")
            else:
                message(msg["content"], is_user=True, key=f"user_{i}")
        
        # Chat input - Use a form to prevent rerun loops
        with st.form(key="message_form"):
            user_input = st.text_input("Type your message here...", key="user_input")
            submit_button = st.form_submit_button("Send")
            
        # Process the message when the form is submitted
        if submit_button and user_input:
            # Store the current input
            current_input = user_input
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": current_input})
            
            # Generate response
            response = generate_response(current_input, st.session_state.messages)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # If response contains a learning objective suggestion, save it
            if "Here's a possible learning objective:" in response:
                objective = response.split("Here's a possible learning objective:")[1].strip()
                st.session_state.current_objective = objective
                if objective not in st.session_state.objective_history:
                    st.session_state.objective_history.append(objective)
            
            # Clear the input field by forcing a rerun once
            st.rerun()

    # Learning objectives panel in the second column
    with col2:
        st.subheader("Learning Objectives")
        
        # Current objective analysis
        if st.session_state.current_objective:
            st.write("**Current Objective:**")
            st.info(st.session_state.current_objective)
            
            # Analyze the current objective
            analysis = analyze_objective(st.session_state.current_objective)
            
            # Display the analysis
            st.write("**Analysis:**")
            st.write(f"- **Bloom's Level:** {analysis['blooms_level']}")
            st.write(f"- **Measurable:** {'Yes' if analysis['measurable'] else 'No'}")
            st.write(f"- **Clarity:** {analysis['clarity_score']}/10")
            
            # Suggestions for improvement
            improvements = suggest_improvements(analysis)
            if improvements:
                st.write("**Suggestions for Improvement:**")
                for suggestion in improvements:
                    st.write(f"- {suggestion}")
        
        # Objective history
        if st.session_state.objective_history:
            st.subheader("Objective History")
            for i, obj in enumerate(st.session_state.objective_history):
                with st.expander(f"Objective {i+1}"):
                    st.write(obj)
        
        # Example objectives section
        with st.expander("Example Learning Objectives"):
            examples = get_sample_objectives()
            for category, objectives in examples.items():
                st.write(f"**{category}:**")
                for obj in objectives:
                    st.write(f"- {obj}")

    # Reset conversation button
    if st.button("Start New Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your Learning Objectives Assistant. What subject or skill are you creating learning objectives for?"}
        ]
        st.session_state.current_objective = ""
        st.rerun()


if __name__ == "__main__":
    main()