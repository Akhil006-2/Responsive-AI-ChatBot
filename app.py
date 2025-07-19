import streamlit as st#main library to create the frontend UI
from streamlit_chat import message#ithu vanthu display chat messages as bubble format 
import httpx #allows http requests (get,post,put,etc..)

API_URL = "http://localhost:8000/chat/stream"#route for connecting to the anthropic's response apro to send the user's input and chat history to this route via post
#7 and 8 lines are for the heading and browser tab title 
st.set_page_config(page_title="AI Chatbot (Claude Streaming)", page_icon="🤖", layout="centered")
st.title("🤖 AI Chatbot (Claude Streaming)")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("You:", key="input", placeholder="Type your message and press Enter...")#stores the current user-typed message
send_btn = st.button("Send")#becomees true when you click the send button 

if send_btn and user_input:
    st.session_state["history"].append({"role": "user", "content": user_input})#appends the chat history

    # Create a placeholder to stream Claude's reply live
    placeholder = st.empty()#to stream the bot's reply in real time (dynamic area)
    with st.spinner("Claude is thinking..."):#shows a loading spinner with the msg
        bot_reply = ""#bot starts as an empty string and is updated chunk by chunk then
        try:#this sends a streaming post request to the backend 
            with httpx.stream("POST", API_URL, json={# httpx.stream(..) it opens a streaming connection with the backend 
                "message": user_input,
                "history": st.session_state["history"]
            }, timeout=60.0) as r:# r is the streaming response object 
                for chunk in r.iter_text():#chunk is the one of the kuttie part of the AI reply
                    bot_reply += chunk #the chunks are added to the total response 
                    placeholder.markdown(f"🤖 **AI:** {bot_reply}▌") #replaces the placeholder with the updated markdown 
                print(f"The message from claude : {bot_reply}")
        except Exception as e: #error handling , to sshow the error in the UI
            bot_reply = f"⚠️ Error: {e}"
            st.error(bot_reply)

        st.session_state["history"].append({"role": "assistant", "content": bot_reply})# after the reply it appends the bot's reply to the histry
        st.rerun()

# Display full chat history
for i, msg in enumerate(st.session_state["history"]):
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user, key=str(i))
