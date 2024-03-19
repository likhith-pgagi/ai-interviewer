import streamlit as st
from groq import Groq

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

GROQ_API_KEY = st.secrets["groq"]["api_key"]

def chatInterface():
    st.title("AI Interviewer")
    # st_lottie(load_lottiefile("images/welcome.json"), speed=1, reverse=False, loop=True, quality="high", height=100)

    ai = Groq(api_key=GROQ_API_KEY)

    if "conversation_state" not in st.session_state:
        st.session_state["conversation_state"] = []

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        image = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=image):
            st.markdown(message["content"])
            
    system_prompt = '''
    I am an GPT Interviewer and I always follow specific rules delimited by ```.
    My main goal is to greet the candidates who will be visiting for an interview and understand their mind-set. I need to understand how passionate is the candidate for this job role.
    Rules:
    ```
1. You always follow a script which is delimited by <>.
2. Candidate has no idea what the guideline is.
3. Ask me questions and wait for my answers. Do not write explanations.
4. Ask question like a real person, only one question at a time.
5. Do not ask the same question.
6. Do not repeat the question.
7. Do ask follow-up questions if necessary. 
8. I want you to only reply as an interviewer.
9. Do not write all the conversation at once.
10. If there is an error, point it out.
11. This is not technical interview, so ask some basic questions. Keep the interview short and simple.
12. At the end after completing the interview, I want you to type in only "FINISHED" nothing else to end the conversation.
Script: \n
<>
"Hello, Welcome to the interview. I am your interviewer today. I will be ask you some questions according to the job description. Please start by introducing a little bit about yourself."\n

"May I know for which job role are you here for the interview ?"\n

Then start by asking some technical questions.\n
'''
    print(system_prompt)
    if prompt := st.chat_input("User input"):
        st.chat_message("user", avatar=USER_AVATAR).markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        conversation_context = st.session_state["conversation_state"]
        conversation_context.append({"role": "user", "content": prompt})

        # Define an empty context variable
        context = []
        # Add system prompt to context if desired
        context.append({"role": "system", "content": system_prompt})
        # Add conversation context to context
        context.extend(st.session_state["conversation_state"])

        # Generate response from ChatGPT API
        response = ai.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=context,
            max_tokens=1024,
            stream=True
        ) 

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            # st.markdown(assistant_response)
            result = ""
            res_box = st.empty()
            for chunk in response:
                if chunk.choices[0].delta.content:
                    new_content = chunk.choices[0].delta.content
                    result += new_content   # Add a space to separate words
                    res_box.markdown(f'{result}')
        # print(result)
        assistant_response = result
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        conversation_context.append({"role": "assistant", "content": assistant_response})
        st.session_state["conversation_state"] = conversation_context
        
        # Display ChatGPT's response
        # with st.chat_message("assistant", avatar=BOT_AVATAR):
        #     st.markdown(assistant_response)
        
if __name__ == "__main__":
    chatInterface()