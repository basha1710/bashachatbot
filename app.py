from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

# Set your API key for the generative AI
GOOGLE_API_KEY = "AIzaSyC8L1FxK7ksv7vdFIszIshUxQsu_UYkYbA"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

# Initialize Flask app
app = Flask(__name__)

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BASHA Chat Application</title>
        <!-- Bootstrap CSS -->
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body, html {
                height: 100%;
                margin: 0;
                font-family: 'Arial', sans-serif;
                background-color: #f0f4f8;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .chat-container {
                width: 100%;
                max-width: 800px;
                height: 90vh;
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                display: flex;
                flex-direction: column;
            }

            .chat-header {
                background-color: #4A90E2;
                padding: 20px;
                color: white;
                font-size: 22px;
                font-weight: bold;
                text-align: center;
                border-radius: 12px 12px 0 0;
            }

            .chat-body {
                padding: 20px;
                flex-grow: 1;
                overflow-y: auto;
                background-color: #F9F9F9;
                border-radius: 0 0 12px 12px;
            }

            .chat-footer {
                display: flex;
                padding: 15px;
                background-color: #F1F1F1;
                border-top: 1px solid #ddd;
            }

            .chat-footer input {
                flex-grow: 1;
                padding: 15px;
                font-size: 16px;
                border-radius: 25px;
                border: 1px solid #ddd;
                margin-right: 10px;
                height: 45px;
                box-sizing: border-box;
                transition: all 0.3s;
            }

            .chat-footer input:focus {
                border-color: #4A90E2;
                outline: none;
                box-shadow: 0 0 5px rgba(74, 144, 226, 0.5);
            }

            .send-button {
                background-color: #4A90E2;
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s;
                padding: 12px 20px;
            }

            .send-button:hover {
                background-color: #357ABD;
            }

            .chat-message {
                padding: 12px;
                border-radius: 20px;
                margin: 10px 0;
                max-width: 80%;
                word-wrap: break-word;
            }

            .chat-message.user {
                background-color: #4A90E2;
                color: white;
                margin-left: auto;
                margin-right: 10px;
            }

            .chat-message.bot {
                background-color: #F1F1F1;
                color: #333;
                margin-left: 10px;
                margin-right: auto;
            }

            .chat-message-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .fab {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #4A90E2;
                color: white;
                font-size: 24px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                transition: background-color 0.3s;
            }

            .fab:hover {
                background-color: #357ABD;
            }

        </style>
    </head>
    <body>

        <div class="chat-container">
            <div class="chat-header">
                BASHA Chat
            </div>

            <div class="chat-body" id="chat-body">
                <div class="chat-message-container" id="chat-messages">
                    <!-- Chat messages will go here -->
                </div>
            </div>

            <div class="chat-footer">
                <input type="text" id="message-input" placeholder="Type your message here...">
                <button class="send-button" id="send-button">Send</button>
            </div>
        </div>

        <div class="fab" id="fab">
            <i class="fas fa-cogs"></i> <!-- Add icons for settings or other options -->
        </div>

        <!-- jQuery and Bootstrap JS -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.6/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.min.js"></script>
        <script src="https://kit.fontawesome.com/a076d05399.js"></script>
        <script>
            $(document).ready(function () {

                // Handle message send on button click or Enter key
                $('#send-button').click(function () {
                    sendMessage();
                });

                $('#message-input').keypress(function (e) {
                    if (e.which === 13) { // Enter key
                        sendMessage();
                    }
                });

                // Function to send the message to the server
                function sendMessage() {
                    var userMessage = $('#message-input').val().trim();
                    if (userMessage) {
                        $('#chat-messages').append('<div class="chat-message user">' + userMessage + '</div>');
                        $('#message-input').val("");  // Clear input field
                        $('#chat-body').scrollTop($('#chat-body')[0].scrollHeight);  // Scroll to bottom

                        $.ajax({
                            url: '/chat',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({ "message": userMessage }),
                            success: function (response) {
                                $('#chat-messages').append('<div class="chat-message bot">' + response.response + '</div>');
                                $('#chat-body').scrollTop($('#chat-body')[0].scrollHeight);
                            },
                            error: function (xhr, status, error) {
                                console.error("Error: " + error);
                            }
                        });
                    }
                }

                // Floating Action Button (FAB) Click Event
                $('#fab').click(function () {
                    alert("Settings or additional options can be added here!");
                });
            });
        </script>
    </body>
    </html>
    ''')

# Route to handle chat interactions
@app.route('/chat', methods=['POST'])
def chat_response():
    try:
        user_input = request.get_json().get('message')

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Send the user's message to the generative model
        response_raw = chat.send_message(user_input)
        response = response_raw.text

        return jsonify({"response": response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app on all network interfaces (0.0.0.0)
    app.run(debug=True, host='0.0.0.0', port=5000)

