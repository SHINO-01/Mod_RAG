import gradio as gr
import base64
from utils import session_manager, ui_components

# Global storage for saved chat sessions
chat_sessions = {}

with open("assets/W3_Nobg.png", "rb") as img_file:
    base64_str = base64.b64encode(img_file.read()).decode()

markdown_content = f"""
<h1 style="display: flex; align-items: center; gap: 10px;">
    <img src="data:image/png;base64,{base64_str}" width="40"/>W3 BrainBot
</h1>
"""

# Initialize the Session Manager
session_manager = session_manager.SessionManager()

# =============================================
#    Gradio UI Setup with Blocks
# =============================================
def handle_message(user_input, history, session_list):
    return session_manager.handle_message(user_input, history, session_list)

def start_new_chat(chat_history, session_list):
    return session_manager.start_new_chat(chat_history, session_list)

def load_chat(selected_index_str, session_list):
    return session_manager.load_chat(selected_index_str, session_list)

with gr.Blocks(
    head=ui_components.UIComponents.get_custom_js(),
    theme=gr.themes.Base(primary_hue="blue", neutral_hue="gray", text_size=gr.themes.sizes.text_md),
    css=ui_components.UIComponents.get_global_css()
) as demo:
    with gr.Row(min_height=700):
        # Sidebar
        with gr.Column(scale=1, elem_classes=["sidebar"], min_width=250):
            gr.Markdown(markdown_content)
            new_chat_btn = gr.Button("＋ New Chat", elem_classes=["new-chat-btn", "spaced-icon-btn"], interactive=False)
            session_list = gr.State([])
            session_html = gr.HTML("<div class='session-list'></div>")
            session_select_callback = gr.Textbox(
                elem_id="session-select-callback", 
                visible=False,
                interactive=True
            )

        # Main Chat UI
        with gr.Column(min_width=1100, scale=30, elem_classes=["main-chat-ui"]):
            chatbot = gr.Chatbot(
                show_label=False,
                type="messages",
                min_height=790,
                min_width=600,
                height=650,
                container=False,
                avatar_images=["assets/USR_small.png", "assets/W3_Nobg_ssmall.png"],
                layout="bubble",
            )

            with gr.Row():
                message_input = gr.MultimodalTextbox(
                    show_label=False, 
                    placeholder="Type your message here...",
                    scale=10,
                    elem_id="message-input",
                    max_plain_text_length=8000,
                    max_lines=8000,
                )

            chat_history = gr.State([])

            # Send message handler
            message_input.submit(
                handle_message,
                inputs=[message_input, chat_history, session_list],
                outputs=[chatbot, message_input, session_list, session_html]
            ).then(
                lambda: gr.update(interactive=True),
                outputs=[new_chat_btn]
            ).then(
                lambda x: x,
                inputs=[chatbot],
                outputs=[chat_history]
            )

            # "New Chat" button
            new_chat_btn.click(
                start_new_chat,
                inputs=[chat_history, session_list],
                outputs=[chatbot, chat_history, session_list, session_html]
            ).then(
                lambda: gr.update(interactive=False),
                outputs=[new_chat_btn]
            )

            # Load a past session
            session_select_callback.input(
                load_chat,
                inputs=[session_select_callback, session_list],
                outputs=[chatbot]
            ).then(
                lambda x: x,
                inputs=[chatbot],
                outputs=[chat_history]
            )

            demo.load(
                lambda: ([{"role": "assistant", "content": "👋 Welcome to W3 BrainBot!"}], ["New Chat"], ui_components.UIComponents.create_session_html(["New Chat"])),
                outputs=[chatbot, session_list, session_html]
            ).then(
                lambda: gr.update(interactive=False),
                outputs=[new_chat_btn]
            )

demo.launch(favicon_path='assets/W3_Nobg.png', server_name="192.168.0.35", server_port=8080)
