import json
import os
import sys
from widgets.system_monitor import SystemMonitor

def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


from .voice_orb import VoiceOrb
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QFrame,
    QDialog,
    QLineEdit,
    QFileDialog,
    QTreeWidget,
    QTreeWidgetItem,
    QComboBox
)
from PySide6.QtCore import Qt, QTimer
import sys
from PySide6.QtGui import QIcon, QColor
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl



class JarvisMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        print("APP START")

        self.thinking_sound = QSoundEffect()

        self.thinking_sound.setSource(
            QUrl.fromLocalFile(
                resource_path("assets/sounds/thinking.wav")
            )
        )

        self.thinking_sound.setVolume(0.4)
        self.thinking_sound.setLoopCount(-2)

        self.mic_muted = False
        
        self.setWindowTitle("JARVIS HUD")
        self.resize(1800, 950)
        self.setWindowIcon(QIcon(resource_path("assets/jarvis_icon.ico")))

        self.build_ui()
        self.apply_theme()

    def apply_theme(self):

        self.setStyleSheet("""

        QWidget {
            background-color: #0D0D0D;
            color: #F5F5F5;
            font-family: 'Segoe UI';
            font-size: 14px;
        }

        QFrame {
            background-color: #171717;
            border: 1px solid #262626;
            border-radius: 20px;
        }

        QLabel {
            background: transparent;
            color: #FFFFFF;
        }

        QPushButton {
            background-color: #1F1F1F;
            border: 1px solid #2B2B2B;
            border-radius: 14px;
            padding: 12px;
            color: white;
            font-size: 14px;
            font-weight: 500;
        }

        QPushButton:hover {
            background-color: #2A2A2A;
            border: 1px solid #3A3A3A;
        }

        QPushButton:pressed {
            background-color: #151515;
        }

        QTreeWidget {
            background-color: #121212;
            border: none;
            border-radius: 16px;
            padding: 6px;
            outline: none;
        }

        QTreeWidget::item {
            padding: 6px 10px;
            border-radius: 8px;
            margin-top: 1px;
            margin-bottom: 1px;
            min-height: 24px;
        }

        QTreeWidget::item:hover {
            background-color: #2A2A2A;
        }

        QTreeWidget::item:selected {
            background-color: #3A3A3A;
            border: 1px solid #4A4A4A;
        }

        QScrollBar:vertical {
            background: #111111;
            width: 10px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: #333333;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #444444;
        }

        """)

        
    def build_ui(self):
        root = QHBoxLayout(self)

        # ================= LEFT PANEL =================
        left_panel = QFrame()
        left_panel.setMaximumWidth(340)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(14, 14, 14, 14)
        left_layout.setSpacing(6)

        title = QLabel("SYSTEM CONTROL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #84FFFF;
        """)

        from PySide6.QtWidgets import QTreeWidget
        self.preset_list = QTreeWidget()
        self.preset_list.setHeaderHidden(True)
        
        self.cargar_presets_ui()
        self.preset_list.itemDoubleClicked.connect(self.ejecutar_preset_desde_ui)

        left_layout.addWidget(title)
        left_layout.addWidget(self.preset_list)

        self.add_preset_btn = QPushButton("Add Preset")
        self.add_preset_btn.clicked.connect(self.add_preset_contextual)

        self.edit_preset_btn = QPushButton("Edit Preset")
        self.edit_preset_btn.clicked.connect(self.editar_preset)

        self.delete_preset_btn = QPushButton("Delete Preset")
        self.delete_preset_btn.clicked.connect(self.delete_preset)

        left_layout.addWidget(self.add_preset_btn)
        left_layout.addWidget(self.edit_preset_btn)
        left_layout.addWidget(self.delete_preset_btn)

        # ================= CENTER PANEL =================
        center_panel = QFrame()
        center_layout = QVBoxLayout(center_panel)

        self.orb = VoiceOrb()
        center_layout.addWidget(self.orb)

        self.mic_button = QPushButton("🎤")

        self.mic_button.setFixedSize(
            60,
            60
        )

        self.mic_button.clicked.connect(
            self.toggle_mic
        )

        center_layout.addWidget(
            self.mic_button,
            alignment=Qt.AlignRight
        )


       # ================= RIGHT PANEL =================

        right_panel = QFrame()

        right_layout = QVBoxLayout(right_panel)

        # ===== TOP SYSTEM PANEL =====

        top_system_panel = QFrame()

        top_system_layout = QVBoxLayout(
            top_system_panel
        )

        self.monitor = SystemMonitor()

        top_system_layout.addWidget(
            self.monitor
        )

        # ===== BOTTOM PANEL =====

        bottom_panel = QFrame()

        bottom_layout = QVBoxLayout(
            bottom_panel
        )

        placeholder = QLabel("EXTRA PANEL")

        bottom_layout.addWidget(
            placeholder
        )

        # ===== ADD TO RIGHT PANEL =====

        right_layout.addWidget(
            top_system_panel,
            6
        )

        right_layout.addWidget(
            bottom_panel,
            4
        )

        root.addWidget(left_panel, 2)
        root.addWidget(center_panel, 6)
        root.addWidget(right_panel, 2)


    def set_orb_state(self, state):

        self.orb.set_state(state)

        if state == "thinking":

            if not self.thinking_sound.isPlaying():
                self.thinking_sound.play()

        else:
            self.thinking_sound.stop()

            
    def set_orb_voice_level(self, level):
        self.orb.set_voice_level(level)
            

    def cargar_presets_ui(self):
        self.preset_list.clear()

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        presets_path = os.path.join(base_path, "presets.json")

        with open(presets_path, "r", encoding="utf-8") as archivo:
            presets = json.load(archivo)

        for categoria, config in presets.items():

            categoria_item = QTreeWidgetItem([categoria])
            self.preset_list.addTopLevelItem(categoria_item)

            categoria_item.setForeground(
                0,
                Qt.white
            )

            categoria_item.setBackground(
                0,
                QColor("#1F1F1F")
            )

            # 🔥 SOLO cargar hijos reales
            children = config.get("children", {})

            for nombre_hijo in children.keys():
                hijo = QTreeWidgetItem([nombre_hijo])
                categoria_item.addChild(hijo)
                        


    def ejecutar_preset_desde_ui(self, item):
        if item.parent() is None:
            return
        from jarvis_core import procesar_comando, hablar

        nombre_preset = item.text(0)

        print("DOBLE CLICK EN:", nombre_preset)

        respuesta = procesar_comando(nombre_preset)

        print("RESPUESTA:", respuesta)

        hablar(respuesta)
    
    def abrir_modal_preset(self, nombre_original=None, datos=None):
        
        item = self.preset_list.currentItem()

        categoria_actual = None

        from PySide6.QtWidgets import (
            QDialog, QVBoxLayout, QLineEdit,
            QPushButton, QLabel, QFileDialog
        )

        modal = QDialog(self)
        modal.setWindowTitle("Nuevo Preset")
        modal.resize(400, 300)

        layout = QVBoxLayout(modal)

        item = self.preset_list.currentItem()

        categoria_actual = None

        if item:
            if item.parent() is None:
                categoria_actual = item.text(0)
            else:
                categoria_actual = item.parent().text(0)

        nombre_input = QLineEdit()
        nombre_input.setPlaceholderText("Nombre del preset")

        app_input = QLineEdit()
        app_input.setPlaceholderText("Ruta de app (opcional)")
        buscar_app_btn = QPushButton("Buscar Programa")

        url_input = QLineEdit()
        url_input.setPlaceholderText("URL (opcional)")

        audio_input = QLineEdit()
        audio_input.setPlaceholderText("Audio Device (opcional)")

        guardar_btn = QPushButton("Guardar Preset")

      
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        presets_path = os.path.join(base_path, "presets.json")

        with open(presets_path, "r", encoding="utf-8") as archivo:
            presets = json.load(archivo)

   
        def buscar_app():
            ruta_inicial = os.path.expandvars(r"%LOCALAPPDATA%")

            archivo, _ = QFileDialog.getOpenFileName(
                modal,
                "Seleccionar Programa",
                ruta_inicial,
                "Ejecutables (*.exe)"
            )

            if archivo:
                app_input.setText(archivo)

        layout.addWidget(QLabel("Nombre"))
        layout.addWidget(nombre_input)

        layout.addWidget(QLabel("Ruta App"))
        layout.addWidget(app_input)
        layout.addWidget(buscar_app_btn)

        layout.addWidget(QLabel("URL"))
        layout.addWidget(url_input)

        layout.addWidget(QLabel("Audio Device"))
        layout.addWidget(audio_input)

        layout.addWidget(guardar_btn)

       

        if datos:
            nombre_input.setText(nombre_original)
            app_input.setText(
                datos.get("apps", [""])[0] if datos.get("apps") else ""
            )
            url_input.setText(
                datos.get("urls", [""])[0] if datos.get("urls") else ""
            )
            audio_input.setText(
                datos.get("audio_device", "")
            )

            

        def guardar():
            nombre = nombre_input.text().strip()

            if not nombre:
                return

            with open("presets.json", "r", encoding="utf-8") as archivo:
                presets = json.load(archivo)

            nuevo_preset = {
                "apps": [app_input.text()] if app_input.text() else [],
                "urls": [url_input.text()] if url_input.text() else []
            }

            if audio_input.text():
                nuevo_preset["audio_device"] = audio_input.text()

            selected_item = self.preset_list.currentItem()

            # ===== PRESET PADRE =====
            if selected_item is None:
                presets[nombre] = nuevo_preset

            # ===== PRESET HIJO =====
            else:
                if selected_item.parent() is None:
                    padre = selected_item.text(0)
                else:
                    padre = selected_item.parent().text(0)

                if "children" not in presets[padre]:
                    presets[padre]["children"] = {}

                presets[padre]["children"][nombre] = nuevo_preset

            with open("presets.json", "w", encoding="utf-8") as archivo:
                json.dump(
                    presets,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            self.cargar_presets_ui()
            modal.accept()

        guardar_btn.clicked.connect(guardar)
        buscar_app_btn.clicked.connect(buscar_app)

        modal.exec()

    def closeEvent(self, event):
        if hasattr(self, "worker"):
            self.worker.stop()
            self.worker.wait()

        event.accept()

    def editar_preset(self):
        item = self.preset_list.currentItem()

        if not item:
            return

        parent = item.parent()

        with open("presets.json", "r", encoding="utf-8") as archivo:
            presets = json.load(archivo)

        # 🔥 CASO HIJO (lo que tú quieres usar SIEMPRE en Chrome)
        if parent is not None:
            categoria = parent.text(0)
            nombre = item.text(0)

            if categoria in presets and "children" in presets[categoria]:
                if nombre in presets[categoria]["children"]:
                    datos = presets[categoria]["children"][nombre]
                    self.abrir_modal_preset(nombre, datos)
                    return

            print("Error: hijo no encontrado correctamente")
            return

        # 🔥 CASO PADRE (Discord, juegos, etc)
        else:
            nombre = item.text(0)

            if nombre in presets:
                datos = presets[nombre]
                self.abrir_modal_preset(nombre, datos)
                return

            print("Error: padre no encontrado")

    def delete_preset(self):
        item = self.preset_list.currentItem()

        if not item:
            return

        if item.parent() is None:
            categoria = item.text(0)

            with open("presets.json", "r", encoding="utf-8") as archivo:
                presets = json.load(archivo)

            if categoria in presets:
                del presets[categoria]

            with open("presets.json", "w", encoding="utf-8") as archivo:
                json.dump(
                    presets,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            self.cargar_presets_ui()
            return

        nombre = item.text(0)
        categoria = item.parent().text(0)

        with open("presets.json", "r", encoding="utf-8") as archivo:
            presets = json.load(archivo)

        if categoria in presets:
            if "children" in presets[categoria]:
                if nombre in presets[categoria]["children"]:
                    del presets[categoria]["children"][nombre]

        with open("presets.json", "w", encoding="utf-8") as archivo:
            json.dump(presets, archivo, indent=4, ensure_ascii=False)

        self.cargar_presets_ui()

    def toggle_mic(self):

        self.mic_muted = (
            not self.mic_muted
        )

        self.worker.muted = (
            self.mic_muted
        )

        if self.mic_muted:

            self.mic_button.setStyleSheet(
                """
                background-color: #B00020;
                color: white;
                border-radius: 30px;
                """
            )

            print(
                "MICRÓFONO SILENCIADO"
            )

        else:

            self.mic_button.setStyleSheet(
                ""
            )

            print(
                "MICRÓFONO ACTIVADO"
            )

    def add_preset_contextual(self):
        # 🔥 NO PASAMOS categoria manual
        self.abrir_modal_preset()