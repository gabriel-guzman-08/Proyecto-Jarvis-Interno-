from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel
)

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont

import psutil
import requests
import subprocess


class SystemMonitor(QFrame):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border: 1px solid #222;
                border-radius: 18px;
            }

            QLabel {
                color: white;
                border: none;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)

        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)

        info_font = QFont()
        info_font.setPointSize(9)

        self.title = QLabel("SYSTEM")
        self.title.setFont(title_font)

        self.cpu_label = QLabel("CPU")
        self.cpu_label.setFont(info_font)

        self.gpu_label = QLabel("GPU")
        self.gpu_label.setFont(info_font)

        self.ram_label = QLabel("RAM")
        self.ram_label.setFont(info_font)

        self.disk_label = QLabel("DISKS")
        self.disk_label.setFont(info_font)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.gpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)

        self.layout.addStretch()

        self.setLayout(self.layout)

        # self.disk_info_cache = self.obtener_info_discos()

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_info)
        self.timer.start(3000)

        self.actualizar_info()

    def obtener_tipo_disco(self, letra):

        try:

            comando = f'''
            $partition = Get-Partition -DriveLetter {letra}
            $disk = $partition | Get-Disk
            $physical = Get-PhysicalDisk | Where-Object {{
                $_.DeviceId -eq $disk.Number
            }}

            $physical.MediaType
            '''

            resultado = subprocess.check_output(
                ["powershell", "-Command", comando],
                text=True
            ).strip()

            if "SSD" in resultado:
                return "SSD"

            if "HDD" in resultado:
                return "HDD"

            return "DESCONOCIDO"

        except:
            return "DESCONOCIDO"

    def obtener_info_discos(self):

        texto = ""

        try:

            partitions = psutil.disk_partitions()

            discos_vistos = set()

            for partition in partitions:

                try:

                    usage = psutil.disk_usage(
                        partition.mountpoint
                    )

                    free = usage.free / (1024 ** 3)

                    letra = partition.device.replace("\\", "")

                    if letra in discos_vistos:
                        continue

                    discos_vistos.add(letra)

                    tipo = self.obtener_tipo_disco(
                        letra[0]
                    )

                    texto += (
                        f"{letra}\n"
                        f"{tipo}\n"
                        f"{free:.0f}GB libres\n\n"
                    )

                except:
                    pass

        except:
            pass

        return texto


    def obtener_temperaturas(self):

        cpu_temp = "N/A"
        gpu_temp = "N/A"

        try:

            data = requests.get(
                "http://localhost:8085/data.json",
                timeout=0.3
            ).json()

            def recorrer(nodos):

                nonlocal cpu_temp
                nonlocal gpu_temp

                for nodo in nodos:

                    texto = nodo.get("Text", "")
                    valor = nodo.get("Value", "")

                    if "CPU CCD #1" in texto:
                        cpu_temp = valor

                    if "GPU Core" in texto:
                        gpu_temp = valor

                    recorrer(
                        nodo.get("Children", [])
                    )

            recorrer(data.get("Children", []))

        except:
            pass

        return cpu_temp, gpu_temp


    def actualizar_info(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        cpu_temp, gpu_temp = (
            self.obtener_temperaturas()
        )

        self.cpu_label.setText(
            f"CPU\n"
            f"{cpu}% | {cpu_temp}"
        )

        self.gpu_label.setText(
            f"GPU\n"
            f"{gpu_temp}"
        )

        self.ram_label.setText(
            f"RAM\n{ram}%"
        )

        self.disk_label.setText(
            "Disks loading..."
        )