import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox


class TextViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 윈도우 설정
        self.setWindowTitle("텍스트 뷰어")
        self.setGeometry(100, 100, 800, 600)

        # 텍스트 에디터 위젯 추가
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # 메뉴바 생성
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("파일")

        # "열기" 액션 추가
        open_action = QAction("열기", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # "종료" 액션 추가
        exit_action = QAction("종료", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        # 파일 열기 대화상자 표시
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "텍스트 파일 열기", "", "텍스트 파일 (*.txt);;모든 파일 (*)", options=options)

        if file_path:
            try:
                with open(file_path, 'rt', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 열 수 없습니다:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TextViewer()
    viewer.show()
    sys.exit(app.exec_())