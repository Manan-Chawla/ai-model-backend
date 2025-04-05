from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
CORS(app)

@app.route('/benchmark', methods=['POST'])
def benchmark():
    file = request.files.get('model')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    return jsonify({
        'model_name': file.filename,
        'accuracy': 90.5,
        'inference_time': 47,
        'memory_usage': 123
    })

@app.route("/compare", methods=["POST"])
def compare_models():
    try:
        print("COMPARE REQUEST RECEIVED")
        print("FILES RECEIVED:", request.files)

        file1 = request.files.get("model1")
        file2 = request.files.get("model2")

        if not file1 or not file2:
            print("Missing files!")
            return jsonify({"error": "Both model files are required."}), 400

        result1 = benchmark_model(file1)
        result2 = benchmark_model(file2)

        print("RESULT 1:", result1)
        print("RESULT 2:", result2)

        # Save PDF Report
        save_report(result1, result2)

        return jsonify({
            "model1": result1,
            "model2": result2
        })

    except Exception as e:
        print("Comparison Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Model Comparison Report")
    c.drawString(50, 720, f"Model 1: {data['model1']['model_name']}")
    c.drawString(50, 700, f"Accuracy: {data['model1']['accuracy']}%")
    c.drawString(50, 680, f"Inference Time: {data['model1']['inference_time']}ms")
    c.drawString(50, 660, f"Memory Usage: {data['model1']['memory_usage']}MB")

    c.drawString(50, 620, f"Model 2: {data['model2']['model_name']}")
    c.drawString(50, 600, f"Accuracy: {data['model2']['accuracy']}%")
    c.drawString(50, 580, f"Inference Time: {data['model2']['inference_time']}ms")
    c.drawString(50, 560, f"Memory Usage: {data['model2']['memory_usage']}MB")

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='model_comparison.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
