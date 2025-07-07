import sys, os, logging
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog,
    QVBoxLayout, QHBoxLayout, QListWidget, QProgressBar,
    QComboBox, QMessageBox, QPlainTextEdit, QTabWidget
)
from PyQt6.QtGui import QIcon, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, QTimer

from compressor import compress_files
from decompressor import decompress_file

# === ЛОГИРОВАНИЕ ===
def init_logger():
    try:
        log_dir = os.path.join(os.getenv("APPDATA"), "HACArchiver")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "log.txt")
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
        logging.info("=== HACArchiver запущен ===")
    except Exception as e:
        print(f"[!] Не удалось инициализировать логгер: {e}")

def get_log_path():
    return os.path.join(os.getenv("APPDATA"), "HACArchiver", "log.txt")

init_logger()


class HACArchiver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HACArchiver ⚡")
        self.setWindowIcon(QIcon(resource_path("ui/icon.ico")))
        self.setAcceptDrops(True)
        self.setFixedSize(520, 540)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(10, 10, 500, 520)

        self.archive_tab = QWidget()
        self.log_tab = QWidget()

        self.init_archive_tab()
        self.init_log_tab()

        self.tabs.addTab(self.archive_tab, "📦 Архивация")
        self.tabs.addTab(self.log_tab, "📝 Журнал событий")

        # Обновление журнала раз в 3 секунды
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_logs)
        self.timer.start(3000)

    def init_archive_tab(self):
        layout = QVBoxLayout()

        self.label = QLabel("Перетащите файлы/папки или используйте кнопки ниже")
        self.file_list = QListWidget()
        self.compress_button = QPushButton("📦 Сжать")
        self.decompress_button = QPushButton("📂 Распаковать")
        self.progress = QProgressBar()
        self.level_select = QComboBox()
        self.level_select.addItems(["Низкий", "Средний", "Максимальный"])

        btns = QHBoxLayout()
        btns.addWidget(self.compress_button)
        btns.addWidget(self.decompress_button)

        layout.addWidget(self.label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.level_select)
        layout.addWidget(self.progress)
        layout.addLayout(btns)

        self.compress_button.clicked.connect(self.compress)
        self.decompress_button.clicked.connect(self.decompress)

        self.archive_tab.setLayout(layout)

    def init_log_tab(self):
        layout = QVBoxLayout()
        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)
        self.log_tab.setLayout(layout)
        self.load_logs()

    def load_logs(self):
        try:
            with open(get_log_path(), 'r', encoding='utf-8', errors='ignore') as f:
                self.log_view.setPlainText(f.read())
                
        except Exception as e:
            self.log_view.setPlainText(f"[Ошибка чтения лога]: {e}")

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            self.file_list.addItem(path)
            logging.info(f"Добавлен путь через drag-n-drop: {path}")

    def compress(self):
        try:
            files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
            if not files:
                QMessageBox.warning(self, "Нет файлов", "Добавьте файлы или папки.")
                return
            level = self.level_select.currentIndex()
            logging.info(f"Начато сжатие файлов: {files} | Уровень: {level}")
            self.progress.setValue(10)
            archive = compress_files(files, level)
            self.progress.setValue(100)
            QMessageBox.information(self, "Успех", f"Сжато в: {archive}")
            logging.info(f"Сжатие завершено: {archive}")
        except Exception as e:
            logging.error(f"Ошибка при сжатии: {e}", exc_info=True)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сжатии:\n{e}")

    def decompress(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Выберите архив .hac", filter="HAC (*.hac)")
            if not file_path:
                return
            logging.info(f"Начата распаковка архива: {file_path}")
            self.progress.setValue(10)
            out = decompress_file(file_path)
            self.progress.setValue(100)
            QMessageBox.information(self, "Готово", f"Распаковано в: {out}")
            logging.info(f"Распаковка завершена: {out}")
        except Exception as e:
            logging.error(f"Ошибка при распаковке: {e}", exc_info=True)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при распаковке:\n{e}")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open(resource_path("ui/style.qss"), "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        logging.warning(f"Не удалось загрузить стиль: {e}")

    win = HACArchiver()
    win.show()
    sys.exit(app.exec())
