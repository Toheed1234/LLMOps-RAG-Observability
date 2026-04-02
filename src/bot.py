import streamlit as st
import phoenix as px
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register
from retriever import get_rag_chain

# Start Phoenix Server for Observability (starts locally on port 6006 - 100% private)
try:
    px.launch_app()
except Exception as e:
    pass # App might already be running

# Instrument Langchain to automatically capture all trace data
tracer_provider = register(project_name="LLMOps-RAG-Assistant")
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

st.title("🤖 Local RAG Assistant")
st.markdown("Ask me questions about your local documents! View traces in the [Phoenix Dashboard](http://localhost:6006)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick chat input
if prompt := st.chat_input("What is in your data?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Display a temporary thinking indicator so the UI is never blank
        message_placeholder.markdown("🧠 *Searching docs and thinking...*")
        
        chain = get_rag_chain()
        
        # Build a memory payload of the last 2 messages to save token space
        chat_history_str = ""
        for msg in st.session_state.messages[-2:]:
            role = "User" if msg["role"] == "user" else "AI"
            chat_history_str += f"{role}: {msg['content']}\n"
            
        response_stream = chain.stream({
            "question": prompt,
            "chat_history": chat_history_str
        })
        
        is_first_chunk = True
        
        # Stream the response chunk by chunk as LM Studio generates them
        for chunk in response_stream:
            # Clear the "Thinking..." text the exact millisecond the first token arrives
            if is_first_chunk:
                message_placeholder.empty()
                is_first_chunk = False
                
            full_response += chunk
            # Add a blinking block cursor to simulate real typing!
            message_placeholder.markdown(full_response + "▌")
            
        # Final render without the cursor
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
