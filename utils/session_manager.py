from .ui_components import UIComponents

class SessionManager:
    def __init__(self):
        self.chat_sessions = {}
        
    def generate_chat_name(self):
        return "New Chat"

    def chatbot_response(self, user_input, chat_history):
        if isinstance(user_input, dict):  # e.g., user uploaded a file
            user_text = user_input.get("text", "")
        else:
            user_text = user_input.strip()

        if not user_text:
            return chat_history, ""  # Ignore empty messages

        bot_reply = f"You asked: '{user_text}'"
        updated_history = list(chat_history)
        updated_history.append({"role": "user", "content": user_text})

        if not bot_reply.strip():
            bot_reply = " "
        updated_history.append({"role": "assistant", "content": bot_reply})

        return updated_history, bot_reply

    def start_new_chat(self, chat_history, session_list):
        if chat_history:
            chat_name = session_list[0]
            self.chat_sessions[chat_name] = list(chat_history)

        if "New Chat" in session_list:
            session_list.remove("New Chat")

        chat_name = "New Chat"
        session_list.insert(0, chat_name)
        self.chat_sessions[chat_name] = [{"role": "assistant", "content": "🔄 New chat started!"}]

        session_html = UIComponents.create_session_html(session_list)
        return [{"role": "assistant", "content": "🔄 New chat started!"}], [], session_list, session_html

    def load_chat(self, selected_index_str, session_list):
        try:
            idx = int(selected_index_str)
            if 0 <= idx < len(session_list):
                chat_name = session_list[idx]
                if chat_name in self.chat_sessions:
                    return self.chat_sessions[chat_name]
        except (ValueError, TypeError):
            return []

        return []

    def handle_message(self, user_input, history, session_list):
        # Check if user_input is a dictionary and extract the text, otherwise treat it as a plain string
        if isinstance(user_input, dict):
            user_text = user_input.get("text", "").strip()
        else:
            user_text = str(user_input).strip()

        if not user_text:
            session_html = UIComponents.create_session_html(session_list)
            return history, "", session_list, session_html

        if not session_list:
            session_list.insert(0, "New Chat")
            self.chat_sessions["New Chat"] = [{"role": "assistant", "content": "🔄 New chat started!"}]

        chat_name = session_list[0]

        if chat_name == "New Chat":
            new_name = user_text[:20] + "..."
            session_list[0] = new_name
            if "New Chat" in self.chat_sessions:
                self.chat_sessions[new_name] = self.chat_sessions.pop("New Chat")
            else:
                self.chat_sessions[new_name] = []
            chat_name = new_name

        # Use the cleaned user_text in the chatbot_response function
        new_history, _ = self.chatbot_response(user_text, history)
        self.chat_sessions[chat_name] = new_history

        session_html = UIComponents.create_session_html(session_list)
        return new_history, "", session_list, session_html
