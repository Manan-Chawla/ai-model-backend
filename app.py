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

@app.route('/compare', methods=['POST'])
def compare():
    model1 = request.files.get('model1')
    model2 = request.files.get('model2')
    if not model1 or not model2:
        return jsonify({'error': 'Both models required'}), 400

    # Dummy results
    return jsonify({
        'model1': {
            'model_name': model1.filename,
            'accuracy': 88.2,
            'inference_time': 53,
            'memory_usage': 110
        },
        'model2': {
            'model_name': model2.filename,
            'accuracy': 91.1,
            'inference_time': 49,
            'memory_usage': 130
        }
    })

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
