"""
Artale WC Merch Calculator
Version: v5
Author: Orin

GitHub: https://github.com/or1n
MapleStory Worlds: Orin#MLQhB
Server: Artale - US
Discord: orin.abc

Description:
This script provides an interface to calculate profitable trading rates for various 
items in MapleStory, specifically for the Artale server on the Maple Worlds platform.
It calculates the expected net profit after factoring in the auction house fees and 
displays the results in a sorted, easy-to-read format. 
"""

import sys

# PyQt6 Imports
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QScrollArea,
    QSlider,
    QFontComboBox
)

from PyQt6.QtCore import (
    Qt,
    QUrl
)

from PyQt6.QtGui import (
    QPixmap,
    QIcon,
    QFont,
    QPalette,
    QColor,
    QDesktopServices,
    QPixmap
)

# For network requests and downloading images
from PyQt6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest
)
# Other standard library imports
from dataclasses import dataclass
from typing import List

# For theme detection
import darkdetect


@dataclass
class Item:
    name: str
    wc_cost: float
    pack_size: int = 1
    
    @property
    def unit_wc_cost(self) -> float:
        return self.wc_cost / self.pack_size

class ItemResult:
    def __init__(self, item: Item, ah_price: int, wc_rate: int):
        self.item = item
        self.ah_price = ah_price
        self.wc_rate = wc_rate
        self.sale_price = ah_price - 1
        self.ah_fee = int(self.sale_price * 0.05)
        self.net = int(self.sale_price * 0.95)
        self.cost = int(item.unit_wc_cost * wc_rate)
        self.profit_mesos = self.net - self.cost
        self.profit_percent = (self.profit_mesos / self.cost * 100) if self.cost > 0 else 0
        
    def calculate_max_rate(self, desired_profit_percent: float) -> int:
        if self.ah_price <= 1:
            return 0
        net = (self.ah_price - 1) * 0.95
        max_cost = net / (1 + desired_profit_percent / 100)
        return int(max_cost / self.item.unit_wc_cost)

class ClickableLabel(QLabel):
    def __init__(self, text, url, parent=None):
        super().__init__(text, parent)
        self.url = url
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("color: #0078D7; text-decoration: underline;")

    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.url))

class DarkLightPalette:
    def __init__(self):
        self.light = {
            'window': '#FFFFFF',
            'text': '#000000',
            'button': '#E0E0E0',
            'input': '#FFFFFF',
            'profit': '#008000',
            'loss': '#FF0000'
        }
        self.dark = {
            'window': '#2D2D2D',
            'text': '#FFFFFF',
            'button': '#404040',
            'input': '#3D3D3D',
            'profit': '#00FF00',
            'loss': '#FF4040'
        }

class ChangelogDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Changelog")
        self.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(self)
        changelog_text = QLabel("""        
        Changelog:
                                
        Version 5
        - Moved Calculate button below the AH prices section.
        - Added a border around Rate, Desired Profit, AH Prices, and Calculate button for visual clarity.
                                        
        Version 4
        - Added changelog button and information.
        
        Version 3:
        - Added a header with creator information (GitHub, Discord, etc.).
        
        Version 2:
        - Introduced theme and scale sliders for better customization.
        - Added font choice option for improved user experience.
        
        Version 1:
        - Created initial script with basic item calculation functionality.
        """)
        layout.addWidget(changelog_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(button_box)
        button_box.accepted.connect(self.accept)

class MerchantCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.items = [
            Item("Defense Charm", 450, 11),
            Item("VIP Teleport Rock", 400, 11),
            Item("SP Reset", 600, 2),
            Item("AP Reset", 800, 2),
            Item("Megaphone", 1200, 11),
            Item("Super Megaphone", 1400, 11),
            Item("Snowflakes", 300, 11),
            Item("Sprinkled Flowers", 300, 11),
            Item("Blue Book Bag", 250),
            Item("Pet", 1600)
        ]
        self.palette = DarkLightPalette()
        self.scale_factor = 1.0
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Artale WC Merch Calc v5 - made by Orin#MLQhB')
        self.setMinimumSize(400, 400)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Header with links
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)

        # Title with version (bold and bigger)
        title_label = QLabel('<b><font size="5">Artale WC Merch Calc v5</font></b>')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

        # "made by or1n" with orange color and bold
        github_link = ClickableLabel('<b><font color="orange">made by or1n</font></b>', "https://github.com/or1n")
        github_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(github_link)
        
        # Orin#MLQhB - Artale US (bold)
        artale_label = QLabel('<b>Orin#MLQhB - Artale US</b>')
        artale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(artale_label)
        
        # orin.abc (bold)
        discord_label = QLabel('<b>orin.abc</b>')
        discord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(discord_label)
        
        layout.addWidget(header_widget)

        # Controls area with frame for Rate, Desired Profit, AH Prices, Calculate
        controls_frame = QFrame()
        controls_frame.setFrameShape(QFrame.Shape.StyledPanel)
        controls_layout = QVBoxLayout(controls_frame)
        
        # Rate input
        rate_widget = QWidget()
        rate_layout = QHBoxLayout(rate_widget)
        rate_layout.addWidget(QLabel("Rate 1:"))
        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("2400")
        rate_layout.addWidget(self.rate_input)
        controls_layout.addWidget(rate_widget)
        
        # Profit threshold input
        profit_widget = QWidget()
        profit_layout = QHBoxLayout(profit_widget)
        profit_layout.addWidget(QLabel("Desired Profit %"))
        self.profit_input = QLineEdit()
        self.profit_input.setPlaceholderText("10")
        profit_layout.addWidget(self.profit_input)
        controls_layout.addWidget(profit_widget)

         # Input grid for AH prices
        input_widget = QWidget()
        self.input_layout = QGridLayout(input_widget)
        self.price_inputs = {}
        
        for i, item in enumerate(self.items):
            col = i % 5
            row = i // 5
            
            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            
            label = QLabel(item.name)
            item_layout.addWidget(label)
            
            price_input = QLineEdit()
            price_input.setPlaceholderText("AH Price")
            self.price_inputs[item.name] = price_input
            item_layout.addWidget(price_input)
            
            self.input_layout.addWidget(item_widget, row, col)
        
        controls_layout.addWidget(input_widget)      

        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate)
        controls_layout.addWidget(self.calc_button)
        
        # Results area
        self.results_widget = QScrollArea()
        self.results_widget.setWidgetResizable(True)
        self.results_content = QWidget()
        self.results_layout = QVBoxLayout(self.results_content)
        self.results_widget.setWidget(self.results_content)
        controls_layout.addWidget(self.results_widget)

        layout.addWidget(controls_frame)

        # Settings area
        settings_frame = QFrame()
        settings_frame.setFrameShape(QFrame.Shape.StyledPanel)
        settings_layout = QVBoxLayout(settings_frame)

        # Theme, Scale, and Font controls in one row
        sliders_font_layout = QHBoxLayout()
        self.theme_slider = QSlider(Qt.Orientation.Horizontal)
        self.theme_slider.setMinimum(0)
        self.theme_slider.setMaximum(100)
        self.theme_slider.setValue(100 if darkdetect.isDark() else 100)
        self.theme_slider.valueChanged.connect(self.update_theme)

        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setMinimum(50)
        self.scale_slider.setMaximum(200)
        self.scale_slider.setValue(100)  # Default font scale
        self.scale_slider.valueChanged.connect(self.update_scale)

        sliders_font_layout.addWidget(QLabel("Theme"))
        sliders_font_layout.addWidget(self.theme_slider)
        sliders_font_layout.addWidget(QLabel("Scale"))
        sliders_font_layout.addWidget(self.scale_slider)

        # Font selector
        font_widget = QWidget()
        font_layout = QHBoxLayout(font_widget)
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.update_font)
        font_layout.addWidget(self.font_combo, alignment=Qt.AlignmentFlag.AlignLeft)

        sliders_font_layout.addWidget(self.font_combo)

        settings_layout.addLayout(sliders_font_layout)
        settings_layout.addWidget(font_widget)

        layout.addWidget(settings_frame)

        # Changelog button
        changelog_button = QPushButton("Changelog")
        changelog_button.clicked.connect(self.show_changelog)
        layout.addWidget(changelog_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Initial theme
        self.update_theme(self.theme_slider.value())

    def update_scale(self, value):
        self.scale_factor = value / 100.0
        font = QApplication.font()
        font.setPointSize(int(10 * self.scale_factor))
        QApplication.setFont(font)
        
    def update_theme(self, value):
        factor = value / 100
        current = {}
        
        for key in self.palette.light:
            light_color = QColor(self.palette.light[key])
            dark_color = QColor(self.palette.dark[key])
            
            r = int(light_color.red() * (1 - factor) + dark_color.red() * factor)
            g = int(light_color.green() * (1 - factor) + dark_color.green() * factor)
            b = int(light_color.blue() * (1 - factor) + dark_color.blue() * factor)
            
            current[key] = QColor(r, g, b)
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, current['window'])
        palette.setColor(QPalette.ColorRole.WindowText, current['text'])
        palette.setColor(QPalette.ColorRole.Button, current['button'])
        palette.setColor(QPalette.ColorRole.Base, current['input'])
        palette.setColor(QPalette.ColorRole.Text, current['text'])
        
        self.setPalette(palette)
        QApplication.instance().setPalette(palette)
        
    def update_font(self, font):
        font.setPointSize(int(10 * self.scale_factor))
        QApplication.instance().setFont(font)
    
    def calculate(self):
        for i in reversed(range(self.results_layout.count())): 
            self.results_layout.itemAt(i).widget().setParent(None)
        
        try:
            wc_rate = int(self.rate_input.text() or "2400")
            desired_profit = float(self.profit_input.text() or "10")
        except ValueError:
            return
        
        results = []
        for item in self.items:
            try:
                ah_price = int(self.price_inputs[item.name].text() or "0")
                if ah_price > 0:
                    result = ItemResult(item, ah_price, wc_rate)
                    results.append(result)
            except ValueError:
                continue
        
        results.sort(key=lambda x: x.profit_percent, reverse=True)
        
        headers = ["Item", "AH Price (-1💰)", "AH Fee", "Net", "Profit %", "Profit Mesos", "Max Rate"]
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        for header in headers:
            label = QLabel(header)
            label.setFont(QFont(self.font_combo.currentFont().family(), weight=QFont.Weight.Bold))
            header_layout.addWidget(label)
        self.results_layout.addWidget(header_widget)
        
        for result in results:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            
            # Prepare profit mesos text with 💰 only for positive profit
            profit_mesos_text = (
                f"{result.profit_mesos:,}💰" if result.profit_mesos > 0
                else f"{result.profit_mesos:,}"
            )
            
            data = [
                result.item.name,
                f"{result.sale_price:,}",
                f"{result.ah_fee:,}",
                f"{result.net:,}",
                f"{result.profit_percent:.1f}%",
                profit_mesos_text,
                f"1:{result.calculate_max_rate(desired_profit):,}"
            ]
            
            # Add ❌ for items with negative profit
            if result.profit_percent < 0:
                data[0] = f"❌ {data[0]}"
            
            for i, text in enumerate(data):
                label = QLabel(text)
                if result.profit_percent < 0:
                    if i != 6:  # Don't strikethrough max rate
                        label.setStyleSheet("text-decoration: line-through;")
                    else:  # Make max rate bold for negative profit items
                        label.setStyleSheet("font-weight: bold;")
                row_layout.addWidget(label)
            
            self.results_layout.addWidget(row_widget)

    def show_changelog(self):
        changelog_dialog = ChangelogDialog()
        changelog_dialog.exec()
        
def main():
    app = QApplication(sys.argv)
    calculator = MerchantCalculator()
    calculator.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()