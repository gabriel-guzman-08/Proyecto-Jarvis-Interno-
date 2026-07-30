from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QRadialGradient,
    QPainterPath
)
from PySide6.QtCore import QTimer, Qt
import math


class VoiceOrb(QWidget):

    def __init__(self):

        super().__init__()

        self.pulse = 0

        self.state = "idle"
        self.voice_level = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

        self.setMinimumSize(650, 650)

    def animate(self):

        self.pulse += 0.012

        self.update()

    def set_state(self, state):

        self.state = state

    def set_voice_level(self, level):

        self.voice_level = max(0, min(level, 100))

    def draw_soft_layer(
        self,
        painter,
        cx,
        cy,
        radius,
        strength,
        opacity,
        thickness,
        speed,
        density,
        phase
    ):

        path = QPainterPath()

        for i in range(density + 1):

            angle = (
                i / density
            ) * math.pi * 2

            distortion = 0

            distortion += (
                math.sin(
                    angle * 2.5 +
                    self.pulse * speed +
                    phase
                ) * strength
            )

            distortion += (
                math.cos(
                    angle * 4.0 -
                    self.pulse * speed * 0.6
                ) * (strength * 0.6)
            )

            distortion += (
                math.sin(
                    angle * 7.0 +
                    self.pulse * speed * 0.3
                ) * (strength * 0.25)
            )

            dynamic_radius = (
                radius +
                distortion
            )

            x = (
                cx +
                math.cos(angle) *
                dynamic_radius
            )

            y = (
                cy +
                math.sin(angle) *
                dynamic_radius
            )

            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)

        pen = QPen(
            QColor(
                255,
                255,
                255,
                opacity
            ),
            thickness
        )

        painter.setPen(pen)

        painter.drawPath(path)

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.setPen(Qt.NoPen)

        cx = self.width() / 2
        cy = self.height() / 2

        # FLOATING MOTION

        cx += (
            math.sin(self.pulse * 0.4)
            * 8
        )

        cy += (
            math.cos(self.pulse * 0.6)
            * 6
        )

        # ORB SIZE

        base_radius = 145

        if self.state == "listening":

            base_radius += 5

        elif self.state == "thinking":

            base_radius += (
                math.sin(
                    self.pulse * 2
                ) * 5
            )

        elif self.state == "speaking":

            base_radius += (
                self.voice_level * 0.08
            )

        # VERY SOFT OUTER ATMOSPHERE

        atmosphere = QRadialGradient(
            cx,
            cy,
            320
        )

        atmosphere.setColorAt(
            0.0,
            QColor(
                255,
                255,
                255,
                4
            )
        )

        atmosphere.setColorAt(
            0.5,
            QColor(
                180,
                180,
                180,
                3
            )
        )

        atmosphere.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.setBrush(atmosphere)

        painter.drawEllipse(
            int(cx - 320),
            int(cy - 320),
            640,
            640
        )

        # DARK INTERIOR

        core = QRadialGradient(
            cx,
            cy,
            170
        )

        core.setColorAt(
            0.0,
            QColor(
                5,
                5,
                5,
                255
            )
        )

        core.setColorAt(
            0.6,
            QColor(
                12,
                12,
                12,
                240
            )
        )

        core.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.setBrush(core)

        painter.drawEllipse(
            int(cx - 170),
            int(cy - 170),
            340,
            340
        )

        # MAIN FLUID LAYERS

        layer_configs = [

            (0,   13, 42, 1.4, 0.8),
            (8,   12, 38, 1.2, -0.9),
            (16,  11, 34, 1.1, 1.2),
            (24,  10, 30, 1.0, -1.4),
            (32,   9, 28, 0.9, 1.6),
            (40,   8, 24, 0.8, -1.8),
            (48,   7, 20, 0.7, 2.0),
            (56,   6, 18, 0.6, -2.2)

        ]

        for (
            offset,
            strength,
            opacity,
            thickness,
            speed
        ) in layer_configs:

            self.draw_soft_layer(
                painter,
                cx,
                cy,
                base_radius + offset,
                strength,
                opacity,
                thickness,
                speed,
                520,
                offset * 0.2
            )

        # INNER DEPTH LAYERS

        for i in range(18):

            self.draw_soft_layer(
                painter,
                cx,
                cy,
                base_radius - 10 - (i * 3),
                3.5,
                5,
                0.45,
                0.5 + (i * 0.04),
                280,
                i
            )

        # SOFT EDGE GLOW

        edge_glow = QRadialGradient(
            cx,
            cy,
            220
        )

        edge_glow.setColorAt(
            0.0,
            QColor(
                255,
                255,
                255,
                0
            )
        )

        edge_glow.setColorAt(
            0.7,
            QColor(
                255,
                255,
                255,
                6
            )
        )

        edge_glow.setColorAt(
            1.0,
            QColor(
                255,
                255,
                255,
                0
            )
        )

        painter.setBrush(edge_glow)

        painter.drawEllipse(
            int(cx - 220),
            int(cy - 220),
            440,
            440
        )