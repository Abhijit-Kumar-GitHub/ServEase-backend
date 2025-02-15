from flask import Blueprint, request, jsonify, stream_with_context, Response
#from app import db  # Import the Firestore database instance if needed

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

# NO gemini_service Initialization Here!  It will be passed in during blueprint registration

def init_chatbot_routes(gemini_service):
    """
    Initializes the chatbot routes with the Gemini service.
    This allows dependency injection and avoids re-initialization.
    """

    # @chatbot_bp.route('/chat', methods=['POST'])
    # def chat():
    #     """
    #     Endpoint to receive a user message and return a Gemini-generated response.
    #     """
    #     data = request.get_json()
    #     if not data or 'message' not in data:
    #         return jsonify({'error': 'Missing message in request'}), 400

    #     user_message = data['message']
    #     response = gemini_service.generate_response(user_message)  # Use the service
    #     return jsonify({'response': response})


    @chatbot_bp.route('/stream', methods=['POST'])
    def stream_chat():
        """
        Endpoint for streaming the Gemini-generated response.
        """
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message in request'}), 400

        user_message = data['message']

        def generate():
            for chunk in gemini_service.generate_streaming_response(user_message):
                yield chunk

        return Response(stream_with_context(generate()), mimetype='text/plain')

    @chatbot_bp.route('/health', methods=['GET'])
    def health_check():
        """
        Simple health check endpoint for the chatbot.
        """
        return jsonify({'status': 'ok'})

    return chatbot_bp # Return the blueprint after modifying it