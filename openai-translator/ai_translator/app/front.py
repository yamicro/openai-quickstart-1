import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox, QFileDialog
import requests  # 引入 requests 库
import subprocess
import webbrowser
import os


class TranslatorApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Translator')
        self.setGeometry(100, 100, 200, 100)
        self.config = {}
        # 布局
        layout = QVBoxLayout()
        
        # 文件选择按钮
        self.btnSelectFile = QPushButton('Select PDF')
        self.btnSelectFile.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.btnSelectFile)
        
        # 输出格式下拉菜单
        self.comboBox = QComboBox()
        self.comboBox.addItems(["PDF", "MD"])
        layout.addWidget(self.comboBox)
        
        # 翻译按钮
        self.btnTranslate = QPushButton('Translate')
        self.btnTranslate.clicked.connect(self.translate)
        layout.addWidget(self.btnTranslate)
        
        self.setLayout(layout)
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;PDF Files (*.pdf)", options=options)
        if fileName:
            self.config['file_path'] =  fileName # 这里你可以保存文件路径并在翻译函数中使用

    def translate(self):
        # 这里添加调用翻译逻辑的代码
        print("Translate the file")
        selectedFormat = self.comboBox.currentText()
        print(f"Selected format: {selectedFormat}")
        self.config['file_format'] = selectedFormat

        file_path = self.config.get('file_path')  # 假设这是用户选择的文件路径
        
        if file_path:
            # 构建要发送的文件和数据
            files = {'pdf': open(file_path, 'rb')}
            data = {'outputFormat': selectedFormat}
            
            # 发送POST请求到Flask后端
            response = requests.post('http://127.0.0.1:5000/upload-and-translate-pdf', files=files, data=data)
            
            if response.status_code == 200:
                print("翻译成功:", response.json())  # 或者其他逻辑处理
                translated_file_path = response.json().get('translated_file_path')
            
                # 如果是Windows系统，使用os.startfile打开文件
                if os.name == 'nt':
                    os.startfile(translated_file_path)
                # 对于macOS, 使用"open"
                elif sys.platform == "darwin":
                    subprocess.call(["open", translated_file_path])
                # 对于Linux, 使用"xdg-open"
                else:
                    subprocess.call(["xdg-open", translated_file_path])
            else:
                print("翻译失败")
        else:
            print("没有选择文件")
