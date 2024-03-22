import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator
import threading
from flask import Flask, request, jsonify
from app.front import TranslatorApp
from PyQt5.QtWidgets  import QApplication

# if __name__ == "__main__":
#     argument_parser = ArgumentParser()
#     args = argument_parser.parse_arguments()
#     config_loader = ConfigLoader(args.config)

#     config = config_loader.load_config()

#     model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
#     api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
#     model = OpenAIModel(model=model_name, api_key=api_key)


#     pdf_file_path = args.book if args.book else config['common']['book']
#     file_format = args.file_format if args.file_format else config['common']['file_format']

#     # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
#     translator = PDFTranslator(model)
#     translator.translate_pdf(pdf_file_path, file_format)
app = Flask(__name__)

# Initialize your models and configs outside of the request handling to avoid re-loading for each request
argument_parser = ArgumentParser()
args = argument_parser.parse_arguments()
config_loader = ConfigLoader(args.config)
config = config_loader.load_config()

model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
model = OpenAIModel(model=model_name, api_key=api_key)

UPLOAD_FOLDER = 'storage'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload-and-translate-pdf', methods=['POST'])
def upload_and_translate_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdf']
    file_format = request.form.get('outputFormat')
    print(f"file_format: {file_format}")
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        # 确保 storage 文件夹存在
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # 构建文件的保存路径
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        
        # 保存文件
        file.save(file_path)

        # 在这里调用处理函数来处理上传的PDF
        try:
            # 实例化PDFTranslator并传入模型
            translator = PDFTranslator(model=model)
            # 假设您希望处理完的文件保存在同一个目录，文件名相同但后缀为.txt
            output_file_path = os.path.splitext(file_path)[0] + file_format
            # 调用处理函数
            translator.translate_pdf(pdf_file_path=file_path,file_format=file_format,output_file_path=output_file_path)
            return jsonify({'message': f'File {file.filename} uploaded and processed successfully.', 'translated_file_path': output_file_path}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to process the file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Unsupported file format'}), 400

def run_flask():
    app.run(debug=True, use_reloader=False) 

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    app1 = QApplication(sys.argv)
    ex = TranslatorApp()
    ex.show()
    sys.exit(app1.exec_())
    app1.run()
