# Building a basic LLM chat app with streamlit
> https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

## Notes

### Table of Contents

+ Go through Streamlit's chat elements: `st.chat_message` and `st.chat_input`.
+ Build a few apps to showcase increasing levels of complexity and functionality:
  + Build a bot that echoes the user's input to develop some intuition around how the chat elements and session state works.
  + Build a chatbot GUI with streaming
  + Build a ChatGPT-like app

The end state should look something like:

![End state](pics/end-state.png)

### Chat elements

`st.chat_message` lets you insert a chat message container into the app to display messages from the user or from the app.

Chat containers can contain other Streamlit elements (charts, tables, text...).

To add elements to the returned container, you can use `with` as seel below:

```python
import streamlit as st

with st.chat_message("user"):
  st.write("Hello, 👋")
```

Note that the first parameters is the name of the message author, which can be `"user"` or `"assistant"`/`"ai"` to enable preset styling and avatars. Note also that the name is not shown in the UI.

As stated above, you can add other Streamlit elements such as `st.bar_chart`:

```python
import streamlit as st

with st.chat_message("ai"):
  st.write("Here you are! A random bar chart")
  st.bar_chart(np.random.randn(30, 3))
```

While the `with` notation is the recommended one you can use the object return by `st.chat_message()` to obtain the same result:

```python
message_container = st.chat_message("ai")
message_container.write("Ask me anything!")
message_container.bar_chart(np.random.randn(10, 2))
```

`st.chat_input` lets you display a chat input widget so that the user can type in a message.

The returned values will be the user's input or `None` if the user hasn't sent a message yet.

You can also pass a default prompt to be displayed in the input widget:

```python
prompt = st.chat_input("Say something")
if prompt:
  st.write(f"user has written: {prompt!r}")
```

| EXAMPLE: |
| :------- |
| See [00: Hello, `st.chat_message`](docschat/00_hello_chat_message.py) and [01: Hello, `st.chat_input`](docschat/01_hello_chat_input.py) and runnable examples. |

## Build a bot that echoes your input

One of the most challenging parts when working with Streamlit is realizing that the Python program is executed from top to bottom on each user's interaction.

As a result, if you want to keep history between executions you have to rely on additional artifacts, such as the session state.

In this section, we will build a bot that echoes the user's input. That is, the bot will respond to your input with the same message.

A `st.chat_message` will be used to display user's input, and `st.chat_input` will be used to accept the user's input. The program will maintain the chat history in the session state.

The components to use are:
+ two chat message containers to display messages from the user and the bot, respectively.
+ a chat input widget, so the user can type in messages.
+ a list to store the messages and append to it every time the user or bot sends a message. Each entry in the list will be a dictionary with the keys `role` (author of the message) and `content` (message content).

| EXAMPLE: |
| :------- |
| See [02: Echo Bot](docschat/02_echo_bot.py) for a runnable example. |

## Build a simple chatbot GUI with streaming

In this section, we will build a chatbot that responds to the user's input with a random message from a list of pre-determined responses. The idea is to use it as a stepping stone to build a ChatGPT UI application in the final section.

| EXAMPLE: |
| :------- |
| See [03: Canned bot](docschat/03_canned_bot.py) for a runnable example. |

## Building a ChatGPT-like app with Azure OpenAI

In this section, we build a simple chatbot that interacts with an Azure OpenAI Chat model.

This will be later used to let the user select the knowledge base that will let the user talk to their files.

| EXAMPLE: |
| :------- |
| See [04: LLM bot](docschat/04_llm_bot.py) for a runnable example. |

