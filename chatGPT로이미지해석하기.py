import sys
import os
import base64
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, 
                            QWidget, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import requests
import json


# API 키 직접 설정
API_KEY = ""

class DemoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_path = None
        self.api_key = API_KEY  # 직접 API 키 값을 설정
        
        if not self.api_key:
            QMessageBox.warning(self, "API 키 누락", 
                              "OpenAI API 키가 설정되지 않았습니다.")
    
    def initUI(self):
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # 제목 라벨
        title_label = QLabel("이미지 분석 애플리케이션")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 이미지 선택 버튼
        self.select_button = QPushButton("이미지 선택")
        self.select_button.clicked.connect(self.select_image)
        button_layout.addWidget(self.select_button)
        
        # 이미지 분석 버튼
        self.analyze_button = QPushButton("이미지 분석")
        self.analyze_button.clicked.connect(self.analyze_image)
        self.analyze_button.setEnabled(False)  # 이미지가 선택되기 전에는 비활성화
        button_layout.addWidget(self.analyze_button)
        
        main_layout.addLayout(button_layout)
        
        # 이미지 표시 영역
        self.image_label = QLabel("이미지가 여기에 표시됩니다")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(300)
        self.image_label.setStyleSheet("border: 1px solid #cccccc;")
        main_layout.addWidget(self.image_label)
        
        # 분석 결과 표시 영역
        self.result_label = QLabel("분석 결과:")
        main_layout.addWidget(self.result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(150)
        main_layout.addWidget(self.result_text)
        
        # 메인 위젯 설정
        self.setCentralWidget(main_widget)
        
        # 윈도우 설정
        self.setWindowTitle('OpenAI 이미지 분석')
        self.setGeometry(300, 300, 700, 600)
        self.show()
    
    def select_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "이미지 파일 선택", "", 
            "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif);;모든 파일 (*)", 
            options=options)
        
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            
            # 이미지 크기 조정 (라벨에 맞게)
            pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), 
                                  Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.image_label.setPixmap(pixmap)
            self.analyze_button.setEnabled(True)
            self.result_text.clear()
    
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "오류", "먼저 이미지를 선택해주세요.")
            return
        
        if not self.api_key:
            QMessageBox.warning(self, "API 키 누락", 
                               "OpenAI API 키가 설정되지 않았습니다.")
            return
        
        try:
            # GUI를 일시적으로 비활성화
            self.select_button.setEnabled(False)
            self.analyze_button.setEnabled(False)
            self.result_text.setText("이미지 분석 중...")
            QApplication.processEvents()  # UI 업데이트
            
            # 이미지를 base64로 인코딩
            base64_image = self.encode_image(self.image_path)
            
            # OpenAI API 호출
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "이 이미지에 대해 자세히 설명해 주세요. 무엇이 보이는지, 어떤 상황인지 분석해 주세요."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                    headers=headers, json=payload)
            
            # 응답 처리
            if response.status_code == 200:
                result = response.json()
                analysis_text = result["choices"][0]["message"]["content"]
                self.result_text.setText(analysis_text)
            else:
                error_message = f"API 호출 오류: {response.status_code}\n{response.text}"
                self.result_text.setText(error_message)
                QMessageBox.critical(self, "API 오류", error_message)
        
        except Exception as e:
            self.result_text.setText(f"오류 발생: {str(e)}")
            QMessageBox.critical(self, "오류", f"처리 중 오류가 발생했습니다: {str(e)}")
        
        finally:
            # GUI 다시 활성화
            self.select_button.setEnabled(True)
            self.analyze_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoForm()
    sys.exit(app.exec_())