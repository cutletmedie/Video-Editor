from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QSlider, QVBoxLayout, \
    QHBoxLayout, QGroupBox, QTabWidget, QCheckBox


class QControlEffects(QGroupBox):
    def __init__(self, fragment=None):
        super().__init__()
        self.setup_ui()
        # self.setStyleSheet("""[class="QControlEffects"] {border: 0px;}""")

    def setup_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { /* The tab widget frame */
                border-top: 1px solid #bbbbbb;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background-color: transparent;
                border: 1px solid #323232;
                min-width: 80px;
                padding: 5px;
                color: #bbbbbb;
            }
            QTabBar::tab:selected {
                background-color: rgba(187, 187, 187, 0.1);
                border-bottom: 1px solid #bbbbbb;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
            QTabBar::tab:hover {
                
                background-color: #1f1f1f;
            }
            """)

        tabs.addTab(self.audioTabUI(), "Аудиоэффекты")
        tabs.addTab(self.videoTabUI(), "Видеоэффекты")
        layout.addWidget(tabs)
        self.setLayout(layout)

    def audioTabUI(self):
        """Create the General page UI."""
        audioTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("пососи"))
        layout.addWidget(QCheckBox("ну пожалуйста"))
        audioTab.setLayout(layout)
        return audioTab

    def videoTabUI(self):
        """Create the Network page UI."""
        videoTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("ну ладно"))
        layout.addWidget(QCheckBox("тогда не надо"))
        videoTab.setLayout(layout)
        return videoTab
