"""
Artale WC Merch Calculator
Version: v24.11.13@2352
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

import sys, os, time

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
    QFontComboBox,
    QSizePolicy,
    QGroupBox,
    QSpacerItem
)

from PyQt6.QtCore import (
    Qt,
    QUrl,
    QRect,
    QSettings
)

from PyQt6.QtGui import (
    QPixmap,
    QIcon,
    QFont,
    QPalette,
    QColor,
    QDesktopServices,
    QPixmap,
    QGuiApplication,
    QPainter,
    QPen
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

# Function to get the absolute path to the resource
def resource_path(relative_path):
    try:
        # PyInstaller sets _MEIPASS when running from the bundled .exe
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
        return os.path.join(base_path, relative_path)
    except Exception:
        # If not running from the bundle, return the relative path
        return os.path.join(os.path.abspath('.'), relative_path)

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

class DarkLightPalette:
    def __init__(self):
        # Define light and dark palettes with more colors
        self.light = {
            'window': '#FFFFFF',
            'text': '#000000',
            'button': '#E0E0E0',
            'input': '#FFFFFF',
            'profit': '#008000',
            'loss': '#FF0000'
        }
        self.dark = {
            'window': '#1e1e1e',
            'text': '#FFFFFF',
            'button': '#3c3c3c',
            'input': '#3D3D3D',
            'profit': '#00FF00',
            'loss': '#FF4040'
        }

class ClickableLabel(QLabel):
    def __init__(self, text, url, parent=None):
        super().__init__(text, parent)
        self.url = url
        
        # Set the font to be bold and underlined
        font = self.font()
        font.setBold(True)  # Make text bold
        font.setUnderline(True)  # Underline the text correctly
        self.setFont(font)

        # Make the label clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        # Open the URL when clicked
        QDesktopServices.openUrl(QUrl(self.url))

class BoldText(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        # Set the font to be bold and underlined
        font = self.font()
        font.setBold(True)  # Make text bold
        self.setFont(font)

class CustomLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, event):
        # Only call the default paintEvent, don't override placeholder
        super().paintEvent(event)

        # Only draw the placeholder if there is placeholder text and no user input
        if self.placeholderText() and not self.text():
            painter = QPainter(self)
            painter.setPen(QColor(169, 169, 169))  # Fixed color for placeholder text
            painter.setFont(self.font())

            # Calculate the placeholder position manually
            rect = self.rect()
            padding = 10  # Padding to adjust the placement of the placeholder text
            painter.drawText(rect.adjusted(padding, 0, -padding, 0), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.placeholderText())
            painter.end()
            
class ContactDialog(QDialog):
    def __init__(self, parent=None):  # Accept parent window as argument
        super().__init__(parent)
        self.setWindowTitle("Contact Information")

        # Layout for the contact information
        layout = QVBoxLayout(self)

        # GitHub link with clickable label
        github_link = ClickableLabel('<b><font color="orange">GitHub: or1n</font></b>', "https://github.com/or1n")
        github_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(github_link)

        # Artale contact info
        artale_label = QLabel('<b>Orin#MLQhB - Artale US</b>')
        artale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(artale_label)

        # Discord contact info
        discord_label = QLabel('<b>Discord: orin.abc</b>')
        discord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(discord_label)

        # OK button to close the dialog
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set the dialog to resize dynamically based on content
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def showEvent(self, event):
        parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
        dialog_width = self.width()
        dialog_height = self.height()
        dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
        dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
        self.move(dialog_x, dialog_y)

class ChangelogDialog(QDialog):
    def __init__(self, parent=None):  # Accept parent window as argument
        super().__init__(parent)
        self.setWindowTitle("Changelog")
        
        layout = QVBoxLayout(self)
        changelog_text = QLabel("""
                2024.11.14 v2
                    - Fixed issue with undefined 'scale_layout' attribute in Settings dialog.
                    - Added functionality to save AH prices after calculation for persistence across restarts.
                    - Improved settings dialog handling, allowing for more dynamic adjustments.
                    - Fixed light theme text color issue on 'Contact' button, ensuring consistent color with other elements.
		
                2024.11.14
                    - Enhanced UI layout with neatly aligned result headers and item information.
                    - Dynamically sized columns with custom scaling in `update_scale()`.
                    - Improved `calculate()` to display profit results in bold, with strikethrough for negative profits.
                    - Updated styling for button colors and text to better match theme settings.
                    - Modified result display to bold and strikethrough selectively for negative profits.
                    - Reorganized controls for streamlined 'Calculate' section layout and positioning of the changelog button.
        
                2024.11.13                       
                    - Added changelog button and information.
                    - Added a header with creator information (GitHub, Discord, etc.).
        
                2024.11.12
                    - Introduced theme and scale sliders for better customization.
                    - Added font choice option for improved user experience.
        
                2024.11.11
                    - Created initial script with basic item calculation functionality.
                    """)
        layout.addWidget(changelog_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(button_box)
        button_box.accepted.connect(self.accept)

    def showEvent(self, event):
        parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
        dialog_width = self.width()
        dialog_height = self.height()
        dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
        dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
        self.move(dialog_x, dialog_y)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Settings")

        # Initialize settings before UI components
        self.settings = QSettings("MyApp", "Settings")

        # Initialize the color palette
        self.color_palette = DarkLightPalette()  # Create and assign DarkLightPalette instance here

        # Initialize UI components and layout
        self.init_ui()

        # Load saved settings after UI components are set up
        self.load_settings()
        
    def init_ui(self):
        """Set up the user interface elements and layout."""
        fixed_font = QFont()
        fixed_font.setPointSize(12)
        fixed_font.setBold(True)

        layout = QVBoxLayout(self)
        settings_frame = QFrame()
        settings_frame.setFrameShape(QFrame.Shape.StyledPanel)
        settings_layout = QVBoxLayout(settings_frame)

        # Initialize widgets
        self.theme_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_combo = QFontComboBox()
        self.theme_label = QLabel("Theme")
        self.scale_label = QLabel("Scale")

       # Theme layout setup
        self.theme_layout = QVBoxLayout()
        self.theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.theme_layout.addWidget(self.theme_label)
        self.theme_label.setFont(fixed_font)

        # Theme slider setup
        self.theme_slider.setMinimum(0)
        self.theme_slider.setMaximum(100)
        self.theme_slider.setFixedWidth(185)
        self.theme_slider.setFixedHeight(30)
        self.theme_slider.setValue(self.settings.value("theme_value", 100 if darkdetect.isDark() else 0))
        self.theme_slider.valueChanged.connect(self.update_theme)

        # Icon layout for theme slider
        lightbulb_icon = QLabel("💡")
        lightbulb_icon.setStyleSheet("font-size: 20px;")
        sunglasses_icon = QLabel("🕶️")
        sunglasses_icon.setStyleSheet("font-size: 20px;")
        theme_slider_layout = QHBoxLayout()
        theme_slider_layout.addWidget(lightbulb_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        theme_slider_layout.addWidget(self.theme_slider)
        theme_slider_layout.addWidget(sunglasses_icon, alignment=Qt.AlignmentFlag.AlignRight)
        self.theme_layout.addLayout(theme_slider_layout)

        # Scale layout setup
        self.scale_layout = QVBoxLayout()
        self.scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scale_layout.addWidget(self.scale_label)
        self.scale_label.setFont(fixed_font)

        self.scale_slider.setMinimum(60)
        self.scale_slider.setMaximum(200)
        self.scale_slider.setFixedWidth(185)
        self.scale_slider.setFixedHeight(30)
        self.scale_slider.setValue(self.settings.value("scale_value", 100))
        self.scale_slider.valueChanged.connect(self.update_scale)

        # Icon layout for scale slider
        small_icon = QLabel("•")
        small_icon.setStyleSheet("font-size: 20px;")
        big_icon = QLabel("⬤")
        big_icon.setStyleSheet("font-size: 20px;")
        scale_slider_layout = QHBoxLayout()
        scale_slider_layout.addWidget(small_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        scale_slider_layout.addWidget(self.scale_slider)
        scale_slider_layout.addWidget(big_icon, alignment=Qt.AlignmentFlag.AlignRight)
        self.scale_layout.addLayout(scale_slider_layout)

         # Connect sliders to real-time updates
        self.theme_slider.valueChanged.connect(self.update_main_window_scale)
        self.scale_slider.valueChanged.connect(self.update_main_window_scale)

        # Font layout setup
        font_widget = QWidget()
        font_layout = QVBoxLayout(font_widget)

        saved_font = self.settings.value("font_family", "Arial")
        self.font_combo.setCurrentFont(QFont(saved_font))
        self.font_combo.currentFontChanged.connect(self.update_font)
        font_layout.addWidget(self.font_combo)

        # Add layouts to main dialog
        settings_layout.addLayout(self.theme_layout)
        settings_layout.addLayout(self.scale_layout)
        settings_layout.addWidget(font_widget)
        layout.addWidget(settings_frame)

        # Initial application of the theme and scale based on slider values
        self.update_theme(self.theme_slider.value())
        self.update_scale(self.scale_slider.value())

        # OK button to close the dialog
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.save_and_close)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Disable resizing of dialog by setting a fixed size
        self.setFixedSize(300, 300)

    def update_main_window_scale(self):

        theme_value = self.theme_slider.value()
        self.parent().apply_dynamic_theme(theme_value)

    def update_main_window_scale(self):
        # Call this function to apply scaling dynamically
        scale_value = self.scale_slider.value()
        
        # Call the parent method to apply dynamic scaling
        self.parent().apply_dynamic_scaling(scale_value)

    def load_settings(self):
        """Load settings from QSettings."""
        theme_value = self.settings.value("theme_value", 100 if darkdetect.isDark() else 0)
        scale_value = self.settings.value("scale_value", 100)
        font_family = self.settings.value("font_family", "Arial")

        # Set the loaded settings to the UI components
        self.theme_slider.setValue(theme_value)
        self.scale_slider.setValue(scale_value)
        self.font_combo.setCurrentFont(QFont(font_family))

    def apply_settings(self):
        """Apply settings and then close the dialog."""
        self.settings.setValue("theme_value", self.theme_slider.value())
        self.settings.setValue("scale_value", self.scale_slider.value())
        self.settings.setValue("font_family", self.font_combo.currentFont().family())

        self.accept()

    def update_font(self, font):
        """Update the font when changed."""
        self.settings.setValue("font_family", font.family())
        QApplication.instance().setFont(font)  # Apply globally if necessary

    def update_theme(self, value):
        """Update the theme based on the slider value."""
        factor = value / 100
        current = {}

        for key in self.color_palette.light:
            light_color = QColor(self.color_palette.light[key])
            dark_color = QColor(self.color_palette.dark[key])

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

        QApplication.instance().setPalette(palette)
        self.setPalette(palette)

    def update_input_palettes(self):
        # Get the current palette from the theme slider or settings
        palette = QApplication.instance().palette()  # The global app palette
        text_color = palette.color(QPalette.ColorRole.Text)  # Get the current text color (theme-based)

        # Set the text color for all inputs (including placeholders)
        self.rate_input.setPalette(palette)
        self.profit_input.setPalette(palette)
    
        for price_input in self.price_inputs.values():
            price_input.setPalette(palette)
        
    def update_scale(self, value):
        """Update the scale based on the slider value."""
        self.scale_factor = value / 100.0
        font = QApplication.font()
        font.setPointSize(int(10 * self.scale_factor))
        QApplication.setFont(font)

        new_width = int(self.width() * self.scale_factor)
        new_height = int(self.height() * self.scale_factor)
        self.resize(new_width, new_height)
    
    def closeEvent(self, event):
        """Override closeEvent to simulate Ok button press when the window is closed."""
        self.save_and_close()

        # Notify main window about scale change (if needed)
        if self.parent():
            self.parent().update_main_window_scale(self.scale_slider.value())

        event.accept()

    def save_and_close(self):
        """Save settings and close the dialog."""
        self.apply_settings()  # Save settings before closing
        
        # Notify main window about scale change (if needed)
        if self.parent():
            self.parent().update_main_window_scale(self.scale_slider.value())
        
        self.accept()  # Close the dialog

    def showEvent(self, event):
        parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
        dialog_width = self.width()
        dialog_height = self.height()
        dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
        dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
        self.move(dialog_x, dialog_y)
    
class MerchantCalculator(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Run the settings dialog invisibly on startup
        self.run_settings_dialog()
        self.settings_dialog = SettingsDialog(self)  # Pass self as the parent

        self.settings = QSettings("MyCompany", "ArtaleWCMerchCalc")  # Define the organization and application name for storing settings

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
        self.scale_factor = 1.0
        self.init_ui()

    def load_settings(self):
        """Load saved settings for inputs and AH prices."""
        # Load rate and profit
        saved_rate = self.settings.value("rate_input", 2400)  # Default value if not saved
        saved_profit = self.settings.value("profit_input", 10.0)  # Default value if not saved
        
        self.rate_input.setText(str(saved_rate))
        self.profit_input.setText(str(saved_profit))

        # Load AH prices for each item
        for item in self.items:
            saved_price = self.settings.value(f"ah_price_{item.name}", 0)  # Default to 0 if not saved
            self.price_inputs[item.name].setText(str(saved_price))

    def save_settings(self):
        """Save current settings for inputs and AH prices."""
        # Save rate and profit
        self.settings.setValue("rate_input", self.rate_input.text())
        self.settings.setValue("profit_input", self.profit_input.text())

        # Save AH prices for each item
        for item in self.items:
            price_input = self.price_inputs.get(item.name)
            if price_input:
                self.settings.setValue(f"ah_price_{item.name}", price_input.text())
                 
    def update_results(self, new_results):
        """This function will be called to update the results section and resize the window."""
    
        # Clear existing results
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add new results to the results layout
        for result in new_results:
            result_label = QLabel(result)
            self.results_layout.addWidget(result_label)

        # Trigger the window to adjust size based on the updated results
        self.adjustSize()

    def run_settings_dialog(self):
        """Run the settings dialog invisibly, apply settings, and close it."""
        settings_dialog = SettingsDialog(self)
        settings_dialog.hide()  # Hide the dialog (it won't be shown to the user)
        settings_dialog.apply_settings()  # Apply settings without showing the dialog

    def apply_dynamic_scaling(self, scale_value):
        """Update main window scale dynamically based on scale slider."""
        scale_factor = scale_value / 100.0
    
        # Update font size
        font = QApplication.font()
        font.setPointSize(int(10 * scale_factor))  # Dynamically adjust font size
        QApplication.setFont(font)
    
        # Resize window based on scale factor
        current_width = self.width()
        current_height = self.height()

        # Calculate the new size based on the scale factor
        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)
    
        # Resize the window
        self.resize(new_width, new_height)
    
        # Update UI (force refresh to apply the new sizes properly)
        self.update()  # Refresh the window layout to reflect changes
        self.adjustSize()  # Recalculate size based on content

    def apply_dynamic_theme(self, theme_value):
        # Implement theme logic here
        if theme_value == 0:
            # Apply light theme
            self.setStyleSheet("background-color: white; color: black;")
        elif theme_value == 1:
            # Apply dark theme
            self.setStyleSheet("background-color: black; color: white;")
        else:
            # Apply a default theme or reset
            self.setStyleSheet("")

    def init_ui(self):
        # Center the window on the screen
        screen = QApplication.primaryScreen()  # Get the primary screen
        screen_geometry = screen.availableGeometry()  # Get available geometry of the screen
        screen_center = screen_geometry.center()  # Get the center point of the screen
        window_geometry = self.frameGeometry()  # Get the geometry of the window
        window_geometry.moveCenter(screen_center)  # Move the window center to the screen center
        self.move(window_geometry.topLeft())  # Move the top-left corner of the window to the calculated position
    
        # Set the size policy for MerchantCalculator to be dynamically resizable
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        version, last_modified_time, timestamp = self.get_version_from_file_timestamp()
        print(f"Version: {version}, Last Modified: {last_modified_time}, Timestamp: {timestamp}")

        self.setWindowTitle(f'Artale WC Merch Calc {version} - made by Orin#MLQhB')
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Header with links
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)

        # Load avatar image from the "images" folder using the resource_path
        avatar_image = QPixmap(resource_path("images/avatar.png"))
        avatar_label = QLabel()
        avatar_label.setPixmap(avatar_image)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Make avatar label expand horizontally
        header_layout.addWidget(avatar_label)

        # Title with version (bold and bigger)
        title_label = QLabel(f'<b><font size="4">Artale WC Merch Calc</font> <font size="2">{version}</font></b>')
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow title to expand horizontally
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

        # "Orin#MLQhB" with orange color and bold
        github_link = ClickableLabel('<b>Orin#MLQhB</b>', "https://github.com/or1n")
        github_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github_link.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow link to expand horizontally
        header_layout.addWidget(github_link)
        
        layout.addWidget(header_widget)

        # Controls area with frame for Rate, Desired Profit, AH Prices, Calculate
        controls_frame = QFrame()
        controls_frame.setFrameShape(QFrame.Shape.StyledPanel)
        controls_layout = QVBoxLayout(controls_frame)

        # Section Header for Controls
        controls_header = BoldText("Controls")
        controls_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(controls_header)

        # Rate
        rate_widget = QWidget()
        rate_layout = QHBoxLayout(rate_widget)
        rate_layout.addWidget(QLabel("Rate 1:"))

        self.rate_input = CustomLineEdit()
        self.rate_input.setPlaceholderText("2400")

        rate_layout.addWidget(self.rate_input)
        
        # Profit
        profit_widget = QWidget()
        profit_layout = QHBoxLayout(profit_widget)
        profit_layout.addWidget(QLabel("Desired Profit %"))
        self.profit_input = CustomLineEdit()
        self.profit_input.setPlaceholderText("10")

        profit_layout.addWidget(self.profit_input)

        # Combine both rate and profit widgets into one row
        combined_layout = QHBoxLayout()  # One layout for both
        combined_layout.addWidget(rate_widget)
        combined_layout.addWidget(profit_widget)

        # Add the combined layout to the controls layout
        controls_layout.addLayout(combined_layout)

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
            
            # Price input (for each item)
            price_input = CustomLineEdit()
            price_input.setPlaceholderText("AH Price")

            self.price_inputs[item.name] = price_input
            item_layout.addWidget(price_input)
            
            self.input_layout.addWidget(item_widget, row, col)
        
        controls_layout.addWidget(input_widget)      

        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate)
        controls_layout.addWidget(self.calc_button)
        
        layout.addWidget(controls_frame)
        
        #Results area
        results_frame = QFrame()
        results_frame.setFrameShape(QFrame.Shape.StyledPanel)
        results_layout = QVBoxLayout(results_frame)

        # Section Header for Results
        results_header = BoldText("Results")
        results_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        results_layout.addWidget(results_header)
        
        # Directly use a QWidget for results content (no scroll area)
        self.results_content = QWidget()
        self.results_layout = QVBoxLayout(self.results_content)
        results_layout.addWidget(self.results_content)

        # Add results frame to the main layout
        layout.addWidget(results_frame)

        button_layout = QHBoxLayout()
        
        "CONTACTS BUTTON"
        contact_button = QPushButton("Contact")
        contact_button.clicked.connect(self.show_contact)
        button_layout.addWidget(contact_button, alignment=Qt.AlignmentFlag.AlignLeft)

        "SETTINGS BUTTON"
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.show_settings)
        button_layout.addWidget(settings_button, alignment=Qt.AlignmentFlag.AlignCenter)

        "CHANGELOG BUTTON"
        changelog_button = QPushButton("Changelog")
        changelog_button.clicked.connect(self.show_changelog)
        button_layout.addWidget(changelog_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Ensure the results section expands/shrinks as needed
        layout.setStretch(0, 0)  # Header (fixed)
        layout.setStretch(1, 0)  # Controls (fixed)
        layout.setStretch(2, 1)  # Results (expandable)
        layout.setStretch(3, 0)  # Button layout (fixed)
    
        # Resize the window to fit all content
        self.adjustSize()

        # Set a minimum size (optional)
        min_width = self.minimumWidth()
        min_height = self.minimumHeight()
        self.setMinimumSize(min_width, min_height)

        self.load_settings()

    def get_version_from_file_timestamp(self):
        script_name = "Artale WC Merch Calc.pyw"  # Ensure the correct extension is used
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        try:
            last_modified_time = os.path.getmtime(script_path)
            timestamp = time.localtime(last_modified_time)
            version = time.strftime("v%Y.%m.%d", timestamp)
            return version, last_modified_time, timestamp
        except Exception as e:
            print(f"Error: {e}")
            return None, None, None

    def update_main_window_scale(self, scale_value):
        """Update main window scale dynamically based on scale slider."""
        scale_factor = scale_value / 100.0
    
        # Update font size
        font = QApplication.font()
        font.setPointSize(int(10 * scale_factor))  # Dynamically adjust font size
        QApplication.setFont(font)
    
        # Resize window based on scale factor
        current_width = self.width()
        current_height = self.height()

        # Calculate the new size based on the scale factor
        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)
    
        # Resize the window
        self.resize(new_width, new_height)
    
        # Update UI (force refresh to apply the new sizes properly)
        self.update()  # Refresh the window layout to reflect changes
        self.adjustSize()  # Recalculate size based on content
 
    def calculate(self):
        # Clear any existing result widgets
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)
        
        # Handle rate and profit input
        try:
            wc_rate = int(self.rate_input.text().replace(",", "") or "2400")  # Remove commas if present
            desired_profit = float(self.profit_input.text().replace(",", "") or "10")  # Remove commas if present
        except ValueError:
            return
        
        # Save settings after calculation
        self.save_settings()
        
        results = []
        for item in self.items:
            try:
                ah_price_text = self.price_inputs[item.name].text().replace(",", "")  # Remove commas from input
                ah_price = int(ah_price_text or "0")
                if ah_price > 0:
                    result = ItemResult(item, ah_price, wc_rate)
                    results.append(result)
            except ValueError:
                continue
        
        results.sort(key=lambda x: x.profit_percent, reverse=True)

        # Update the font family
        font_family = QApplication.instance().property("font_family") or "Default Font"
        
        headers = ["Item", "AH Price (-1💰)", "AH Fee", "Net", "Profit %", "Profit Mesos", "Max Rate"]
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        for header in headers:
            label = QLabel(header)
            label.setFont(QFont(font_family, weight=QFont.Weight.Bold))  # Apply saved font and bold weight
            header_layout.addWidget(label)
        self.results_layout.addWidget(header_widget)
        
        # Create result rows
        for result in results:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)

            # Set a fixed width for each column except the "Item" column (which can stretch)
            column_width = 120  # Adjust as needed to fit content
            
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
            # Add ❌ for items with negative profit, but only to the item name (first column)
            for i, text in enumerate(data):
                if result.profit_percent < 0 and i == 0:  # Only modify the first column (item name)
                    data[i] = f"❌ {data[i]}"  # Add "❌" to the beginning of the item name

                label = QLabel(data[i])  # Use the (possibly modified) text
                label.setFont(QFont(font_family))  # Apply saved font

                # Create a QFont object and adjust font size dynamically
                font = label.font()  # Get current font

                # Set fixed widths for all columns except the name column
                if i == 0:  # The "Item" column can stretch
                    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                else:  # Other columns should have fixed width
                    label.setFixedWidth(column_width)

                # Set bold text and/or strikethrough if needed (e.g., for negative profit)
                if result.profit_percent < 0:
                    if i != 6:  # Skip strikethrough for the max rate (index 6 in your case)
                        font.setBold(False)  # Make the font non-bold for negative profits
                        font.setStrikeOut(True)  # Apply strikethrough
                    else:  # Make max rate bold without strikethrough
                        font.setBold(True)
                else:
                    font.setBold(False)  # Non-bold text for positive profits
                    font.setStrikeOut(False)  # Remove strikethrough for non-negative profits

                # Apply the adjusted font to the label
                label.setFont(font)

                # Apply sizePolicy to allow horizontal stretching
                label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

                # Add the label to the layout
                row_layout.addWidget(label)

            # After processing all labels, add the row_widget to the results_layout
            self.results_layout.addWidget(row_widget)

        # Automatically resize the whole window to fit the content
        self.adjustSize()
    
        # Ensure the window does not shrink too small
        min_width = self.minimumWidth()  # Get the current minimum width
        min_height = self.minimumHeight()  # Get the current minimum height
        self.setMinimumSize(min_width, min_height)  # Ensure the window size is not smaller than the minimum

    def show_contact(self):
        contact_dialog = ContactDialog(self) # Pass self as the parent
        contact_dialog.exec() # Show the dialog modally

    def show_settings(self):
        settings_dialog = SettingsDialog(self)  # Pass self as the parent
        settings_dialog.exec()  # Show the dialog modally

    def show_changelog(self):
        changelog_dialog = ChangelogDialog(self)  # Pass self as parent
        changelog_dialog.exec() # Show the dialog modally

def main():
    # Ensure QApplication is created first
    app = QApplication(sys.argv)
    
    # Initialize the main window
    calculator = MerchantCalculator()
    calculator.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()