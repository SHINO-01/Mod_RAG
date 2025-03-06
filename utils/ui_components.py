import os

class UIComponents:
    
    @staticmethod
    def get_global_css():
        # Return the global CSS as a string
        return open('static/styles.css', 'r').read()

    @staticmethod
    def get_custom_js():
        # Build the path to the static/script.js file
        static_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'script.js')
        with open(static_path, 'r') as f:
            js_content = f.read()
        # Wrap the JS code in <script> tags
        return f"<script>{js_content}</script>"

    @staticmethod
    def create_session_html(sessions):
        html = "<div class='session-list'>"
        for i, session in enumerate(sessions):
            if session == "New Chat":
                continue
            html += f"""
            <div class="session-item" data-index="{i}">
                <div class="session-name">{session}</div>
                <div class="options" data-session-id="{i}">⁝</div>
            </div>
            """
        html += "</div>"
        html += """<div id='modal' class='modal'>
                        <div class='modal-content'>
                            <button class='rename-btn'>Rename</button>
                            <button class='delete-btn'>Delete</button>
                        </div>
                    </div>"""
        return html
