from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_model():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Assuming Ollama model can be queried with a subprocess command
    result = subprocess.run(["ollama", "query", question], capture_output=True, text=True)
    answer = result.stdout.strip()

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
