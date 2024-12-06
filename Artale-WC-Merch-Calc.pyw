# 📝 Code Description
DESCRIPTION = [
    "A comprehensive calculator tool for MapleStory Artale server merchants."
    "Analyze WC, exchange rates, calculate profit margins, track price history and optimize trading decisions."
]

# 🔑 Key Features
FEATURES = [
    "💰 Real-time profit calculation and margin analysis",
    "📊 Auction house fee consideration (5%)",
    "🔄 Dynamic WC rate analysis and max rate suggestions",
    "📈 Auto-sorted profit display by percentage",
    "🔍 Individual item toggle and filtering",
    "💾 Persistent settings and calculation history",
    "🌙 Customizable light/dark theme with smooth transitions",
    "📏 Dynamic UI scaling for all elements",
    "🎨 Custom fonts and styling options",
    "📱 Responsive layout with auto-adjusting tables",
    "✨ Visual feedback for profitable/non-profitable items",
    "🔄 One-click regeneration of previous calculations",
    "📋 Detailed calculation history with timestamps",
    "🌳 Tree-based organization for history and changelog",
    "💬 Integrated contact and changelog system",
    "⌨️ Input validation and error handling",
    "🎯 Precise profit margin targeting",
    "🖥️ Cross-platform compatibility",
    "🔒 Settings persistence across sessions",
    "📊 Dynamic table column management",
    "🎨 Custom styling for UI elements",
    "🔍 Detailed item pack size consideration"
]
 
#region 📥 Imports
# 📚 Standard Library Imports
import os                                   # 📂 File system operations
import sys                                  # 💻 System functions
import json                                 # 📝 JSON handling
from datetime import datetime               # 🕰️ Time utilities
from dataclasses import dataclass           # 📦 Data structures
from typing import List, Tuple, Optional    # 🔍 Type hints

# ⚙️ PyQt6 Core
from PyQt6.QtCore import (
    # 🎯 Core Types
    Qt, QUrl, QSize, QRect,
    # 🔢 Model Interfaces
    QAbstractItemModel, QModelIndex, QSortFilterProxyModel,
    # 💡 Signals and Slots
    pyqtSignal,
    # ⏱️ Events
    QEvent, QTimer,
    # 💾 Settings
    QSettings
)

# 🖥️ PyQt6 Widgets
from PyQt6.QtWidgets import (
    # 🚀 Core Components
    QApplication, QMainWindow, QDialog, QWidget,
    # 📐 Layouts
    QVBoxLayout, QHBoxLayout, QGridLayout, QLayout,
    QSizePolicy, QSpacerItem,
    # 🎛️ Basic Widgets
    QLabel, QLineEdit, QPushButton, QFrame,
    QGroupBox, QMessageBox,
    # 📊 Data Display
    QTableWidget, QTableWidgetItem, QHeaderView,
    QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem,
    # 🛠️ Specialized Widgets
    QScrollArea, QSlider, QFontComboBox, QDialogButtonBox,
    # ✨ Visual Elements
    QStyledItemDelegate, QAbstractItemView, QGraphicsOpacityEffect, QStyleOptionViewItem,
)

# 🎨 PyQt6 Graphics
from PyQt6.QtGui import (
    # 🎯 Styling
    QFont, QPalette, QColor, QTextCharFormat,
    # 🖌️ Drawing
    QPainter, QBrush, QPen, QPixmap,
    # 📏 Metrics
    QFontMetrics, QResizeEvent,
    # 📄 Text Handling
    QTextDocument, QTextCursor, QAbstractTextDocumentLayout,
    # 🌐 System Integration
    QDesktopServices,
    # 🎨 Icons and Images
    QIcon,
)
#endregion

#region ⚛️ Application Constants
# 👤 Author Information
CREATOR = "Orin#MLQhB"                      # 🎮 Maple Worlds ID
GITHUB_LINK = "https://github.com/or1n"     # 💻 Source code repository
DISCORD_TAG = "orin.abc"                    # 💬 Contact information

# 📱 Application Identity
APP_NAME = "Artale WC Merch Calc"           # Application display name
COMPANY_NAME = "or1n"                       # Publisher name
PRODUCT_NAME = "Artale WC Merch Calculator"
INTERNAL_NAME = "ArtaleWCMerchCalc"
FILE_DESCRIPTION = "Artale WC Merch Calculator"
ORIGINAL_FILENAME = "ArtaleWCMerchCalc.exe"

# 📚 Technical Details
SERVER = "Artale US"                        # 🌍 Server name
PLATFORM = "Maple Worlds",                  # 🎮 Gaming platform
CURRENCY = "World Coin"                     # 💎 Trading currency

# ℹ️ Usage Information
AUCTION_FEE = 0.05                          # 💸 5% auction house fee
MIN_PROFIT = 0.0                            # 📊 Minimum profit threshold

# 📅 Version Generation
NOW = datetime.now()
VERSION = f"{NOW.year % 100:02d}.{NOW.month:02d}.{NOW.day:02d}.{NOW.hour:02d}"
LEGAL_COPYRIGHT = f"(c) {NOW.year} {CREATOR}"

# 💰 Default Values
DEFAULT_WC_RATE = 2600    # Default Worker Crystal exchange rate
DEFAULT_PROFIT = 5.0      # Default profit percentage target
#endregion

#region 📦 Version Management
# 📦 Get version based on runtime environment
def get_version() -> str:
    # 🔍 Check if running as exe or development
    if getattr(sys, 'frozen', False):  
        version_path = os.path.join(os.path.dirname(sys.executable), "version_info.txt")
        
        try:
            # 📂 Read version from file if exists
            if os.path.exists(version_path):
                with open(version_path, 'r') as file:
                    version_line = file.readline()
                    return version_line.strip().split('=')[-1].strip('"')
            return "Unknown Version"  # ❌ File not found
        except Exception:
            return "Error Reading Version"  # ❌ File read error
    else:
        return VERSION  # 🔄 Development version

# 🏷️ Create UI version label
def create_version_label() -> QLabel:
    label = QLabel(f'<b><font size="2">v{VERSION}</font></b>')
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label

# 📝 Version info template for executable
VERSION_INFO_TEMPLATE = f"""
VSVersionInfo(
    ffi=FixedFileInfo(
        # Version numbers
        filevers=({VERSION}),
        prodvers=({VERSION}),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable(
                u'040904B0',
                [
                    # File metadata
                    StringStruct(u'CompanyName', u'{COMPANY_NAME}'),
                    StringStruct(u'FileDescription', u'{FILE_DESCRIPTION}'),
                    StringStruct(u'FileVersion', u'{VERSION}'),
                    StringStruct(u'InternalName', u'{INTERNAL_NAME}'),
                    StringStruct(u'LegalCopyright', u'{LEGAL_COPYRIGHT}'),
                    StringStruct(u'OriginalFilename', u'{ORIGINAL_FILENAME}'),
                    StringStruct(u'ProductName', u'{PRODUCT_NAME}'),
                    StringStruct(u'ProductVersion', u'{VERSION}')
                ]
            )
        ])
    ]
)
"""

# 💾 Save version info to file
try:
    with open("version_info.txt", "w") as version_file:
        version_file.write(VERSION_INFO_TEMPLATE)
except Exception as e:
    print(f"❌ Error saving version info: {e}")  # Log error if file write fails

# 🔄 Initialize version
version = get_version()
#endregion

#region 📜 Changelog Content
CHANGELOG_2024_12_06_04 = """
v24.12.06.04
    - Added HistoryDialog
        * "Select" and "Trash" buttons
        * Auto unfold entry details on click
        * Complete history saving of calculations
        * Entry selection and bulk delete
        * State preservation for expanded entries
        * Detailed calculation history with timestamps
        * Tree-based organization for history and changelog
    - Enhanced tree-based organization
        * Hierarchical view for history entries
        * Year/month/day grouping for navigation
    - Improved table management
        * Dynamic column width calculations
        * Custom transparent styling and alignment
        * Custom item delegate for painting table items
        * Visual feedback for profitable/non-profitable items
        * Transparent backgrounds, no grid lines
        * Enhanced visual hierarchy, spacing, and alignment
    - Enhanced UI scaling and styling
        * Dynamic UI scaling for all elements
        * Custom fonts and styling options
        * Responsive layout with auto-adjusting tables
        * Detailed item pack size consideration
        * Added new button classes: ScalableButton, ScalableToggleButton, ScalableCalculateButton
    - Improved input handling and validation
        * Input validation and error handling
        * Cross-platform compatibility
        * Settings persistence across sessions
        * Dynamic table column management
        * Custom styling for UI elements
    - Enhanced dialogs
        * SettingsDialog: Theme, scale, and font choice real-time updates, added value UI for theme and scale
        * ContactDialog: Improved layout and styling, clickable GitHub link
        * ChangelogDialog: Tree system for organizing changelogs by years and months
    - Updated MerchantCalculator
        * Added icon and image to the header
        * Centered controls area
        * Enhanced navigation with History, Contact, Settings, and Changelog buttons
        * Added font selection with system font support and custom font loading
        * Smooth theme transitions with light/dark mode support
        * Real-time updates for theme, scale, and font choice
    - Enhanced codebase documentation and organization
        * Comprehensive inline code comments
        * Improved import categorization and region structure
        * Robust error handling for version management
        * Restructured configuration constants for better maintainability
"""

CHANGELOG_2024_11_14_03 = """
v24.11.14.03
    -  Implemented QSettings for persistent data storage
        *  Rate and profit inputs now save between sessions
        *  Item prices persist across application restarts
        *  Theme and scale preferences are preserved
    -  Enhanced real-time UI updates
        *  Dynamic theme transitions
        *  Smooth scaling animations
        *  Instant calculation updates
    -  Added Settings Dialog with
        *  Theme slider (Light/Dark mode)
        *  UI Scale control
        *  Font selection
    -  Added Contact Dialog with
        *  Developer information
        *  GitHub repository link
        *  Discord contact details
    -  Fixed scaling issues with
        *  Table headers and content
        *  Input fields and buttons
        *  Dialog windows
    -  Enhanced navigation with
        *  History button
        *  Contact button
        *  Settings button
        *  Changelog button
"""

CHANGELOG_2024_11_13_23 = """
v24.11.13.23
    -  Implemented comprehensive changelog system
        *  Version history tracking
        *  Feature documentation
        *  Bug fix records
    -  Added creator information header
        *  Developer identification
        *  Contact details
        *  Project links
    -  Added complete theme customization
        *  Light/Dark mode support
        *  Custom color schemes
        *  Smooth theme transitions
    -  Implemented dynamic UI scaling
        *  Responsive layouts
        *  Font size adjustments
        *  Component resizing
    -  Added font selection
        *  System font support
        *  Custom font loading
        *  Font size controls
"""

CHANGELOG_2024_11_11_16 = """
v24.11.11.16 (Initial Release)
    -  Core calculation functionality
        *  World Coin rate conversion
        *  Auction house fee calculation (5%)
        *  Profit margin computation
    -  Basic UI implementation
        *  Rate input field
        *  Profit target input
        *  Item price fields
    -  Calculation features
        *  Real-time updates
        *  Sorted results display
        *  Profit/loss indicators
"""
#endregion

#region 📊 Data Structures
# 📦 Core Item Properties
@dataclass
class Item:
    name: str               # 📝 Item name
    wc_cost: float          # 💎 World Coin cost
    pack_size: int = 1      # 📦 Items per craft/pack

    @property
    def unit_wc_cost(self) -> float:
        # 🧮 Calculate cost per individual item
        return self.wc_cost / max(1, self.pack_size)  # Prevent division by zero

# 📦 Item result calculations
class ItemResult:
    def __init__(self, item: Item, ah_price: int, wc_rate: int):
        # 📦 Input Parameters
        self.item = item              # Original item being analyzed
        self.ah_price = ah_price      # Listed price on Auction House
        self.wc_rate = wc_rate        # Current WC to mesos conversion rate

        # 💰 Cost Calculations
        self.buying_cost = int(item.unit_wc_cost * wc_rate)  # Total cost in mesos
        self.cost = self.buying_cost  # Alias for clarity in calculations

        # 📊 Sale Price Calculations
        self.sale_price = ah_price - 1  # Competitive price (1 meso below AH)
        self.ah_fee = int(self.sale_price * AUCTION_FEE)  # 5% AH fee
        self.net = int(self.sale_price * (1 - AUCTION_FEE))  # Amount after fees

        # 📈 Profit Analysis
        self.profit_mesos = self.net - self.cost  # Raw profit in mesos
        self.profit_percent = self._calculate_profit_percent()  # Percentage return

    # 📈 Calculate profit percentage
    def _calculate_profit_percent(self) -> float:
        return (self.profit_mesos / self.cost * 100) if self.cost > 0 else 0

    # 📈 Check if item is profitable
    def is_profitable(self) -> bool:
        return self.profit_percent > MIN_PROFIT

    # 📈 Calculate max rate for desired profit
    def calculate_max_rate(self, desired_profit_percent: float) -> int:
        if self.ah_price <= 1:
            return 0  # Prevent calculations with invalid prices
            
        net = (self.ah_price - 1) * (1 - AUCTION_FEE)  # Net after fees
        max_cost = net / (1 + desired_profit_percent / 100)  # Max cost for target profit
        return int(max_cost / self.item.unit_wc_cost)  # Convert to WC rate
#endregion

#region 🎯 Resource Management
# 🎯 Get absolute path for resources
def resource_path(relative_path: str) -> str:
    # 🎯 Purpose: Get absolute path for resources, handling PyInstaller packaging
    try:
        # 📦 Check if running as bundled executable
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
        
        # 🔍 Create absolute path
        absolute_path = os.path.join(base_path, relative_path)
        
        # ✅ Verify path exists
        if not os.path.exists(absolute_path):
            print(f"⚠️ Warning: Resource not found at {absolute_path}")
        
        return absolute_path

    except Exception as e:
        # ❌ Handle errors gracefully
        print(f"❌ Error resolving resource path: {e}")
        return os.path.join(os.path.abspath('.'), relative_path)
#endregion

#region 🎨 Theme Management
# 🎨 Color palette management for light/dark themes
class DarkLightPalette:
    def __init__(self):
        # 🌞 Light Theme Colors
        self.light = {
            'window': '#F5F5F5',    # 🪟 Main window background
            'text': '#2b2b2b',      # 📝 Primary text color
            'button': '#E0E0E0',    # 🔘 Button background
            'input': '#FFFFFF',     # ⌨️ Input field background
            'profit': '#008000',    # 📈 Profit indicator (green)
            'loss': '#FF0000',      # 📉 Loss indicator (red)
            'header': '#D3D3D3',    # 🎯 Header background
            'border': '#CCCCCC'     # 🔲 Border elements
        }

        # 🌙 Dark Theme Colors
        self.dark = {
            'window': '#121212',    # 🪟 Main window background
            'text': '#E0E0E0',      # 📝 Primary text color
            'button': '#2C2C2C',    # 🔘 Button background
            'input': '#2D2D2D',     # ⌨️ Input field background
            'profit': '#00CC00',    # 📈 Profit indicator (darker green)
            'loss': '#CC3333',      # 📉 Loss indicator (darker red)
            'header': '#1A1A1A',    # 🎯 Header background
            'border': '#303030'     # 🔲 Border elements
        }

    # 🎨 Calculate color based on theme value
    def get_interpolated_color(self, key: str, theme_value: float) -> QColor:
        try:
            # 🎯 Get light and dark colors
            light_color = QColor(self.light[key])
            dark_color = QColor(self.dark[key])
            factor = theme_value / 100

            # 🎨 Interpolate RGB values
            r = int(light_color.red() * (1 - factor) + dark_color.red() * factor)
            g = int(light_color.green() * (1 - factor) + dark_color.green() * factor)
            b = int(light_color.blue() * (1 - factor) + dark_color.blue() * factor)

            return QColor(r, g, b)
        except KeyError:
            print(f"❌ Invalid color key: {key}")
            return QColor(self.light['text'])  # ⚠️ Fallback to default
        except Exception as e:
            print(f"❌ Error calculating color: {e}")
            return QColor(self.light['text'])  # ⚠️ Fallback to default

    # 🎨 Generate complete palette for given theme value
    def get_theme_palette(self, theme_value: float) -> QPalette:
        try:
            # 🎨 Create new palette
            palette = QPalette()

            # 📝 Set standard colors
            palette.setColor(QPalette.ColorRole.Window, 
                           self.get_interpolated_color('window', theme_value))
            palette.setColor(QPalette.ColorRole.WindowText, 
                           self.get_interpolated_color('text', theme_value))
            palette.setColor(QPalette.ColorRole.Button, 
                           self.get_interpolated_color('button', theme_value))
            palette.setColor(QPalette.ColorRole.Base, 
                           self.get_interpolated_color('input', theme_value))
            palette.setColor(QPalette.ColorRole.Text, 
                           self.get_interpolated_color('text', theme_value))

            return palette
        except Exception as e:
            print(f"❌ Error creating palette: {e}")
            return QPalette()  # ⚠️ Return default palette
#endregion

#region 🧩 UI Components
# 🏷️ Manages clickable label widget with hover effects
class ClickableLabel(QLabel):
    def __init__(self, text: str, link: str, parent=None):
        super().__init__(text, parent)
        self.link = link          # Store URL
        self._setup_appearance()  # Configure visual style
        
    # 🎨 Configure visual style
    def _setup_appearance(self):
        font = self.font()
        font.setBold(True)
        font.setUnderline(True)
        self.setFont(font)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # 🌐 Open URL when clicked
    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.link))

    # 🖱️ Mouse hover effect - unbold and remove underline
    def enterEvent(self, event: QEvent) -> None:
        font = self.font()
        font.setBold(False)
        font.setUnderline(False)
        self.setFont(font)
        super().enterEvent(event)

    # 🖱️ Mouse leave effect - restore bold and underline
    def leaveEvent(self, event) -> None:
        font = self.font()
        font.setBold(True)
        font.setUnderline(True)
        self.setFont(font)
        super().leaveEvent(event)

# 📝 Creates label widget with bold text styling
class BoldText(QLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        font = self.font()
        font.setBold(True)
        self.setFont(font)

# ⌨️ Enhanced LineEdit with custom placeholder text rendering
class CustomLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 🎨 Draw placeholder if no text
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.placeholderText() and not self.text():
            painter = QPainter(self)
            painter.setPen(QColor(169, 169, 169))  # 🎨 Placeholder color
            painter.setFont(self.font())

            rect = self.rect()
            padding = 10
            painter.drawText(
                rect.adjusted(padding, 0, -padding, 0),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                self.placeholderText()
            )
            painter.end()

# 📏 Input field that scales based on application settings
class ScalableLineEdit(QLineEdit):
    heightChanged = pyqtSignal(int)  # Signal for height changes

    def __init__(self, num_digits, padding=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_digits = num_digits  # Number of digits to display
        self.original_font_size = self.font().pointSize()
        self.scale_factor = 1.0
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._update_dimensions()

    # 📏 Update font size on resize
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()
        self.heightChanged.emit(self.height())

    def set_scale_factor(self, scale_factor):
        self.scale_factor = scale_factor
        self._update_font_size()
        self._update_dimensions()

    def _update_font_size(self):
        font = self.font()
        new_font_size = int(self.original_font_size * self.scale_factor)
        font.setPointSize(new_font_size)
        self.setFont(font)

    def _update_dimensions(self):
        # Calculate the width of a single digit in the current font
        digit_width = self.fontMetrics().horizontalAdvance('0')
        # Set the fixed width based on the number of digits and padding
        content_width = digit_width * self.num_digits + 25
        self.setFixedWidth(content_width)

# 🔘 Button that scales dynamically with application settings
class ScalableButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_font_size = self.font().pointSize()
        self.original_width = self.sizeHint().width()
        self.original_height = self.sizeHint().height()
        self.scale_factor = 1.0

    def set_scale_factor(self, factor: float):
        self.scale_factor = factor
        self._update_font_size()
        self._update_dimensions()

    def _update_font_size(self):
        font = self.font()
        font.setPointSize(int(self.original_font_size * self.scale_factor))
        self.setFont(font)

    def _update_dimensions(self):
        new_width = int(self.original_width * self.scale_factor)
        new_height = int(self.original_height * self.scale_factor)
        self.setFixedSize(new_width, new_height)

# 🔄 Toggle button that scales with application settings
class ScalableToggleButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_font_size = self.font().pointSize()
        self.original_size = self.sizeHint().height()  # Use height to maintain square shape
        self.scale_factor = 1.0

    def set_scale_factor(self, factor: float):
        self.scale_factor = factor
        self._update_font_size()
        self._update_dimensions()

    def _update_font_size(self):
        font = self.font()
        font.setPointSize(int(self.original_font_size * self.scale_factor))
        self.setFont(font)

    def _update_dimensions(self):
        new_size = int(self.original_size * self.scale_factor)
        self.setFixedSize(new_size, new_size)

# 🧮 Calculate button with dynamic scaling capabilities
class ScalableCalculateButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_initial_state()
        
    def _setup_initial_state(self):
        self.scale_factor = 1.0
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFixedHeight(30)
        self.setFixedWidth(100)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()
        self._update_dimensions()

    def _update_font_size(self):
        font = self.font()
        new_font_size = int(self.original_font_size * self.scale_factor)
        font.setPointSize(new_font_size)
        self.setFont(font)

    def _update_dimensions(self):
        min_width = max(120, int(120 * self.scale_factor))
        self.setMinimumWidth(min_width)
        fixed_height = max(35, int(35 * self.scale_factor))
        self.setFixedHeight(fixed_height)

    def set_scale_factor(self, factor: float):
        self.scale_factor = factor
        self.resizeEvent(None)

# 🎨 Custom styling for table items with profitability indicators
class TableItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scale_factor = 1.0
        self.theme_value = 100

    def set_theme_value(self, value: int):
        self.theme_value = value
        self._trigger_repaint()

    def set_scale_factor(self, factor: float):
        self.scale_factor = factor
        self._trigger_repaint()

    def _trigger_repaint(self):
        try:
            if hasattr(self.parent(), 'table'):
                self.parent().table.viewport().update()
            elif hasattr(self.parent(), 'update'):
                self.parent().update()
        except Exception:
            pass

    def paint(self, painter, option, index):
        # Scale font size
        adjusted_font = QFont(option.font)
        adjusted_font.setPointSizeF(option.font.pointSize() * self.scale_factor)
        option.font = adjusted_font

        # Get profitability status
        is_profitable = index.data(Qt.ItemDataRole.UserRole)

        # Configure font styling
        font = QFont(option.font)
        font.setBold(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        opacity = 1.0

        # Apply conditional formatting
        if index.column() == 3 and is_profitable:  # 📈 Sale price for profitable items
            font.setBold(True)
            font.setUnderline(True)
        elif index.column() == 8 and not is_profitable:  # ⚡ Max rate for non-profitable items
            font.setBold(True)
        elif not is_profitable:  # ❌ Non-profitable items
            font.setStrikeOut(True)
            opacity = 0.1

        # Paint with styling
        painter.save()
        painter.setOpacity(opacity)
        option.font = font
        super().paint(painter, option, index)
        painter.restore()

# 🎨 Custom table item styling
class ChangelogItemDelegate(QStyledItemDelegate):
    BASE_FONT_SIZE = 8  # Base font size in points

    # Font size increments as percentages of the base font size
    YEAR_FONT_SIZE_PERCENT = 1.20  # 140% of base font size
    MONTH_FONT_SIZE_PERCENT = 1.15  # 130% of base font size
    ENTRY_FONT_SIZE_PERCENT = 1.10  # 120% of base font size
    DASH_FONT_SIZE_PERCENT = 1.05  # 110% of base font size
    STAR_FONT_SIZE_PERCENT = 1.0  # 100% of base font size

    # Font bold settings
    YEAR_FONT_BOLD = True
    MONTH_FONT_BOLD = True
    ENTRY_FONT_BOLD = True
    DASH_FONT_BOLD = True
    STAR_FONT_BOLD = True
    STAR_FONT_ITALIC = True

    # Row height adjustment percentages
    YEAR_HEIGHT_PERCENT = 1.25
    MONTH_HEIGHT_PERCENT = 1.25
    ENTRY_HEIGHT_PERCENT = 1.25
    DASH_ROW_HEIGHT_PERCENT = 1.10
    STAR_ROW_HEIGHT_PERCENT = 1.10

    # Indentation constants
    STAR_INDENT_SPACES = 5  # Number of spaces before '*' entries

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = parent
        self.scale_factor = 1.0

    def set_scale_factor(self, factor: float):
        self.scale_factor = factor
        self._trigger_repaint()

    def _trigger_repaint(self):
        try:
            if hasattr(self.parent(), 'viewport'):
                self.parent().viewport().update()
            elif hasattr(self.parent(), 'update'):
                self.parent().update()
        except Exception:
            pass

    def paint(self, painter, option, index):
        level = self._item_level(index)
        text = index.data(Qt.ItemDataRole.DisplayRole)
        font = QFont(option.font)
        painter.save()

        # Adjust font size based on level and scale factor
        if level == 0:  # Year
            font.setPointSizeF(self.BASE_FONT_SIZE * self.YEAR_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.YEAR_FONT_BOLD)
        elif level == 1:  # Month
            font.setPointSizeF(self.BASE_FONT_SIZE * self.MONTH_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.MONTH_FONT_BOLD)
        elif level == 2:  # Entry (version title)
            font.setPointSizeF(self.BASE_FONT_SIZE * self.ENTRY_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.ENTRY_FONT_BOLD)
        elif level == 3:  # Dash or Star rows
            text = text.strip()
            if text.startswith('-'):
                font.setPointSizeF(self.BASE_FONT_SIZE * self.DASH_FONT_SIZE_PERCENT * self.scale_factor)
            elif text.startswith('*'):
                font.setPointSizeF(self.BASE_FONT_SIZE * self.STAR_FONT_SIZE_PERCENT * self.scale_factor)
            else:
                font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)
        else:
            font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)

        # Handle special formatting for '-' and '*' characters
        if level == 3 and (text.startswith('-') or text.startswith('*')):
            char = text[0]
            rest_text = text[1:].strip()

            # Prepare the first character formatting
            char_format = QTextCharFormat()
            char_format.setFont(QFont(font))  # Use current font settings
            if char == '-':
                if self.DASH_FONT_BOLD:
                    char_format.setFontWeight(QFont.Weight.Bold)
            elif char == '*':
                if self.STAR_FONT_BOLD:
                    char_format.setFontWeight(QFont.Weight.Bold)
                if self.STAR_FONT_ITALIC:
                    char_format.setFontItalic(True)

            # Prepare the rest of the text formatting
            rest_format = QTextCharFormat()
            rest_font = QFont(font)  # Create a copy of the font
            rest_font.setBold(False)  # Ensure rest of the text is not bold
            rest_font.setItalic(False)  # Ensure rest of the text is not italic
            rest_format.setFont(rest_font)

            # Create text document for rich text rendering
            doc = QTextDocument()
            cursor = QTextCursor(doc)

            # Adjust indentation for '*' entries
            if char == '*':
                indent = ' ' * self.STAR_INDENT_SPACES
                cursor.insertText(indent)

            # Insert the formatted first character
            cursor.insertText(char, char_format)

            # Insert the rest of the text
            cursor.insertText(' ' + rest_text, rest_format)

            # Draw the text
            painter.translate(option.rect.topLeft())
            ctx = QAbstractTextDocumentLayout.PaintContext()
            doc.documentLayout().draw(painter, ctx)
            painter.restore()
            return  # Manually handled painting

        # Set adjusted font
        option.font = font
        super().paint(painter, option, index)
        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        level = self._item_level(index)
        font = QFont(option.font)

        # Calculate row height based on level and scale factor
        if level == 0:  # Year
            row_height_percent = self.YEAR_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.YEAR_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 1:  # Month
            row_height_percent = self.MONTH_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.MONTH_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 2:  # Entry (version title)
            row_height_percent = self.ENTRY_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.ENTRY_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 3:
            text = index.data(Qt.ItemDataRole.DisplayRole).strip()
            if text.startswith('-'):
                row_height_percent = self.DASH_ROW_HEIGHT_PERCENT
                font.setPointSizeF(self.BASE_FONT_SIZE * self.DASH_FONT_SIZE_PERCENT * self.scale_factor)
            elif text.startswith('*'):
                row_height_percent = self.STAR_ROW_HEIGHT_PERCENT
                font.setPointSizeF(self.BASE_FONT_SIZE * self.STAR_FONT_SIZE_PERCENT * self.scale_factor)
            else:
                row_height_percent = 1.0
                font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)
        else:
            row_height_percent = 1.0
            font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)

        # Update font metrics
        fm = QFontMetrics(font)
        size.setHeight(int(fm.height() * row_height_percent))
        size.setWidth(fm.horizontalAdvance(index.data(Qt.ItemDataRole.DisplayRole)))
        return size

    # 🎯 Get tree item nesting level
    def _item_level(self, index):
        level = 0
        parent = index.parent()
        while parent.isValid():
            level += 1
            parent = parent.parent()
        return level

#endregion

#region 📜 History Dialog
# 📜 Dialog for managing calculation history entries
class HistoryDialog(QDialog):
    SETTINGSDIALOG_SCREEN_HEIGHT_PERCENT = 0.8  # 80% of screen height
    SETTINGSDIALOG_SCREEN_WIDTH_PERCENT = 0.5   # 50% of screen width

    PADDING_HEIGHT = 45  # Padding for height adjustment
    PADDING_WIDTH = 140  # Padding for width adjustment

    regenerate_requested = pyqtSignal(dict)  # Signal to regenerate calculation

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculation History")

        self.selected_entries = set()  # Track selected entries

        self._setup_ui()
        self.load_history()

        # Set the scale factor for the item delegate
        if parent:
            scale_factor = parent.scale_factor
            self.item_delegate.set_scale_factor(scale_factor)

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.history_tree = QTreeWidget()
        self.history_tree.setHeaderHidden(True)
        self.history_tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.history_tree.itemExpanded.connect(self.adjust_size)
        self.history_tree.itemCollapsed.connect(self.adjust_size)
        self.history_tree.itemClicked.connect(self.on_item_clicked)  # Handle item click

        # Apply custom item delegate
        self.item_delegate = HistoryItemDelegate(self)
        self.history_tree.setItemDelegate(self.item_delegate)

        layout.addWidget(self.history_tree)

        # Button layout
        button_layout = QHBoxLayout()

        # Add stretch to center the generate button
        button_layout.addStretch()

        # Generate button
        self.generate_button = ScalableButton("Generate")
        self.generate_button.clicked.connect(self.generate_selected)
        button_layout.addWidget(self.generate_button)

        # Add stretch to push the trash button to the right
        button_layout.addStretch()

        # Trash button
        self.trash_button = QPushButton("🗑️")
        self.trash_button.clicked.connect(self.confirm_delete_entries)
        self.trash_button.setFixedSize(30, 30)
        button_layout.addWidget(self.trash_button)

        layout.addLayout(button_layout)

    def load_history(self):
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        history_json = settings.value("calculation_history", "{}")

        print(f"Loading history~")  # Debug print

        try:
            history = json.loads(history_json)
            print(f"Loaded entries: {len(history)}")  # Debug print

            # Clear existing items
            self.history_tree.clear()

            # Organize history by year, month, and day
            organized_history = {}
            for timestamp, data in sorted(history.items(), reverse=True):
                dt = datetime.strptime(timestamp, "%y.%m.%d.%H.%M.%S")

                year = dt.strftime("%Y")
                month = dt.strftime("%B")
                day = dt.strftime("%d")

                if year not in organized_history:
                    organized_history[year] = {}
                if month not in organized_history[year]:
                    organized_history[year][month] = {}
                if day not in organized_history[year][month]:
                    organized_history[year][month][day] = []

                organized_history[year][month][day].append((timestamp, data))

            # Populate the tree with organized history
            for year, months in organized_history.items():
                year_item = QTreeWidgetItem([year])
                self.history_tree.addTopLevelItem(year_item)

                for month, days in months.items():
                    month_item = QTreeWidgetItem([month])
                    year_item.addChild(month_item)

                    for day, entries in days.items():
                        day_item = QTreeWidgetItem([day])
                        month_item.addChild(day_item)

                        for timestamp, data in entries:
                            dt = datetime.strptime(timestamp, "%y.%m.%d.%H.%M.%S")
                            entry_text = f"{dt.strftime('%Hh %Mm %Ss')} ({len(data['results'])} items)"
                            entry_item = QTreeWidgetItem()
                            entry_item.setData(0, Qt.ItemDataRole.UserRole, timestamp)
                            day_item.addChild(entry_item)

                            # Create a container widget for the select button and entry text
                            container_widget = QWidget()
                            container_layout = QHBoxLayout(container_widget)
                            container_layout.setContentsMargins(0, 0, 0, 0)

                            # Add select button
                            select_button = QPushButton()
                            select_button.setFixedSize(20, 20)
                            select_button.clicked.connect(lambda _, item=entry_item: self.toggle_select_entry(item))
                            container_layout.addWidget(select_button)

                            # Add entry text label
                            entry_label = QLabel(entry_text)
                            container_layout.addWidget(entry_label)

                            # Set the custom widget for the entry item
                            self.history_tree.setItemWidget(entry_item, 0, container_widget)

                            # Add additional details
                            details_widget = QWidget()
                            details_layout = QVBoxLayout(details_widget)
                            details_layout.setContentsMargins(20, 0, 0, 0)
                            details_layout.addWidget(QLabel(f"Rate: {data['rate']}"))
                            details_layout.addWidget(QLabel(f"Desired profit: {data['profit']}%"))
                            items_profitable = sum(1 for result in data['results'] if result['is_profitable'])
                            details_layout.addWidget(QLabel(f"Items profitable: {items_profitable}"))
                            entry_item.addChild(QTreeWidgetItem([""]))
                            self.history_tree.setItemWidget(entry_item.child(0), 0, details_widget)

        except json.JSONDecodeError as e:
            print(f"Error decoding history JSON: {e}")  # Debug print
        except Exception as e:
            print(f"Unexpected error loading history: {e}")  # Debug print

        self.adjust_size()

    def _calculate_item_height(self, item):
        height = self.history_tree.sizeHintForRow(0)
        if item.isExpanded():
            for i in range(item.childCount()):
                height += self._calculate_item_height(item.child(i))
        return height

    def _calculate_item_width(self, item):
        width = self.history_tree.sizeHintForColumn(0)
        if item.isExpanded():
            for i in range(item.childCount()):
                width = max(width, self._calculate_item_width(item.child(i)))
        return width

    # 🔄 Handle item expansion in tree view
    def on_item_expanded(self, item):
        # Handle item expansion to dynamically adjust size.
        self.adjust_size()

    # 🔄 Handle item collapse in tree view
    def on_item_collapsed(self, item):
        # Handle item collapse to dynamically adjust size.
        self.adjust_size()

    # 🖱️ Handle double-click on history entry
    def on_item_double_clicked(self, item, column):
        # If a minute-level item is double-clicked, generate from that history
        if item.parent() and item.parent().parent():
            self._save_tree_state()
            settings = QSettings("or1n", "ArtaleWCMerchCalc")
            settings.setValue("history_dialog_x", self.x())
            settings.setValue("history_dialog_y", self.y())
            self.generate_from_timestamp(item.data(0, Qt.ItemDataRole.UserRole))

    # 🖱️ Handle single click on history entry
    def on_item_clicked(self, item, column):
        # Toggle the expansion state of the item
        item.setExpanded(not item.isExpanded())
        self.adjust_size()

    # 🔄 Generate calculation from selected entry
    def generate_selected(self):
        current_item = self.history_tree.currentItem()
        if current_item and current_item.data(0, Qt.ItemDataRole.UserRole):
            self._save_tree_state()
            settings = QSettings("or1n", "ArtaleWCMerchCalc")
            settings.setValue("history_dialog_x", self.x())
            settings.setValue("history_dialog_y", self.y())
            self.generate_from_timestamp(current_item.data(0, Qt.ItemDataRole.UserRole))

    # 📊 Generate table from history entry
    def generate_from_timestamp(self, timestamp):
        if timestamp:
            settings = QSettings("or1n", "ArtaleWCMerchCalc")
            history_json = settings.value("calculation_history", "{}")
            history = json.loads(history_json)

            if timestamp in history:
                self.parent().regenerate_from_history(history[timestamp])
                self.accept()

    # ✅ Toggle selection state of history entry
    def toggle_select_entry(self, item):
        timestamp = item.data(0, Qt.ItemDataRole.UserRole)
        button = self.history_tree.itemWidget(item, 0).layout().itemAt(0).widget()
        if timestamp in self.selected_entries:
            self.selected_entries.remove(timestamp)
            button.setText("")
        else:
            self.selected_entries.add(timestamp)
            button.setText("🗑️")

    # 🗑️ Show confirmation dialog for entry deletion
    def confirm_delete_entries(self):
        if not self.selected_entries:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Delete entries")
        dialog.setLayout(QVBoxLayout())

        label = QLabel("<b>Are you sure you want to permanently delete these entries?</b>")
        dialog.layout().addWidget(label)

        button_layout = QHBoxLayout()
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)
        dialog.layout().addLayout(button_layout)

        yes_button.clicked.connect(lambda: self.delete_selected_entries(dialog))
        no_button.clicked.connect(dialog.reject)

        dialog.exec()

    # 🗑️ Delete selected entries from history
    def delete_selected_entries(self, dialog):
        # Save the expanded state of the tree
        expanded_state = self._save_expanded_state()

        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        history_json = settings.value("calculation_history", "{}")
        try:
            current_history = json.loads(history_json)
        except json.JSONDecodeError:
            current_history = {}

        for timestamp in self.selected_entries:
            if timestamp in current_history:
                del current_history[timestamp]

        updated_history_json = json.dumps(current_history)
        settings.setValue("calculation_history", updated_history_json)

        dialog.accept()
        self.selected_entries.clear()
        self.load_history()

        # Restore the expanded state of the tree
        self._restore_expanded_state(expanded_state)

    # 💾 Save expanded states before tree updates
    def _save_expanded_state(self):
        expanded_state = {}
        for i in range(self.history_tree.topLevelItemCount()):
            item = self.history_tree.topLevelItem(i)
            expanded_state[item.text(0)] = self._get_expanded_state(item)
        return expanded_state

    # 🔄 Restore previously saved expanded states
    def _restore_expanded_state(self, expanded_state):
        for i in range(self.history_tree.topLevelItemCount()):
            item = self.history_tree.topLevelItem(i)
            self._set_expanded_state(item, expanded_state.get(item.text(0), {}))

    # 🔄 Update dialog size based on screen dimensions
    def adjust_size(self):
        try:
            # Get the active screen size
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # Calculate maximum allowed dimensions based on screen size
            max_height = int(screen_height * self.SETTINGSDIALOG_SCREEN_HEIGHT_PERCENT)
            max_width = int(screen_width * self.SETTINGSDIALOG_SCREEN_WIDTH_PERCENT)

            # Calculate the required height based on the expanded state
            total_height = self.history_tree.sizeHintForRow(0) * self.history_tree.topLevelItemCount()
            for i in range(self.history_tree.topLevelItemCount()):
                item = self.history_tree.topLevelItem(i)
                total_height += self._calculate_item_height(item)

            # Calculate the required width based on the content
            total_width = self.history_tree.sizeHintForColumn(0)
            for i in range(self.history_tree.topLevelItemCount()):
                item = self.history_tree.topLevelItem(i)
                total_width = max(total_width, self._calculate_item_width(item))

            # Adjust the dialog size
            self.setFixedHeight(min(total_height + self.PADDING_HEIGHT, max_height))  # Add some padding and enforce max height
            self.setFixedWidth(min(total_width + self.PADDING_WIDTH, max_width))     # Add some padding and enforce max width
        except Exception as e:
            print(f"Error adjusting size: {e}")  # Debug print

    def showEvent(self, event):
        super().showEvent(event)
        self.adjust_size()
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        dialog_x = settings.value("history_dialog_x", None)
        dialog_y = settings.value("history_dialog_y", None)
        if dialog_x is not None and dialog_y is not None:
            self.move(int(dialog_x), int(dialog_y))
        else:
            parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
            dialog_width = self.width()
            dialog_height = self.height()
            dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
            dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
            self.move(dialog_x, dialog_y)

        # Restore tree state
        self._restore_tree_state()

    def closeEvent(self, event):
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        settings.setValue("history_dialog_x", self.x())
        settings.setValue("history_dialog_y", self.y())
        self._save_tree_state()
        super().closeEvent(event)

    # Save the expanded state of the tree
    def _save_tree_state(self):
        expanded_state = {}
        for i in range(self.history_tree.topLevelItemCount()):
            item = self.history_tree.topLevelItem(i)
            expanded_state[item.text(0)] = self._get_expanded_state(item)
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        settings.setValue("history_tree_state", expanded_state)

    # Get expanded state for individual item
    def _get_expanded_state(self, item):
        state = {'expanded': item.isExpanded(), 'children': {}}
        for i in range(item.childCount()):
            child = item.child(i)
            state['children'][child.text(0)] = self._get_expanded_state(child)
        return state

    # Restore the expanded state of the tree
    def _restore_tree_state(self):
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        expanded_state = settings.value("history_tree_state", {})
        for i in range(self.history_tree.topLevelItemCount()):
            item = self.history_tree.topLevelItem(i)
            self._set_expanded_state(item, expanded_state.get(item.text(0), {}))

    # Set expanded state for individual item
    def _set_expanded_state(self, item, state):
        item.setExpanded(state.get('expanded', False))
        for i in range(item.childCount()):
            child = item.child(i)
            self._set_expanded_state(child, state.get('children', {}).get(child.text(0), {}))

class HistoryItemDelegate(QStyledItemDelegate):
    BASE_FONT_SIZE = 8  # Base font size in points

    # Font size increments as percentages of the base font size
    YEAR_FONT_SIZE_PERCENT = 1.25
    MONTH_FONT_SIZE_PERCENT = 1.20
    DAY_FONT_SIZE_PERCENT = 1.10
    ENTRY_ITEM_SIZE_PERCENT = 1.15
    DETAILS_WIDGET_SIZE_PERCENT = 1.6

    # Font bold settings
    YEAR_FONT_BOLD = True
    MONTH_FONT_BOLD = True
    DAY_FONT_BOLD = True
    ENTRY_ITEM_BOLD = True
    DETAILS_WIDGET_BOLD = False

    # Row height adjustment percentages
    YEAR_HEIGHT_PERCENT = 1.2
    MONTH_HEIGHT_PERCENT = 1.2
    DAY_HEIGHT_PERCENT = 1.2
    ENTRY_HEIGHT_PERCENT = 1.2
    DETAILS_HEIGHT_PERCENT = 1.5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = parent
        self.scale_factor = 1.0

    def set_scale_factor(self, factor: float):
        self.scale_factor = factor
        self._trigger_repaint()

    def _trigger_repaint(self):
        try:
            if hasattr(self.parent(), 'viewport'):
                self.parent().viewport().update()
            elif hasattr(self.parent(), 'update'):
                self.parent().update()
        except Exception:
            pass

    def paint(self, painter, option, index):
        level = self._item_level(index)
        text = index.data(Qt.ItemDataRole.DisplayRole)
        font = QFont(option.font)
        painter.save()

        # Adjust font size based on level and scale factor
        if level == 0:  # Year
            font.setPointSizeF(self.BASE_FONT_SIZE * self.YEAR_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.YEAR_FONT_BOLD)
        elif level == 1:  # Month
            font.setPointSizeF(self.BASE_FONT_SIZE * self.MONTH_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.MONTH_FONT_BOLD)
        elif level == 2:  # Day
            font.setPointSizeF(self.BASE_FONT_SIZE * self.DAY_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.DAY_FONT_BOLD)
        elif level == 3:  # Entry item
            font.setPointSizeF(self.BASE_FONT_SIZE * self.ENTRY_ITEM_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.ENTRY_ITEM_BOLD)
        elif level == 4:  # Details widget
            font.setPointSizeF(self.BASE_FONT_SIZE * self.DETAILS_WIDGET_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.DETAILS_WIDGET_BOLD)
        else:
            font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)

        # Set adjusted font
        option.font = font
        painter.setFont(font)
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        level = self._item_level(index)
        font = QFont(option.font)

        # Calculate row height based on level and scale factor
        if level == 0:  # Year
            row_height_percent = self.YEAR_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.YEAR_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 1:  # Month
            row_height_percent = self.MONTH_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.MONTH_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 2:  # Day
            row_height_percent = self.DAY_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.DAY_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 3:  # Entry item
            row_height_percent = self.ENTRY_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.ENTRY_ITEM_SIZE_PERCENT * self.scale_factor)
        elif level == 4:  # Details widget
            row_height_percent = self.DETAILS_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.DETAILS_WIDGET_SIZE_PERCENT * self.scale_factor)
        else:
            row_height_percent = 1.0
            font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)

        # Update font metrics
        fm = QFontMetrics(font)
        size.setHeight(int(fm.height() * row_height_percent))
        size.setWidth(fm.horizontalAdvance(index.data(Qt.ItemDataRole.DisplayRole)))
        return size

    # 🎯 Get tree item nesting level
    def _item_level(self, index):
        level = 0
        parent = index.parent()
        while parent.isValid():
            level += 1
            parent = parent.parent()
        return level
#endregion

#region 💬 Contact Dialog
# 💬 Dialog displaying developer contact information
class ContactDialog(QDialog):
    CONTACTDIALOG_SCREEN_HEIGHT_PERCENT = 0.8  # 80% of screen height
    CONTACTDIALOG_SCREEN_WIDTH_PERCENT = 0.5   # 50% of screen width
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contact Information")
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Add avatar image
        avatar_label = QLabel()
        avatar_path = os.path.join(os.path.dirname(__file__), "images", "avatar2.png")
        avatar_image = QPixmap(avatar_path)
        avatar_label.setPixmap(avatar_image.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(avatar_label)

        # Add contact information
        github_label = self._create_github_label()
        layout.addWidget(github_label)
        
        artale_label = self._create_artale_label()
        layout.addWidget(artale_label)
        
        profile_label = self._create_profile_label()
        layout.addWidget(profile_label)
        
        discord_label = self._create_discord_label()
        layout.addWidget(discord_label)
        
        ok_button = self._create_ok_button()
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self._configure_sizing()

    def _create_artale_label(self):
        artale_label = QLabel(f'<b>Server: {SERVER}</b>')
        artale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return artale_label

    def _create_profile_label(self):
        profile_label = QLabel(f'<b>Character: {CREATOR}</b>')
        profile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return profile_label

    def _create_discord_label(self):
        discord_label = QLabel(f'<b>Discord: {DISCORD_TAG}</b>')
        discord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return discord_label

    def _create_github_label(self):
        github_label = ClickableLabel(f'<b><font color="orange">GitHub: {COMPANY_NAME}</font></b>', GITHUB_LINK)
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return github_label

    def _create_ok_button(self):
        ok_button = ScalableButton("Close")
        ok_button.clicked.connect(self.save_and_close)
        ok_button.setFixedWidth(100)
        ok_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        return ok_button

    def _configure_sizing(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # 🔄 Update dialog size based on screen dimensions
    def adjust_size(self):
        try:
            # Get the active screen size
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # Calculate maximum allowed dimensions based on screen size
            max_height = int(screen_height * self.CONTACTDIALOG_SCREEN_HEIGHT_PERCENT)
            max_width = int(screen_width * self.CONTACTDIALOG_SCREEN_WIDTH_PERCENT)

            # Adjust the dialog size
            self.setFixedHeight(min(self.sizeHint().height(), max_height))  # Enforce max height
            self.setFixedWidth(min(self.sizeHint().width(), max_width))     # Enforce max width
        except Exception as e:
            print(f"Error adjusting size: {e}")  # Debug print

    # Override closeEvent to simulate Close button press when the window is closed.
    def closeEvent(self, event):
        self.save_and_close()
        event.accept()

    # 💾 Save settings and close dialog
    def save_and_close(self):
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        settings.setValue("contact_dialog_x", self.x())
        settings.setValue("contact_dialog_y", self.y())
        self.accept()  # Close the dialog

    def showEvent(self, event):
        super().showEvent(event)
        self.adjust_size()
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        dialog_x = settings.value("contact_dialog_x", None)
        dialog_y = settings.value("contact_dialog_y", None)
        if dialog_x is not None and dialog_y is not None:
            self.move(int(dialog_x), int(dialog_y))
        else:
            parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
            dialog_width = self.width()
            dialog_height = self.height()
            dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
            dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
            self.move(dialog_x, dialog_y)




# endregion

#region ⚙️ Settings Dialog
# ⚙️ Dialog for application settings and preferences
class SettingsDialog(QDialog):
    SETTINGSDIALOG_SCREEN_HEIGHT_PERCENT = 0.8  # 80% of screen height
    SETTINGSDIALOG_SCREEN_WIDTH_PERCENT = 0.5   # 50% of screen width
    
    VALUE_LABEL_FONT_SIZE = 10  # Constant for value label font size

    #region 🏁 Initialization
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("or1n", "ArtaleWCMerchCalc")  # Match main app settings

        # Initialize color palette
        self.color_palette = DarkLightPalette()

        # Create UI elements and initialize state
        self.theme_slider = None
        self.scale_slider = None
        self.font_combo = None
        self.theme_label = None
        self.scale_label = None
        self.font_label = None
        self.theme_value_label = None
        self.scale_value_label = None

        # Set up UI after initializing variables
        self.init_ui()

        # Load UI settings after the UI components are created
        self.load_ui_settings()

    # 🪟 Prepare main window properties and positioning
    def _prepare_window(self):
        self._set_window_size_policy()
        self._set_window_title()

    def _set_window_size_policy(self):
        # Set the size policy for the window
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.adjustSize()

    def _set_window_title(self):
        # Set the window title
        self.setWindowTitle("Settings")

    # 📦 Create primary container for UI components
    def _create_main_container(self):
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)  # Set layout on main_widget
        self.setLayout(QVBoxLayout())  # Set a layout for the dialog itself
        self.layout().addWidget(main_widget)  # Add main_widget to dialog's layout
        return main_widget
    #endregion

    #region 🎨 User Interface
    def init_ui(self):
        # 🏗 Orchestrate complete user interface initialization
        self._prepare_window()
        main_widget = self._create_main_container()

        # Construct UI sections in order
        self._build_theme_section(main_widget)
        self._build_scale_section(main_widget)
        self._build_font_selection_section(main_widget)

        # Final configuration
        self._configure_layout(main_widget)

        # Initial application of the theme and scale based on slider values
        self.update_theme(self.theme_slider.value())
        self.update_scale(self.scale_slider.value())

    # 🎨 Construct theme section with inputs
    def _build_theme_section(self, main_widget):
        theme_frame = self._create_theme_frame()
        main_widget.layout().addWidget(theme_frame)

    # 🖼 Create theme container frame
    def _create_theme_frame(self):
        theme_frame = QFrame()
        theme_frame.setFrameShape(QFrame.Shape.StyledPanel)
        theme_layout = QVBoxLayout(theme_frame)
        theme_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add theme header
        theme_header = BoldText("Theme")
        theme_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme_header.setFixedHeight(30)  # Set fixed height
        font = theme_header.font()
        font.setPointSize(10)  # Set fixed font size
        theme_header.setFont(font)
        theme_layout.addWidget(theme_header)

        # Theme slider setup
        self.theme_slider = QSlider(Qt.Orientation.Horizontal)
        self.theme_slider.setFixedWidth(200)  # Set fixed width
        self.theme_slider.setMinimum(0)
        self.theme_slider.setMaximum(100)
        self.theme_slider.setValue(self.settings.value("theme_value", 100))
        self.theme_slider.valueChanged.connect(self.update_theme)

        # Icon layout for theme slider
        self.lightbulb_icon = QLabel("💡")
        self.lightbulb_icon.setStyleSheet("font-size: 20px;")
        self.sunglasses_icon = QLabel("🕶️")
        self.sunglasses_icon.setStyleSheet("font-size: 20px;")
        theme_slider_layout = QVBoxLayout()
        theme_slider_icons_layout = QHBoxLayout()
        theme_slider_icons_layout.addWidget(self.lightbulb_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        theme_slider_icons_layout.addWidget(self.theme_slider)
        theme_slider_icons_layout.addWidget(self.sunglasses_icon, alignment=Qt.AlignmentFlag.AlignRight)
        theme_slider_layout.addLayout(theme_slider_icons_layout)

        # Theme value label
        self.theme_value_label = QLabel()
        value_label_font = QFont()
        value_label_font.setPointSize(self.VALUE_LABEL_FONT_SIZE)
        self.theme_value_label.setFont(value_label_font)
        theme_slider_layout.addWidget(self.theme_value_label, alignment=Qt.AlignmentFlag.AlignCenter)

        theme_layout.addLayout(theme_slider_layout)
        return theme_frame
    #endregion

    # 📏 Construct scale section with inputs
    def _build_scale_section(self, main_widget):
        scale_frame = self._create_scale_frame()
        main_widget.layout().addWidget(scale_frame)

    # 🖼 Create scale container frame
    def _create_scale_frame(self):
        scale_frame = QFrame()
        scale_frame.setFrameShape(QFrame.Shape.StyledPanel)
        scale_layout = QVBoxLayout(scale_frame)
        scale_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add scale header
        scale_header = BoldText("Scale")
        scale_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scale_header.setFixedHeight(30)  # Set fixed height
        font = scale_header.font()
        font.setPointSize(10)  # Set fixed font size
        scale_header.setFont(font)
        scale_layout.addWidget(scale_header)

        # Fix slider width
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setFixedWidth(200)  # Set fixed width
        self.scale_slider.setMinimum(60)
        self.scale_slider.setMaximum(130)
        self.scale_slider.setValue(self.settings.value("scale_value", 100))
        self.scale_slider.valueChanged.connect(self.update_scale)

        # Icon layout for scale slider
        self.small_icon = QLabel("•")
        self.small_icon.setStyleSheet("font-size: 20px;")
        self.big_icon = QLabel("⬤")
        self.big_icon.setStyleSheet("font-size: 20px;")
        scale_slider_layout = QVBoxLayout()
        scale_slider_icons_layout = QHBoxLayout()
        scale_slider_icons_layout.addWidget(self.small_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        scale_slider_icons_layout.addWidget(self.scale_slider)
        scale_slider_icons_layout.addWidget(self.big_icon, alignment=Qt.AlignmentFlag.AlignRight)
        scale_slider_layout.addLayout(scale_slider_icons_layout)

        # Scale value label
        self.scale_value_label = QLabel()
        value_label_font = QFont()
        value_label_font.setPointSize(self.VALUE_LABEL_FONT_SIZE)
        self.scale_value_label.setFont(value_label_font)
        scale_slider_layout.addWidget(self.scale_value_label, alignment=Qt.AlignmentFlag.AlignCenter)

        scale_layout.addLayout(scale_slider_layout)
        return scale_frame

    # 🖋 Construct font selection section with inputs
    def _build_font_selection_section(self, main_widget):
        font_selection_frame = self._create_font_selection_frame()
        main_widget.layout().addWidget(font_selection_frame)

    # 🖼 Create font selection container frame
    def _create_font_selection_frame(self):
        font_selection_frame = QFrame()
        font_selection_frame.setFrameShape(QFrame.Shape.StyledPanel)
        font_selection_layout = QVBoxLayout(font_selection_frame)
        font_selection_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add font selection header
        font_selection_header = BoldText("Font")
        font_selection_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_selection_header.setFixedHeight(30)  # Set fixed height
        font = font_selection_header.font()
        font.setPointSize(10)  # Set fixed font size
        font_selection_header.setFont(font)
        font_selection_layout.addWidget(font_selection_header)

        # Font combo box setup
        self.font_combo = QFontComboBox()
        saved_font = self.settings.value("font_family", "Segoe UI")
        self.font_combo.setCurrentFont(QFont(saved_font))
        self.font_combo.currentFontChanged.connect(self.update_font)
        font_selection_layout.addWidget(self.font_combo)

        return font_selection_frame

    def _configure_layout(self, main_widget):
        # Close button to close the dialog
        ok_button = ScalableButton("Close")
        ok_button.clicked.connect(self.save_and_close)
        main_widget.layout().addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set standard size for the dialog
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.adjustSize()

    def apply_dynamic_scaling(self, value):
        if self.parent():
            self.parent().apply_dynamic_scaling(value)

    # This method now calls the parent method
    def apply_dynamic_theme(self, value):
        if not hasattr(self, 'color_palette'):
            print("color_palette is not initialized")
        if self.parent():
            self.parent().apply_dynamic_theme(value)

    # Call this function to apply scaling dynamically
    def update_main_window_scale(self):
        scale_value = self.scale_slider.value()

        # Call the parent method to apply dynamic scaling
        self.parent().update_main_window_scale(scale_value)

    # 🎯 Load and validate UI theme settings from storage
    def load_ui_settings(self):
        theme_value = self.settings.value("theme_value", 100)
        scale_value = self.settings.value("scale_value", 100)
        font_family = self.settings.value("font_family", "Segoe UI")

        # Set the loaded settings to the UI components
        self.theme_slider.setValue(theme_value)
        self.scale_slider.setValue(scale_value)
        self.font_combo.setCurrentFont(QFont(font_family))

        # Update value labels
        self.update_theme(theme_value)
        self.update_scale(scale_value)

        # Return the settings values
        return theme_value, scale_value, font_family

    # 🎨 Save current UI theme settings to storage
    def save_settings(self):
        self.settings.setValue("theme_value", self.theme_slider.value())
        self.settings.setValue("scale_value", self.scale_slider.value())
        self.settings.setValue("font_family", self.font_combo.currentFont().family())

    # 🔄 Update visual state of UI elements based on theme value
    def update_theme(self, value):
        # Update value label with Light/Dark/Custom
        if value == 0:
            self.theme_value_label.setText("Light")
        elif value == 100:
            self.theme_value_label.setText("Dark")
        else:
            self.theme_value_label.setText(str(value))
    
        # Calculate theme colors
        factor = value / 100
        current = {}
        for key in self.color_palette.light:
            light_color = QColor(self.color_palette.light[key])
            dark_color = QColor(self.color_palette.dark[key])
            r = int(light_color.red() * (1 - factor) + dark_color.red() * factor)
            g = int(light_color.green() * (1 - factor) + dark_color.green() * factor)
            b = int(light_color.blue() * (1 - factor) + dark_color.blue() * factor)
            current[key] = QColor(r, g, b)
    
        # Apply theme colors
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, current['window'])
        palette.setColor(QPalette.ColorRole.WindowText, current['text'])
        palette.setColor(QPalette.ColorRole.Button, current['button'])
        palette.setColor(QPalette.ColorRole.Base, current['input'])
        palette.setColor(QPalette.ColorRole.Text, current['text'])
    
        QApplication.instance().setPalette(palette)
        self.setPalette(palette)
    
        # Update icon colors
        icon_color = current['text'].name()
        self.lightbulb_icon.setStyleSheet(f"font-size: 20px; color: {icon_color};")
        self.sunglasses_icon.setStyleSheet(f"font-size: 20px; color: {icon_color};")
        self.small_icon.setStyleSheet(f"font-size: 20px; color: {icon_color};")
        self.big_icon.setStyleSheet(f"font-size: 20px; color: {icon_color};")
    
        # Update parent window
        if self.parent():
            try:
                # Update parent theme
                self.parent().apply_dynamic_theme(value)
                self.parent().update_button_colors(value)
                
                # Update table theme
                if hasattr(self.parent(), 'results_table'):
                    self.parent().apply_theme_to_table(self.parent().results_table, palette)
                
                # Update table delegate
                if hasattr(self.parent(), 'table') and hasattr(self.parent().table, 'itemDelegate'):
                    delegate = self.parent().table.itemDelegate()
                    if hasattr(delegate, 'set_theme_value'):
                        delegate.set_theme_value(value)
                        
                # Force table update
                if hasattr(self.parent(), 'results_table'):
                    self.parent().results_table.viewport().update()
            except Exception as e:
                print(f"Error updating theme: {e}")
    
        self.adjustSize()

    # 📏 Ensure dialog maintains minimum required dimensions
    def _ensure_minimum_size(self):
        # Get minimum size needed for all content
        hint = self.sizeHint()
        # Add small padding to prevent cramping
        min_width = hint.width() + 20
        min_height = hint.height() + 5
        # Apply minimum size
        self.setMinimumSize(min_width, min_height)
        # Resize to fit if current size is smaller
        if self.width() < min_width or self.height() < min_height:
            self.resize(min_width, min_height)

    # 📏 Update scale value display and apply changes
    def update_scale(self, value):
        # Update value label
        if value == 100:
            self.scale_value_label.setText("Base")
        else:
            self.scale_value_label.setText(str(value))
    
        scale_factor = value / 100.0
        
        # Update application font
        font = QApplication.font()
        font.setPointSize(int(10 * scale_factor))
        QApplication.setFont(font)
    
        # Save the scale value
        self.settings.setValue("scale_value", value)
    
        if self.parent():
            try:
                # Update parent window size
                self.parent().adjustSize()
                content_size = self.parent().sizeHint()
                min_width = int(content_size.width() * scale_factor)
                min_height = int(content_size.height() * scale_factor)

                # Set minimum sizes to prevent resizing smaller than content
                self.parent().setMinimumSize(min_width, min_height)

                # If current size is smaller than minimum, resize to fit
                if self.parent().width() < min_width or self.parent().height() < min_height:
                    self.parent().resize(min_width, min_height)     
                
                # Update all buttons in parent
                for button in self.parent().findChildren(ScalableButton):
                    button.set_scale_factor(scale_factor)
                
                # Update all buttons in settings dialog
                for button in self.findChildren(ScalableButton):
                    button.set_scale_factor(scale_factor)
                # Update table delegate with scaling
                if hasattr(self.parent(), 'results_table'):
                    table = self.parent().results_table
                    delegate = table.itemDelegate()
                    if delegate:
                        delegate.set_scale_factor(scale_factor)
                    table.viewport().update()

                    # Update header font size
                    header = table.horizontalHeader()
                    header_font = header.font()
                    header_font.setPointSize(int(10 * scale_factor))
                    header.setFont(header_font)
                    header.setStyleSheet(f"QHeaderView::section {{ font-size: {int(10 * scale_factor)}pt; }}")

                    # Ensure minimum table dimensions
                    table_width = table.horizontalHeader().length()
                    table_height = (
                        table.verticalHeader().length() + 
                        table.horizontalHeader().height()
                    )
                    table.setMinimumWidth(table_width)
                    table.setMinimumHeight(table_height)
                    self.parent()._refresh_table()

                # Update table delegate
                if hasattr(self.parent(), 'table') and hasattr(self.parent().table, 'itemDelegate'):
                    self.parent().table.itemDelegate().set_scale_factor(scale_factor)
                
                # Update changelog delegate if exists
                if hasattr(self.parent(), 'changelog_dialog') and hasattr(self.parent().changelog_dialog, 'item_delegate'):
                    self.parent().changelog_dialog.item_delegate.set_scale_factor(scale_factor)
                
                # Update input fields
                for input_field in [self.parent().rate_input, self.parent().profit_input] + list(self.parent().price_inputs.values()):
                    input_field.set_scale_factor(scale_factor)
                
                # Update calculate button
                self.parent().calc_button.set_scale_factor(scale_factor)
                
                # Force table refresh
                if hasattr(self.parent(), 'results_table'):
                    self.parent()._refresh_table()

                # Final adjustment pass
                self.parent().apply_dynamic_scaling(self.scale_slider.value())
                self.parent().adjustSize()


            except Exception as e:
                print(f"Error updating scale: {e}")
    
        self.adjustSize()

    # Apply settings and then close the dialog.
    def apply_settings(self):
        self.settings.setValue("theme_value", self.theme_slider.value())
        self.settings.setValue("scale_value", self.scale_slider.value())
        self.settings.setValue("font_family", self.font_combo.currentFont().family())
        self.accept()

    # 🖋️ Update font selection and apply changes
    def update_font(self, font):
        self.settings.setValue("font_family", font.family())
        QApplication.instance().setFont(font)
        if self.parent():
            self.parent().apply_dynamic_font(font)

    # Override closeEvent to simulate Close button press when the window is closed.
    def closeEvent(self, event):
        self.save_and_close()
        # Notify main window about scale change (if needed)
        if self.parent():
            self.parent().apply_dynamic_scaling(self.scale_slider.value())
        event.accept()

    # 💾 Save settings and close dialog
    def save_and_close(self):
        self.apply_settings()  # Save settings before closing
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        settings.setValue("settings_dialog_x", self.x())
        settings.setValue("settings_dialog_y", self.y())
        # Notify main window about scale change (if needed)
        if self.parent():
            self.parent().apply_dynamic_scaling(self.scale_slider.value())
        self.accept()  # Close the dialog

    def showEvent(self, event):
        super().showEvent(event)
        self.adjust_size()
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        dialog_x = settings.value("settings_dialog_x", None)
        dialog_y = settings.value("settings_dialog_y", None)
        if dialog_x is not None and dialog_y is not None:
            self.move(int(dialog_x), int(dialog_y))
        else:
            parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
            dialog_width = self.width()
            dialog_height = self.height()
            dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
            dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
            self.move(dialog_x, dialog_y)

    # 🔄 Update dialog size based on screen dimensions
    def adjust_size(self):
        try:
            # Get the active screen size
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # Calculate maximum allowed dimensions based on screen size
            max_height = int(screen_height * self.SETTINGSDIALOG_SCREEN_HEIGHT_PERCENT)
            max_width = int(screen_width * self.SETTINGSDIALOG_SCREEN_WIDTH_PERCENT)

            # Adjust the dialog size
            self.setFixedHeight(min(self.sizeHint().height(), max_height))  # Enforce max height
            self.setFixedWidth(min(self.sizeHint().width(), max_width))     # Enforce max width
        except Exception as e:
            print(f"Error adjusting size: {e}")  # Debug print
#endregion

#region 📜 Changelog Dialog
# 📜 Dialog displaying version history and changes
class ChangelogDialog(QDialog):
    CHANGELOGDIALOG_SCREEN_HEIGHT_PERCENT = 0.8  # 80% of screen height
    CHANGELOGDIALOG_SCREEN_WIDTH_PERCENT = 0.5   # 50% of screen width
    
    PADDING_HEIGHT = 45  # Padding for height adjustment
    PADDING_WIDTH = 140  # Padding for width adjustment

    # Height adjustment percentages for different sections
    YEAR_HEIGHT_ADJUSTMENT_PERCENT = 1.6
    MONTH_HEIGHT_ADJUSTMENT_PERCENT = 1.4
    ENTRY_LIST_HEIGHT_ADJUSTMENT_PERCENT = 1
    ENTRY_HEIGHT_ADJUSTMENT_PERCENT = 0.95

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Changelog")
        self._setup_ui()

        # Set the scale factor for the item delegate
        if parent:
            scale_factor = parent.scale_factor
            self.item_delegate.set_scale_factor(scale_factor)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)  # Space between elements

        # Create changelog tree widget
        self.changelog_tree = QTreeWidget()
        self.changelog_tree.setHeaderHidden(True)
        self.changelog_tree.itemExpanded.connect(self.adjust_size)
        self.changelog_tree.itemCollapsed.connect(self.adjust_size)

        # Apply custom item delegate
        self.item_delegate = ChangelogItemDelegate(self)
        self.changelog_tree.setItemDelegate(self.item_delegate)

        layout.addWidget(self.changelog_tree)

        # Parse and populate changelog entries
        self._populate_changelog_tree()

        # Close button
        ok_button = QPushButton("Close")
        ok_button.clicked.connect(self.save_and_close)
        ok_button.setMinimumWidth(100)
        ok_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Configure dialog sizing
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.adjust_size()

    # 🌳 Organize and display changelog entries in tree
    def _populate_changelog_tree(self):
        changelog_entries = self._parse_changelog_text()
        organized_entries = {}

        for version, changes in changelog_entries.items():
            year, month, day, hour = version.split('_')[1:5]
            month_name = datetime.strptime(month, "%m").strftime("%B")
            if year not in organized_entries:
                organized_entries[year] = {}
            if month_name not in organized_entries[year]:
                organized_entries[year][month_name] = []
            organized_entries[year][month_name].append((version, changes))

        # Count top-level entries to determine if we should auto-expand
        year_count = len(organized_entries)

        for year, months in organized_entries.items():
            year_item = QTreeWidgetItem([year])
            self.changelog_tree.addTopLevelItem(year_item)
            month_count = len(months)

            # Auto-expand if only one year
            if year_count == 1:
                year_item.setExpanded(True)

            for month_name, entries in months.items():
                month_item = QTreeWidgetItem([month_name])
                year_item.addChild(month_item)

                # Auto-expand if only one month
                if month_count == 1:
                    month_item.setExpanded(True)

                for version, changes in entries:
                    version_title = changes[0]  # Use the first line as the title
                    version_item = QTreeWidgetItem([version_title])
                    month_item.addChild(version_item)

                    for change in changes[1:]:  # Skip the first line
                        change_item = QTreeWidgetItem([change.strip()])
                        version_item.addChild(change_item)

    # 📝 Parse changelog text into structured format
    def _parse_changelog_text(self):
        changelog_entries = {}
        for name, value in globals().items():
            if name.startswith("CHANGELOG_"):
                changelog_entries[name] = value.strip().split('\n')
        return changelog_entries

    # 📏 Calculate height for year items in tree
    def _calculate_year_height(self, year_item):
        height = self.changelog_tree.sizeHintForRow(0) * self.YEAR_HEIGHT_ADJUSTMENT_PERCENT
        if year_item.isExpanded():
            for i in range(year_item.childCount()):
                month_item = year_item.child(i)
                height += self._calculate_month_height(month_item)
        return height

    # 📏 Calculate height for month items in tree
    def _calculate_month_height(self, month_item):
        height = self.changelog_tree.sizeHintForRow(0) * self.MONTH_HEIGHT_ADJUSTMENT_PERCENT
        if month_item.isExpanded():
            for i in range(month_item.childCount()):
                entry_item = month_item.child(i)
                height += self._calculate_entry_list_height(entry_item)
        return height

    # 📏 Calculate height for entry list items
    def _calculate_entry_list_height(self, entry_item):
        height = self.changelog_tree.sizeHintForRow(0) * self.ENTRY_LIST_HEIGHT_ADJUSTMENT_PERCENT
        if entry_item.isExpanded():
            for i in range(entry_item.childCount()):
                change_item = entry_item.child(i)
                height += self._calculate_entry_height(change_item)
        return height

    # 📏 Calculate height for individual entries
    def _calculate_entry_height(self, change_item):
        num_rows = self._get_number_of_rows(change_item)
        return self.changelog_tree.sizeHintForRow(0) * self.ENTRY_HEIGHT_ADJUSTMENT_PERCENT * num_rows

    # 🔢 Get number of rows for an item
    def _get_number_of_rows(self, item):
        if item.childCount() == 0:
            return 1
        return item.childCount()

    # 📏 Calculate width needed for item display
    def _calculate_item_width(self, item):
        index = self.changelog_tree.indexFromItem(item)
        option = QStyleOptionViewItem()
        size = self.item_delegate.sizeHint(option, index)
        width = size.width()

        if item.isExpanded():
            for i in range(item.childCount()):
                width = max(width, self._calculate_item_width(item.child(i)))
        return width

    # 🔄 Update dialog size based on screen dimensions
    def adjust_size(self):
        try:
            # Get the active screen size
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
    
            # Calculate maximum allowed dimensions based on screen size
            max_height = int(screen_height * self.CHANGELOGDIALOG_SCREEN_HEIGHT_PERCENT)
            max_width = int(screen_width * self.CHANGELOGDIALOG_SCREEN_WIDTH_PERCENT)
    
            # Calculate the required height based on the expanded state
            total_height = self.changelog_tree.header().height()
            for i in range(self.changelog_tree.topLevelItemCount()):
                item = self.changelog_tree.topLevelItem(i)
                total_height += self._calculate_year_height(item)
    
            # Calculate the required width based on the visible content
            total_width = 0
            for i in range(self.changelog_tree.topLevelItemCount()):
                item = self.changelog_tree.topLevelItem(i)
                total_width = max(total_width, self._calculate_item_width(item))
    
            # Ensure the dialog does not resize beyond the main window's boundaries
            total_height = min(int(total_height + self.PADDING_HEIGHT), max_height)
            total_width = min(total_width + self.PADDING_WIDTH, max_width)
    
            # Adjust the dialog size
            self.setFixedHeight(total_height)  # Enforce max height
            self.setFixedWidth(total_width)    # Enforce max width
        except Exception as e:
            print(f"Error adjusting size: {e}")  # Debug print

    # Override closeEvent to simulate Close button press when the window is closed.
    def closeEvent(self, event):
        self.save_and_close()
        event.accept()

    # 💾 Save settings and close dialog
    def save_and_close(self):
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        settings.setValue("changelog_dialog_x", self.x())
        settings.setValue("changelog_dialog_y", self.y())
        self._save_tree_state()
        self.accept()  # Close the dialog

    def showEvent(self, event):
        super().showEvent(event)
        self.adjust_size()
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        dialog_x = settings.value("changelog_dialog_x", None)
        dialog_y = settings.value("changelog_dialog_y", None)
        if dialog_x is not None and dialog_y is not None:
            self.move(int(dialog_x), int(dialog_y))
        else:
            parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
            dialog_width = self.width()
            dialog_height = self.height()
            dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
            dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
            self.move(dialog_x, dialog_y)

        # Restore tree state
        self._restore_tree_state()

    # Save the expanded state of the tree
    def _save_tree_state(self):
        expanded_state = {}
        for i in range(self.changelog_tree.topLevelItemCount()):
            item = self.changelog_tree.topLevelItem(i)
            expanded_state[item.text(0)] = self._get_expanded_state(item)
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        settings.setValue("changelog_tree_state", expanded_state)

    # Get expanded state for individual item
    def _get_expanded_state(self, item):
        state = {'expanded': item.isExpanded(), 'children': {}}
        for i in range(item.childCount()):
            child = item.child(i)
            state['children'][child.text(0)] = self._get_expanded_state(child)
        return state

    # Restore the expanded state of the tree
    def _restore_tree_state(self):
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        expanded_state = settings.value("changelog_tree_state", {})
        for i in range(self.changelog_tree.topLevelItemCount()):
            item = self.changelog_tree.topLevelItem(i)
            self._set_expanded_state(item, expanded_state.get(item.text(0), {}))

    # Set expanded state for individual item
    def _set_expanded_state(self, item, state):
        item.setExpanded(state.get('expanded', False))
        for i in range(item.childCount()):
            child = item.child(i)
            self._set_expanded_state(child, state.get('children', {}).get(child.text(0), {}))

class ChangelogItemDelegate(QStyledItemDelegate):
    BASE_FONT_SIZE = 8  # Base font size in points

    # Font size increments as percentages of the base font size
    YEAR_FONT_SIZE_PERCENT = 1.25 # 120% of base font size
    MONTH_FONT_SIZE_PERCENT = 1.20  # 115% of base font size
    ENTRY_FONT_SIZE_PERCENT = 1.15  # 110% of base font size
    DASH_FONT_SIZE_PERCENT = 1.10  # 105% of base font size
    STAR_FONT_SIZE_PERCENT = 1.0  # 100% of base font size

    # Font bold settings
    YEAR_FONT_BOLD = True
    MONTH_FONT_BOLD = True
    ENTRY_FONT_BOLD = True
    DASH_FONT_BOLD = True
    STAR_FONT_BOLD = False

    # Row height adjustment percentages
    YEAR_HEIGHT_PERCENT = 1.2
    MONTH_HEIGHT_PERCENT = 1.2
    ENTRY_HEIGHT_PERCENT = 1.2
    DASH_ROW_HEIGHT_PERCENT = 1.2
    STAR_ROW_HEIGHT_PERCENT = 1.2

    # Indentation constants
    STAR_INDENT_SPACES = 8 # Number of spaces before '*' entries

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = parent
        self.scale_factor = 1.0

    def set_scale_factor(self, factor: float):
        self.scale_factor = factor
        self._trigger_repaint()

    def _trigger_repaint(self):
        try:
            if hasattr(self.parent(), 'viewport'):
                self.parent().viewport().update()
            elif hasattr(self.parent(), 'update'):
                self.parent().update()
        except Exception:
            pass

    def paint(self, painter, option, index):
        level = self._item_level(index)
        text = index.data(Qt.ItemDataRole.DisplayRole)
        font = QFont(option.font)
        painter.save()

        # Adjust font size based on level and scale factor
        if level == 0:  # Year
            font.setPointSizeF(self.BASE_FONT_SIZE * self.YEAR_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.YEAR_FONT_BOLD)
        elif level == 1:  # Month
            font.setPointSizeF(self.BASE_FONT_SIZE * self.MONTH_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.MONTH_FONT_BOLD)
        elif level == 2:  # Entry (version title)
            font.setPointSizeF(self.BASE_FONT_SIZE * self.ENTRY_FONT_SIZE_PERCENT * self.scale_factor)
            font.setBold(self.ENTRY_FONT_BOLD)
        elif level == 3:  # Dash or Star rows
            text = text.strip()
            if text.startswith('-'):
                font.setPointSizeF(self.BASE_FONT_SIZE * self.DASH_FONT_SIZE_PERCENT * self.scale_factor)
                font.setBold(self.DASH_FONT_BOLD)
            elif text.startswith('*'):
                font.setPointSizeF(self.BASE_FONT_SIZE * self.STAR_FONT_SIZE_PERCENT * self.scale_factor)
                font.setBold(self.STAR_FONT_BOLD)
            else:
                font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)
        else:
            font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)

        # Handle special formatting for '*' character
        if level == 3 and text.startswith('*'):
            text = ' ' * self.STAR_INDENT_SPACES + text

        # Set adjusted font
        option.font = font
        painter.setFont(font)
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        level = self._item_level(index)
        font = QFont(option.font)

        # Calculate row height based on level and scale factor
        if level == 0:  # Year
            row_height_percent = self.YEAR_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.YEAR_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 1:  # Month
            row_height_percent = self.MONTH_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.MONTH_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 2:  # Entry (version title)
            row_height_percent = self.ENTRY_HEIGHT_PERCENT
            font.setPointSizeF(self.BASE_FONT_SIZE * self.ENTRY_FONT_SIZE_PERCENT * self.scale_factor)
        elif level == 3:
            text = index.data(Qt.ItemDataRole.DisplayRole).strip()
            if text.startswith('-'):
                row_height_percent = self.DASH_ROW_HEIGHT_PERCENT
                font.setPointSizeF(self.BASE_FONT_SIZE * self.DASH_FONT_SIZE_PERCENT * self.scale_factor)
                font.setBold(self.DASH_FONT_BOLD)
            elif text.startswith('*'):
                row_height_percent = self.STAR_ROW_HEIGHT_PERCENT
                font.setPointSizeF(self.BASE_FONT_SIZE * self.STAR_FONT_SIZE_PERCENT * self.scale_factor)
            else:
                row_height_percent = 1.0
                font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)
        else:
            row_height_percent = 1.0
            font.setPointSizeF(self.BASE_FONT_SIZE * self.scale_factor)

        # Update font metrics
        fm = QFontMetrics(font)
        size.setHeight(int(fm.height() * row_height_percent))
        size.setWidth(fm.horizontalAdvance(index.data(Qt.ItemDataRole.DisplayRole)))
        return size

    # 🎯 Get tree item nesting level
    def _item_level(self, index):
        level = 0
        parent = index.parent()
        while parent.isValid():
            level += 1
            parent = parent.parent()
        return level
#endregion

# 🧮 Main application window for WC merchant calculations
class MerchantCalculator(QMainWindow):
    #region 🚀 Initialization
    MAINWINDOW_SCREEN_HEIGHT_PERCENT = 0.8  # 80% of screen height
    MAINWINDOW_SCREEN_WIDTH_PERCENT = 0.5   # 50% of screen width

    # Responsible for setting up core application state and preparing UI components
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize settings before trying to access them
        self.settings = QSettings("or1n", "ArtaleWCMerchCalc")

        # Initialize the color_palette
        self.color_palette = DarkLightPalette()  # Ensure DarkLightPalette is defined
        
        theme_value = self.settings.value("theme_value", 100, type=int)
        scale_value = self.settings.value("scale_value", 100, type=int)
        font_family = self.settings.value("font_family", "Segoe UI")

        # Store scale factor
        self.scale_factor = scale_value / 100.0

        # 📊 State tracking dictionaries for price management
        self.price_enabled = {}  # Tracks enabled/disabled states for items
        self.price_inputs = {}   # Stores references to input fields

        # 📋 Item catalog initialization
        self.items = self._create_default_items()

        # 💾 Restore previous application state
        self.load_button_states()

        # 🎬 Finalize UI setup
        self.init_ui()

        # Apply settings in correct order
        app = QApplication.instance()
        font = QFont(font_family)
        font.setPointSize(int(10 * self.scale_factor))
        app.setFont(font)
        
        # Apply theme and scaling
        self.apply_dynamic_theme(theme_value)
        self.apply_dynamic_scaling(scale_value)

        # Center window after all sizing is done
        self._center_window()

    # 🪟 Prepare main window properties and positioning
    def _prepare_window(self):
        self._center_window()
        self._set_window_size_policy()
        self._set_window_title()

    def _center_window(self):
        screen = QApplication.primaryScreen()  # Retrieve the primary screen
        screen_geometry = screen.availableGeometry()  # Get available screen area
        screen_center = screen_geometry.center()  # Extract center point of screen

        window_geometry = self.frameGeometry()  # Capture current window geometry
        window_geometry.moveCenter(screen_center)  # Align window's center with screen center

        self.move(window_geometry.topLeft())  # Position window at calculated coordinates

        # Adjust size based on screen dimensions
        max_height = int(screen_geometry.height() * self.MAINWINDOW_SCREEN_HEIGHT_PERCENT)
        max_width = int(screen_geometry.width() * self.MAINWINDOW_SCREEN_WIDTH_PERCENT)
        self.setMaximumHeight(max_height)
        self.setMaximumWidth(max_width)

    def showEvent(self, event):
        super().showEvent(event)
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        dialog_x = settings.value("merchant_dialog_x", None)
        dialog_y = settings.value("merchant_dialog_y", None)
        if dialog_x is not None and dialog_y is not None:
            self.move(int(dialog_x), int(dialog_y))
        else:
            parent_geometry = self.parent().geometry() if self.parent() else QRect(0, 0, 800, 600)
            dialog_width = self.width()
            dialog_height = self.height()
            dialog_x = parent_geometry.x() + (parent_geometry.width() - dialog_width) // 2
            dialog_y = parent_geometry.y() + (parent_geometry.height() - dialog_height) // 2
            self.move(dialog_x, dialog_y)

    # ⚙️ Configures window to dynamically resize across different display contexts
    def _set_window_size_policy(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    # 🏷 Generates informative window title with app metadata
    def _set_window_title(self):
        # Construct comprehensive window title string using global constants
        self.setWindowTitle(f'{APP_NAME} {VERSION} - made by {CREATOR}')
  
    # 📦 Create primary container for UI components
    def _create_main_container(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        main_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(main_widget)
        return main_widget

        return main_widget
    #endregion

    #region 🎨 UI Configuration
    # 🎨 Orchestrates complete user interface initialization
    def init_ui(self):
        # 🏗 Orchestrate complete user interface initialization
        self._prepare_window()
        main_widget = self._create_main_container()
        
        # Construct UI sections in order
        self._build_header(main_widget)
        self._build_controls(main_widget)
        self._build_results(main_widget)
        self._build_bottom_buttons(main_widget)
        
        # Final configuration
        self._configure_layout(main_widget)
        self._setup_input_listeners()

        # Apply initial layout adjustments
        self.apply_initial_layout_adjustments()

    def apply_initial_layout_adjustments(self):
        # Adjust size to fit all UI elements
        self.adjustSize()
        self.setMinimumSize(self.sizeHint())

    # 📏 Configure layout stretching and sizing
    def _configure_layout(self, main_widget):
        layout = main_widget.layout()
        layout.setStretch(0, 0)  # Header (fixed)
        layout.setStretch(1, 0)  # Controls (fixed)
        layout.setStretch(2, 1)  # Results (expandable)
        layout.setStretch(3, 0)  # Buttons (fixed)

        # Set resizing policy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.adjustSize()

    # 🖼 Construct header with avatar, title, and version
    def _build_header(self, main_widget):
        header_widget = QWidget()
        header_widget.setObjectName("header_widget")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align to top

        # Create and add avatar
        avatar_label = self._create_avatar_label()
        header_layout.addWidget(avatar_label)
        header_layout.addWidget(avatar_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Create and add title
        title_label = self._create_title_label()
        header_layout.addWidget(title_label)
        header_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Create and add version
        version_label = self._create_version_label()
        header_layout.addWidget(version_label)
        header_layout.addWidget(version_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Set size policy for the header widget
        header_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        header_widget.setMinimumHeight(header_widget.sizeHint().height() +10)

        # Add header to main layout
        main_widget.layout().addWidget(header_widget)

    def _create_avatar_label(self):
        avatar_path = os.path.join(os.path.dirname(__file__), "images", "avatar.png")
        avatar_image = QPixmap(avatar_path)
        self.avatar_label = QLabel()
        self.avatar_label.setPixmap(avatar_image)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return self.avatar_label

    def set_avatar_scale_factor(self, scale_factor):
        avatar_path = os.path.join(os.path.dirname(__file__), "images", "avatar.png")
        avatar_image = QPixmap(avatar_path)
        scaled_image = avatar_image.scaled(
            int(avatar_image.width() * scale_factor),
            int(avatar_image.height() * scale_factor),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.avatar_label.setPixmap(scaled_image)

    # 📝 Create application title label
    def _create_title_label(self):
        title_label = QLabel(f'<b><font size="4">Artale WC Merch Calculator</font></b>')
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return title_label

    # 🏷 Create version label
    def _create_version_label(self):
        version_label = QLabel(f'<b><font size="2">v{version}</font></b>')
        version_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return version_label

    # 🎮 Construct controls section with inputs
    def _build_controls(self, main_widget):
        controls_frame = self._create_controls_frame()
        controls_frame.setObjectName("controls_frame")

        # Setup rate and profit inputs
        self._setup_rate_profit_inputs(controls_frame)

        # Setup item price inputs
        self._setup_item_price_inputs(controls_frame)

        # Add calculate button
        self._add_calculate_button(controls_frame)

        # Set size policy for the controls frame
        controls_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        controls_frame.setMinimumHeight(controls_frame.sizeHint().height() +10)

        main_widget.layout().addWidget(controls_frame)

    # 🖼 Create controls container frame
    def _create_controls_frame(self):
        controls_frame = QFrame()
        controls_frame.setFrameShape(QFrame.Shape.StyledPanel)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Add controls header
        controls_header = BoldText("Controls")
        controls_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(controls_header)

        return controls_frame

    # 🔢 Create rate and profit input section
    def _setup_rate_profit_inputs(self, controls_frame):
        rate_widget, profit_widget = self._create_rate_profit_widgets()
        
        # Combine rate and profit inputs
        combined_layout = QHBoxLayout()
        combined_layout.addStretch()
        combined_layout.addWidget(rate_widget)
        combined_layout.addWidget(profit_widget)
        combined_layout.addStretch()

        controls_frame.layout().addLayout(combined_layout)

    # 💰 Create individual widgets for rate and profit inputs
    def _create_rate_profit_widgets(self):
        # Rate widget setup
        rate_widget = QWidget()
        rate_layout = QVBoxLayout(rate_widget)
        rate_label = QLabel("Rate")
        rate_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        rate_input_layout = QHBoxLayout()
        self.rate_label = QLabel("1:")
        self.rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Rate input (4 digits wide)
        self.rate_input = ScalableLineEdit(num_digits=4)
        self.rate_input.setPlaceholderText("Rate")
        self.rate_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        rate_input_layout.addWidget(self.rate_label)
        rate_input_layout.addWidget(self.rate_input)

        rate_layout.addWidget(rate_label)
        rate_layout.addLayout(rate_input_layout)
        rate_layout.setSpacing(5)

        # Profit widget setup
        profit_widget = QWidget()
        profit_layout = QVBoxLayout(profit_widget)
        profit_label = QLabel("Profit")
        profit_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        profit_input_layout = QHBoxLayout()
        self.profit_label = QLabel("%")
        self.profit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Profit input (4 digits wide)
        self.profit_input = ScalableLineEdit(num_digits=4)
        self.profit_input.setPlaceholderText("Desired")
        self.profit_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.profit_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        profit_input_layout.addWidget(self.profit_input)
        profit_input_layout.addWidget(self.profit_label)

        profit_layout.addWidget(profit_label)
        profit_layout.addLayout(profit_input_layout)
        profit_layout.setSpacing(5)

        return rate_widget, profit_widget

    def _setup_item_price_inputs(self, controls_frame):
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setSpacing(30)  # Increased spacing between rows
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        self.price_inputs = {}
        self.price_enabled = {}
        self.toggle_buttons = {}

        # Group items into rows (max 4 items per row)
        rows = [self.items[i:i+4] for i in range(0, len(self.items), 4)]

        # Always use 4-item positions as reference
        reference_positions = [25, 37.5, 62.5, 75]

        for row_items in rows:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setSpacing(30)
            row_layout.setContentsMargins(0, 0, 0, 0)

            num_items = len(row_items)
            item_widgets = [self._create_item_input_widget(item) for item in row_items]
            
            # Select positions based on number of items
            if num_items == 1:
                positions = [50]  # Center position
            elif num_items == 2:
                positions = [reference_positions[1], reference_positions[2]]  # Align with 2nd and 3rd positions of 4
            elif num_items == 3:
                positions = [reference_positions[0], reference_positions[1], reference_positions[2]]
            else:  # 4 items
                positions = reference_positions

            # Add initial stretch
            row_layout.addStretch()

            for i, (item_widget, position) in enumerate(zip(item_widgets, positions)):
                # Create a container widget for proper alignment
                container = QWidget()
                container_layout = QHBoxLayout(container)
                container_layout.setContentsMargins(0, 0, 0, 0)
                container_layout.addWidget(item_widget)
                
                # Set stretch factors to position items
                left_stretch = position
                right_stretch = 100 - position
                
                if i == 0:  # First item
                    row_layout.addStretch(int(left_stretch))
                    row_layout.addWidget(container)
                    if num_items == 1:  # If only one item, add final stretch
                        row_layout.addStretch(int(right_stretch))
                else:
                    # Calculate space between items
                    prev_position = positions[i-1]
                    space_between = position - prev_position
                    row_layout.addStretch(int(space_between))
                    row_layout.addWidget(container)
                    
                    if i == len(positions) - 1:  # Last item
                        row_layout.addStretch(int(right_stretch))

            input_layout.addWidget(row_widget)

        controls_frame.layout().addWidget(input_widget)

    # 🎯 Creates and configures a custom input field widget
    def _create_item_input_widget(self, item):
        item_name = item.name
        item_widget = QWidget()
    
        # QVBoxLayout to stack the components vertically
        item_layout = QVBoxLayout(item_widget)
        item_layout.setSpacing(5)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
        # Create item name label
        item_label = QLabel(item_name)
        item_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        item_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    
        # Create a horizontal layout for toggle button and price input
        input_layout = QHBoxLayout()
        input_layout.setSpacing(0)
        input_layout.setContentsMargins(0, 0, 0, 0)
    
        # Item price input (8 digits wide)
        price_input = ScalableLineEdit(num_digits=8)
        price_input.setPlaceholderText("AH Price")
        price_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    
        # Create toggle button with matching height
        toggle_button = ScalableToggleButton("✓")
        toggle_button.setFixedHeight(price_input.sizeHint().height())  # Match input height
        toggle_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        toggle_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    
        # Add toggle button and price input to the horizontal layout
        input_layout.addWidget(toggle_button)
        input_layout.addWidget(price_input)
        input_layout.addStretch()
    
        # Add components to item layout
        item_layout.addWidget(item_label)
        item_layout.addLayout(input_layout)
    
        # Store references for later use
        self.price_inputs[item_name] = price_input
        self.toggle_buttons[item_name] = toggle_button
        self.price_enabled[item_name] = True
    
        # Connect toggle button to toggle function
        toggle_button.clicked.connect(
            lambda checked, button=toggle_button, input_field=price_input, name=item_name:
            self.toggle_state(button, input_field, name)
        )
        return item_widget

    # 🖱 Add calculate button to controls
    def _add_calculate_button(self, controls_frame):
        self.calc_button = ScalableButton("Calculate")
        self.calc_button.clicked.connect(lambda: self.calculate_table(save_history=True))
        self.calc_button.setMinimumWidth(120)
        self.calc_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        controls_frame.layout().addWidget(self.calc_button, alignment=Qt.AlignmentFlag.AlignCenter)

    # 📋 Create results section
    def _build_results(self, main_widget):
        results_frame = QFrame()
        results_frame.setFrameShape(QFrame.Shape.StyledPanel)
        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(10, 10, 10, 10)

        # Results header - set to fixed size to always stay at top
        results_header = BoldText("Results")
        results_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        results_header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        results_layout.addWidget(results_header)

        # Results content area
        self.results_content = QWidget()
        self.results_layout = QVBoxLayout(self.results_content)
        self.results_layout.setContentsMargins(0, 0, 0, 0)  # Remove internal margins
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align content to top

        results_layout.addWidget(self.results_content)

        # Add to main layout
        main_widget.layout().addWidget(results_frame)

    # 🔘 Create bottom buttons section
    def _build_bottom_buttons(self, main_widget):
        buttons_layout = QHBoxLayout()
        buttons_layout.setObjectName("bottom_buttons_layout")
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align to top
    
        # History button
        history_button = ScalableButton("History")
        history_button.clicked.connect(self.show_history)
        buttons_layout.addWidget(history_button)
    
        # Add stretch to push remaining buttons right
        buttons_layout.addStretch()
    
        # Right-side buttons
        contact_button = ScalableButton("Contact")
        contact_button.clicked.connect(self.show_contact)
        buttons_layout.addWidget(contact_button)
    
        settings_button = ScalableButton("Settings")
        settings_button.clicked.connect(self.show_settings)
        buttons_layout.addWidget(settings_button)
    
        changelog_button = ScalableButton("Changelog")
        changelog_button.clicked.connect(self.show_changelog)
        buttons_layout.addWidget(changelog_button)
    
        # Also set NoFocus for all the bottom buttons
        for button in [history_button, contact_button, settings_button, changelog_button]:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
        # Set size policy for the buttons layout
        buttons_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
    
        # Add to main layout
        main_widget.layout().addLayout(buttons_layout)

    # 🎮 Show history dialog and handle regeneration requests
    def show_history(self):
        history_dialog = HistoryDialog(self) # Pass self as the parent
        history_dialog.regenerate_requested.connect(self.regenerate_from_history)
        history_dialog.exec() # Show the dialog modally

    # 💬 Display contact information dialog
    def show_contact(self):
        contact_dialog = ContactDialog(self) # Pass self as the parent
        contact_dialog.exec() # Show the dialog modally
    
    # ⚙️ Show settings configuration dialog
    def show_settings(self):
        settings_dialog = SettingsDialog(self)  # Pass self as the parent
        settings_dialog.exec()  # Show the dialog modally    

    # 📜 Display changelog dialog with version history
    def show_changelog(self):
        # Retrieve the saved scale value
        scale_value = self.settings.value("scale_value", 100, type=int)
        scale_factor = scale_value / 100.0

        changelog_dialog = ChangelogDialog(self)  # Pass self as parent

        # Set the scale factor for the item delegate based on the saved scale value
        changelog_dialog.item_delegate.set_scale_factor(scale_factor)

        changelog_dialog.exec()  # Show the dialog modally

    # 🔗 Connect input listeners for saving settings
    def _setup_input_listeners(self):
        self.rate_input.textChanged.connect(self.save_rate_setting)
        self.profit_input.textChanged.connect(self.save_profit_setting)

        # Connect price input listeners
        for item in self.items:
            self.price_inputs[item.name].textChanged.connect(
                lambda state, item_name=item.name: self.save_price_setting(item_name)
            )

        # Load saved settings
        self.load_settings()
    #endregion

    #region 💾 State Management
    # 📥 Loads (previous setssion's) application-wide settings and input states
    def load_settings(self):
        # Load rate and profit input settings with default fallbacks
        saved_rate = self.settings.value("rate_input", DEFAULT_WC_RATE)  # Default rate if not saved
        saved_profit = self.settings.value("profit_input", DEFAULT_PROFIT)  # Default profit if not saved
        
        # Restore rate and profit input values
        self.rate_input.setText(str(saved_rate))
        self.profit_input.setText(str(saved_profit))
    
        # Restore individual item settings
        for item in self.items:
            item_name = item.name
            
            # Handle AH price restoration
            saved_price = self.settings.value(f"ah_price_{item_name}", "")
            if saved_price == "" or saved_price is None:
                self.price_inputs[item_name].setText("")
                self.price_inputs[item_name].setPlaceholderText("Price")
            else:
                self.price_inputs[item_name].setText(str(saved_price))
            
            # Restore item button state
            saved_button_state = self.settings.value(f"button_state_{item_name}", True, type=bool)
            self.price_enabled[item_name] = saved_button_state
            
            # Update toggle button appearance and input state
            button = self.toggle_buttons.get(item_name)
            if button:
                self._update_item_button_state(item_name, saved_button_state)
    
    # 💾 Loads saved button states for all items
    def load_button_states(self):
        for item_name in self.price_inputs.keys():
            state = self.settings.value(f"button_state_{item_name}", True, type=bool)
            self.price_enabled[item_name] = state
            self._update_item_button_state(item_name, state)

    # 📦 Provides consistent, predefined item catalog for application
    def _create_default_items(self):
        return [
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

    # Save the button state to settings.
    def save_button_state(self, item_name):
        self.settings.setValue(f"button_state_{item_name}", self.price_enabled[item_name])

    # 💾 Save individual setting with key-value pair
    def save_setting(self, key, value):
        if value is not None:
            self.settings.setValue(key, value)
        else:
            self.settings.setValue(key, "")

    # 💾 Save rate input value to settings
    def save_rate_setting(self):
        try:
            rate = int(self.rate_input.text())
            self.settings.setValue("rate_input", rate)
        except ValueError:
            pass  # Ignore invalid input

    # 💾 Save profit target value to settings
    def save_profit_setting(self):
        try:
            profit = float(self.profit_input.text())
            self.settings.setValue("profit_input", profit)
        except ValueError:
            pass  # Ignore invalid input

    # 💾 Save item price to persistent storage
    def save_price_setting(self, item_name):
        price_input = self.price_inputs[item_name]
        text = price_input.text().strip()
        # Only save if there's actually a value, otherwise save empty string
        if text:
            try:
                price = int(text)
                self.settings.setValue(f"ah_price_{item_name}", price)
            except ValueError:
                self.settings.setValue(f"ah_price_{item_name}", "")
        else:
            self.settings.setValue(f"ah_price_{item_name}", "")

    # 💾 Save calculation results to persistent storage
    def save_calculation_history(self, results):
        try:
            # Generate a unique timestamp for this calculation
            timestamp = datetime.now().strftime("%y.%m.%d.%H.%M.%S")
            
            # Prepare history data dictionary
            history_data = {
                'rate': self.rate_input.text() or "2600",
                'profit': self.profit_input.text() or "0",
                'prices': {},
                'enabled_items': {},
                'wc_rate': int(self.rate_input.text() or "2600"),
                'desired_profit': float(self.profit_input.text() or "0")
            }
            
            # Collect prices for all items
            for item in self.items:
                history_data['prices'][item.name] = self.price_inputs[item.name].text()
                history_data['enabled_items'][item.name] = self.price_inputs[item.name].isEnabled()
            
            # Serialize results list with more comprehensive item details
            history_data['results'] = [
                {
                    'name': r.item.name,
                    'wc_cost': r.item.wc_cost,
                    'pack_size': r.item.pack_size,
                    'ah_price': r.ah_price,
                    'wc_rate': r.wc_rate,
                    'buying_cost': r.buying_cost,
                    'sale_price': r.sale_price,
                    'ah_fee': r.ah_fee,
                    'net': r.net,
                    'profit_mesos': r.profit_mesos,
                    'profit_percent': r.profit_percent,
                    'is_profitable': r.is_profitable()
                } for r in results
            ]
            
            # Load existing history
            settings = QSettings("or1n", "ArtaleWCMerchCalc")
            history_json = settings.value("calculation_history", "{}")
    
            print(f"Existing history JSON loaded")  # Debug print
    
            try:
                current_history = json.loads(history_json)
            except json.JSONDecodeError:
                print("JSON decode error, initializing empty history")  # Debug print
                current_history = {}
            
            # Check if the current calculation is the same as the last saved entry
            if current_history:
                last_timestamp = sorted(current_history.keys())[-1]
                last_entry = current_history[last_timestamp]
                if history_data == last_entry:
                    print("Current calculation is the same as the last entry. Not saving a new entry.")
                    return
            
            # Add new entry
            current_history[timestamp] = history_data
            
            # Limit history to last 500 entries to prevent excessive storage
            if len(current_history) > 500:
                # Remove oldest entries
                sorted_timestamps = sorted(current_history.keys())
                for old_timestamp in sorted_timestamps[:-50]:
                    del current_history[old_timestamp]
        
            # Convert to JSON and save
            updated_history_json = json.dumps(current_history)
            settings.setValue("calculation_history", updated_history_json)
            
            print(f"Saved history entries: {len(current_history)}")  # Debug print
            print(f"Saved calculation to history JSON ")  # Debug print
    
        except Exception as e:
            print(f"Error saving calculation history: {e}")
        try:
            # Generate a unique timestamp for this calculation
            timestamp = datetime.now().strftime("%y.%m.%d.%H.%M.%S")
            
            # Prepare history data dictionary
            history_data = {
                'rate': self.rate_input.text() or "2600",
                'profit': self.profit_input.text() or "0",
                'prices': {},
                'enabled_items': {},
                'wc_rate': int(self.rate_input.text() or "2600"),
                'desired_profit': float(self.profit_input.text() or "0")
            }
            
            # Collect prices for all items
            for item in self.items:
                history_data['prices'][item.name] = self.price_inputs[item.name].text()
                history_data['enabled_items'][item.name] = self.price_inputs[item.name].isEnabled()
            
            # Serialize results list with more comprehensive item details
            history_data['results'] = [
                {
                    'name': r.item.name,
                    'wc_cost': r.item.wc_cost,
                    'pack_size': r.item.pack_size,
                    'ah_price': r.ah_price,
                    'wc_rate': r.wc_rate,
                    'buying_cost': r.buying_cost,
                    'sale_price': r.sale_price,
                    'ah_fee': r.ah_fee,
                    'net': r.net,
                    'profit_mesos': r.profit_mesos,
                    'profit_percent': r.profit_percent,
                    'is_profitable': r.is_profitable()
                } for r in results
            ]
            
            # Load existing history
            settings = QSettings("or1n", "ArtaleWCMerchCalc")
            history_json = settings.value("calculation_history", "{}")
    
            print(f"Existing history JSON loaded")  # Debug print
    
            try:
                current_history = json.loads(history_json)
            except json.JSONDecodeError:
                print("JSON decode error, initializing empty history")  # Debug print
                current_history = {}
            
            # Check if the current calculation is the same as the last saved entry
            if current_history:
                last_timestamp = sorted(current_history.keys())[-1]
                last_entry = current_history[last_timestamp]
                if history_data == last_entry:
                    print("Current calculation is the same as the last entry. Not saving a new entry.")
                    return
            
            # Add new entry
            current_history[timestamp] = history_data
            
            # Limit history to last 50 entries to prevent excessive storage
            if len(current_history) > 50:
                # Remove oldest entries
                sorted_timestamps = sorted(current_history.keys())
                for old_timestamp in sorted_timestamps[:-50]:
                    del current_history[old_timestamp]
        
            # Convert to JSON and save
            updated_history_json = json.dumps(current_history)
            settings.setValue("calculation_history", updated_history_json)
            
            print(f"Saved history entries: {len(current_history)}")  # Debug print
            print(f"Saved calculation to history JSON ")  # Debug print
    
        except Exception as e:
            print(f"Error saving calculation history: {e}")

    # 🔄 Recreate previous calculation from history data
    def regenerate_from_history(self, history_data):
        try:
            # Restore inputs
            self.rate_input.setText(str(history_data.get('rate', '2600')))
            self.profit_input.setText(str(history_data.get('profit', '0')))
            
            # Restore prices and enabled states
            for item_name, price in history_data.get('prices', {}).items():
                if item_name in self.price_inputs:
                    self.price_inputs[item_name].setText(str(price))
                    
                    # Restore enabled state, defaulting to True if not present
                    enabled = history_data.get('enabled_items', {}).get(item_name, True)
                    self.price_inputs[item_name].setEnabled(enabled)
            
            # Recreate ItemResult objects from saved data
            results = []
            for r in history_data.get('results', []):
                item = Item(r['name'], r['wc_cost'], r['pack_size'])
                result = ItemResult(item, r['ah_price'], r['wc_rate'])
                results.append(result)
            
            # Trigger calculation with the restored data
            if results:
                self.calculate_table(save_history=False)  # Prevent re-saving the same history

            # Setup and populate the table
            self.results_table = self._setup_table(
                results, history_data['wc_rate'], history_data.get('desired_profit')
            )
            self.results_table = self._populate_table(
                self.results_table, results, history_data.get('desired_profit')
            )
            self.results_table = self._configure_table(self.results_table)

            # Apply current theme
            palette = self.palette()
            self.apply_theme_to_table(self.results_table, palette)

            # Set delegate
            delegate = TableItemDelegate(self.results_table)
            self.results_table.setItemDelegate(delegate)

            # Clear existing results and add new table
            for i in reversed(range(self.results_layout.count())):
                widget = self.results_layout.itemAt(i).widget()
                if widget and isinstance(widget, QTableWidget):
                    widget.setParent(None)

            self.results_layout.addWidget(self.results_table)
            self.adjustSize()
        except Exception as e:
            print(f"Error regenerating calculation from history: {e}")
    #endregion

    #region 🔄 UI Updates
    # 🎨 Update all button colors based on current theme
    def update_button_colors(self, theme_value):
        # Calculate colors based on theme value
        factor = theme_value / 100
    
        # Interpolate between light and dark colors
        text_r = int(0 * (1 - factor) + 255 * factor)
        text_g = int(0 * (1 - factor) + 255 * factor)
        text_b = int(0 * (1 - factor) + 255 * factor)
    
        # Create button style
        button_style = (
            f"ScalableButton {{\n"
            f"    color: rgb({text_r}, {text_g}, {text_b});\n"
            f"}}\n"
            f"ScalableButton:hover {{\n"
            f"}}"
        )
    
        # Apply to all buttons
        for button in self.findChildren(ScalableButton):
            button.setStyleSheet(button_style)

         # Scale all ScalableToggleButton instances
        for toggle_button in self.findChildren(ScalableToggleButton):
            toggle_button.setStyleSheet(button_style)

    # 🔄 Update visual state of buttons based on saved data
    def update_button_state(self, item_name):
        button = self.findChild(ScalableButton, f"button_{item_name}")  # Find the button by its name or ID
        input_field = self.price_inputs.get(item_name)

        if self.price_enabled.get(item_name, True):  # Default to enabled if not saved
            button.setText("✓")
            input_field.setEnabled(True)
            input_field.setGraphicsEffect(None)  # Ensure no opacity effect
            button.setGraphicsEffect(None)  # Ensure no opacity effect
        else:
            button.setText("✘")
            input_field.setEnabled(False)
            self.set_opacity(input_field, 0.1)  # Apply opacity to the input field
            self.set_opacity(button, 0.1)  # Apply opacity to the button

    # 📏 Apply scaling to all UI elements dynamically
    def apply_dynamic_scaling(self, scale_value):
        scale_factor = scale_value / 100.0
    
        # Adjust font size dynamically
        font = QApplication.font()
        font.setPointSize(int(10 * scale_factor))  # Adjust the font size based on scale factor
        QApplication.setFont(font)
    
        # Scale all ScalableButton instances
        for button in self.findChildren(ScalableButton):
            button.set_scale_factor(scale_factor)
    
        # Scale all ScalableToggleButton instances
        for toggle_button in self.findChildren(ScalableToggleButton):
            toggle_button.set_scale_factor(scale_factor)
    
        # Scale all ScalableLineEdit instances
        for line_edit in self.findChildren(ScalableLineEdit):
            line_edit.set_scale_factor(scale_factor)
    
        # Scale avatar label
        self.set_avatar_scale_factor(scale_factor)
    
        # Scale rate_input and profit_input
        self.rate_input.set_scale_factor(scale_factor)
        self.profit_input.set_scale_factor(scale_factor)
    
        # Update ChangelogDialog if it exists
        if hasattr(self, 'changelog_dialog') and self.changelog_dialog:
            self.changelog_dialog.item_delegate.set_scale_factor(scale_factor)
            self.changelog_dialog.adjust_size()
    
        # Ensure that results_table exists before applying theme
        if hasattr(self, 'results_table') and self.results_table:
            self.update_table_fonts(self.results_table)
    
        # Update table if it exists
        if hasattr(self, 'results_table') and self.results_table:
            # Store current results
            current_results = []
            for row in range(self.results_table.rowCount()):
                row_data = []
                for col in range(self.results_table.columnCount()):
                    item = self.results_table.item(row, col)
                    if item:
                        row_data.append((item.text(), item.data(Qt.ItemDataRole.UserRole)))
                current_results.append(row_data)
    
            # Reconfigure table with new scale
            self._configure_table(self.results_table)
            
            # Update font size for all items
            for row in range(self.results_table.rowCount()):
                for col in range(self.results_table.columnCount()):
                    item = self.results_table.item(row, col)
                    if item:
                        font = item.font()
                        font.setPointSize(int(10 * scale_factor))
                        item.setFont(font)
    
            # Recalculate table dimensions
            self._configure_table(self.results_table)
            
            # Adjust window size
            table_width = self.results_table.minimumWidth()
            controls_width = self.centralWidget().sizeHint().width()
            required_width = max(table_width, controls_width) + 40
            
            self.setMinimumWidth(required_width)
            self.adjustSize()
    
        self.update_table_column_widths()
    
        # Adjust sizes of header, controls, results, and bottom buttons
        self._adjust_widget_sizes()
    
        # Adjust the height dynamically based on the content
        self._adjust_height()

    # Update theme dynamically based on theme slider.
    def apply_dynamic_theme(self, value):
        factor = value / 100
        current = {}

        for key in self.color_palette.light:
            light_color = QColor(self.color_palette.light[key])
            dark_color = QColor(self.color_palette.dark[key])

            r = int(light_color.red() * (1 - factor) + dark_color.red() * factor)
            g = int(light_color.green() * (1 - factor) + dark_color.green() * factor)
            b = int(light_color.blue() * (1 - factor) + dark_color.blue() * factor)

            current[key] = QColor(r, g, b)

        # Apply theme to main window
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, current['window'])
        palette.setColor(QPalette.ColorRole.WindowText, current['text'])
        palette.setColor(QPalette.ColorRole.Button, current['button'])
        palette.setColor(QPalette.ColorRole.Base, current['input'])
        palette.setColor(QPalette.ColorRole.Text, current['text'])

        QApplication.instance().setPalette(palette)
        self.setPalette(palette)

        # Update button colors in the main window
        if self.parent():
            self.parent().apply_dynamic_theme(value)

        # Ensure that results_table exists before applying theme
        if hasattr(self, 'results_table') and self.results_table:
            self.apply_theme_to_table(self.results_table, palette)

            # Update the font color of the table cells based on the new theme
            for row in range(self.results_table.rowCount()):
                for col in range(self.results_table.columnCount()):
                    item = self.results_table.item(row, col)
                    if item:
                        # Set the text color to the new theme color
                        item.setForeground(current['text'])

    # Update font dynamically based on font choice.
    def apply_dynamic_font(self, font):
        # Set the application font to the new font
        QApplication.setFont(font)
        
        # Update the font for all relevant UI elements
        self.update()
        self.adjustSize()

        if hasattr(self, 'results_table') and self.results_table:
            self.update_table_fonts(self.results_table)
            self._refresh_table()
    
        # Update the font for all ScalableButton instances
        for button in self.findChildren(ScalableButton):
            button.setFont(font)
    
        # Update the font for all ScalableToggleButton instances
        for toggle_button in self.findChildren(ScalableToggleButton):
            toggle_button.setFont(font)
    
        # Update the font for all ScalableLineEdit instances
        for line_edit in self.findChildren(ScalableLineEdit):
            line_edit.setFont(font)
    
    # Update fonts of all items in the given table based on the application font.
    def update_table_fonts(self, table):
        font = QApplication.font()
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setFont(font)  # Apply the updated font
    
    # 🔄 Refresh table display and update layout
    def _refresh_table(self):
        if hasattr(self, 'results_table') and self.results_table:
            self._configure_table(self.results_table)
            self.results_table.viewport().update()
            self.results_table.resizeColumnsToContents()
            self.results_table.resizeRowsToContents()
            self.adjustSize()  

    # 📏 Update column widths based on content
    def update_table_column_widths(self):
        if hasattr(self, 'results_table'):
            total_width = self.results_table.viewport().width()
            column_widths = [
                int(total_width * 0.10),  # Status column
                int(total_width * 0.20),  # Item Name
                int(total_width * 0.10),  # AH Price
                int(total_width * 0.10),  # Sale Price
                int(total_width * 0.10),  # Net
                int(total_width * 0.10),  # Cost
                int(total_width * 0.10),  # Profit Mesos
                int(total_width * 0.10),  # Profit %
                int(total_width * 0.10),  # Max Rate
            ]
            for i, width in enumerate(column_widths):
                self.results_table.setColumnWidth(i, width)

    def _adjust_widget_sizes(self):
        # Adjust header size
        header_widget = self.findChild(QWidget, "header_widget")
        if header_widget:
            header_widget.setMinimumHeight(header_widget.sizeHint().height() + 10)  # Add padding
    
        # Adjust controls size
        controls_frame = self.findChild(QFrame, "controls_frame")
        if controls_frame:
            controls_frame.setMinimumHeight(controls_frame.sizeHint().height() + 10)  # Add padding
    
        # Adjust results size
        results_frame = self.findChild(QFrame, "results_frame")
        if results_frame:
            results_frame.setMinimumHeight(results_frame.sizeHint().height() + 10)  # Add padding
    
        # Adjust bottom buttons size
        bottom_buttons_layout = self.findChild(QHBoxLayout, "bottom_buttons_layout")
        if bottom_buttons_layout:
            bottom_buttons_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
    
    def _adjust_height(self):
        # Calculate the total height required for the main widget
        total_height = 0
    
        header_widget = self.findChild(QWidget, "header_widget")
        if header_widget:
            total_height += header_widget.sizeHint().height() + 10  # Add padding
    
        controls_frame = self.findChild(QFrame, "controls_frame")
        if controls_frame:
            total_height += controls_frame.sizeHint().height() + 10  # Add padding
    
        results_frame = self.findChild(QFrame, "results_frame")
        if results_frame:
            total_height += results_frame.sizeHint().height() + 10  # Add padding
    
            # Include the height of the results table if it exists
            results_table = self.findChild(QTableWidget)
            if results_table:
                total_height += results_table.verticalHeader().length() + results_table.horizontalHeader().height() + 10  # Add padding
    
        bottom_buttons_layout = self.findChild(QHBoxLayout, "bottom_buttons_layout")
        if bottom_buttons_layout:
            # Calculate the height of the bottom buttons layout
            bottom_buttons_height = 0
            for i in range(bottom_buttons_layout.count()):
                item = bottom_buttons_layout.itemAt(i)
                if item.widget():
                    bottom_buttons_height += item.widget().sizeHint().height()
            total_height += bottom_buttons_height + 10  # Add padding
    
        # Set the minimum height to the calculated total height
        self.centralWidget().setMinimumHeight(total_height)
        self.adjustSize()

 
 
    #endregion

    #region 🔧 Utility Functions
    # 🔄 Updates individual item button state with visual feedback
    def _update_item_button_state(self, item_name, is_enabled):
        button = self.toggle_buttons.get(item_name)
        input_field = self.price_inputs.get(item_name)

        if button and input_field:
            self.toggle_widget_state(button, input_field, item_name, is_enabled)

    # Toggle the enabled state of the price input field.
    def toggle_state(self, button, input_field, item_name):
        # Determine the new state
        enabled = not input_field.isEnabled()
        self.toggle_widget_state(button, input_field, item_name, enabled)

    # Toggles the state of the input field and button with visual feedback
    def toggle_widget_state(self, button, input_field, item_name, enabled):
        button.setText("✓" if enabled else "✘")
        input_field.setEnabled(enabled)

        if enabled:
            input_field.setGraphicsEffect(None)
            button.setGraphicsEffect(None)
        else:
            self.set_opacity(input_field, 0.1)
            self.set_opacity(button, 0.1)

        # Update internal state
        self.price_enabled[item_name] = enabled
        self.save_button_state(item_name)

    # Toggle the enabled/disabled state of a price input box.
    def toggle_price_input(self, item_name):
        current_state = self.price_enabled[item_name]  # Get current state
        new_state = not current_state  # Flip the state

        self.price_enabled[item_name] = new_state  # Update the dictionary
        price_input = self.price_inputs[item_name]  # Get the input box

        if price_input:
            price_input.setEnabled(new_state)  # Enable/Disable the input box

        # Update toggle button text
        toggle_button = self.toggle_buttons[item_name]
        if toggle_button:
            toggle_button.setText("✓" if new_state else "✘")
 
    def set_opacity(self, widget, opacity):
        if widget is not None:  # Check if widget is valid
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(opacity)
            widget.setGraphicsEffect(effect)
    #endregion

    #region 🏗️ Calculation Table
    # Update the results section and resize the window.
    def update_results(self, new_results):
        # Clear existing results
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add new results to the results layout
        for result in new_results:
            result_label = QLabel(result)
            self.results_layout.addWidget(result_label)

        # Force a layout update
        self.results_layout.update()

        # Adjust the window size based on the updated layout
        self.adjustSize()

        # Optionally, you can also resize the window to a specific minimum size if necessary
        # self.resize(self.width(), self.minimumHeight())

    # 📊 Validate and process rate and profit inputs
    def _validate_inputs(self):
        try:
            wc_rate_text = self.rate_input.text().replace(",", "")
            wc_rate = int(wc_rate_text or "2600")
            
            desired_profit_text = self.profit_input.text().replace(",", "")
            desired_profit = float(desired_profit_text) if desired_profit_text else None

            return wc_rate, desired_profit
        except ValueError:
            return None, None

    # 📋 Gather calculation results for all enabled items
    def _collect_item_results(self, wc_rate):
        results = []
        for item in self.items:
            if not self.price_inputs[item.name].isEnabled():
                continue  
            try:
                ah_price_text = self.price_inputs[item.name].text().replace(",", "")
                if ah_price_text:
                    ah_price = int(ah_price_text)
                    if ah_price > 0:
                        result = ItemResult(item, ah_price, wc_rate)
                        results.append(result)
            except ValueError:
                continue
        
        return results

    # 📊 Setup table structure and headers
    def _setup_table(self, results, wc_rate, desired_profit):
        table = QTableWidget()
        table.setColumnCount(8 if desired_profit is None else 9)
        table.setRowCount(len(results))

        table.setSortingEnabled(False)
        table.verticalHeader().setVisible(False)

        headers = [" ☺", " Item", f"1:{wc_rate} ", "Sell ", "Fee ", "Net ", "% ", "Profit "]
        if desired_profit is not None:
            headers.append(f"@{desired_profit}% ")
        table.setHorizontalHeaderLabels(headers)

        self.update_table_column_widths()

        return table

    # 🎨 Apply theme colors to table elements
    def apply_theme_to_table(self, table, palette):
        COMMON_STYLES = "background: transparent; border: none; padding: 0;"
        table.setStyleSheet(
            f"QTableWidget {{ {COMMON_STYLES} gridline-color: transparent; }}"
            f"QTableWidget::item {{ {COMMON_STYLES} }}"
            f"QHeaderView::section {{ {COMMON_STYLES} }}"
        )

        # Configure header
        header = table.horizontalHeader()

        header.setAutoFillBackground(True)
        header.setPalette(QPalette(QColor(0, 0, 0, 0)))  # Transparent background
        header.setSectionsClickable(False)
        header.setSectionsMovable(False)

        # Configure header alignments
        for col in range(table.columnCount()):
            header_item = table.horizontalHeaderItem(col)
            if header_item:
                if col < 2:
                    header_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
                else:
                    header_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)

        # Apply color to items
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setForeground(palette.color(QPalette.ColorRole.Text))

        # Apply color to header
        header.setStyleSheet(f"""
            QHeaderView::section {{ 
                color: {palette.color(QPalette.ColorRole.Text).name()}; 
                background: transparent;
            }}
        """)

            # Update the table font color based on the theme
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setForeground(palette.color(QPalette.ColorRole.Text))

    # ⚙️ Configure table behavior and appearance
    def _configure_table(self, table):
        table.setSortingEnabled(False)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
        # Adjust column sizing to content
        header = table.horizontalHeader()
    
        # Use QPalette to set transparent background for the header
        header.setAutoFillBackground(True)  # Enable background filling
        header.setPalette(QPalette(QColor(0, 0, 0, 0)))  # Transparent background
    
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # Calculate necessary width for the first column (status)
        table.resizeColumnToContents(0)
        status_column_width = table.columnWidth(0) - 80
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setMinimumSectionSize(status_column_width)

        # Second column (name) resize to contents
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        
        # Calculate minimum size for each column based on content
        total_width = status_column_width  # Start with the width of the first column
        for col in range(2, table.columnCount()):
            table.resizeColumnToContents(col)
            min_size = table.columnWidth(col)
            if col == 3:  # Add extra width for the sale_price column
                min_size += 10
            if col == 4:  # Add extra width for the sale_price column
                min_size += 35
            elif col == 6:  # Add extra width for the net column
                min_size += 5
            elif col == 7:  # Remove width for the profit_percent column
                min_size -= 20
            elif col == 8:  # Remove width for the max_rate column
                min_size -= 60
            header.setMinimumSectionSize(min_size)
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
            total_width += min_size

        # Add widths of the first two columns
        total_width += table.columnWidth(1)
    
        # Adjust height to show all rows
        row_height = table.rowHeight(0)
        header_height = table.horizontalHeader().height()
        total_height = row_height * table.rowCount() + header_height
        table.setFixedHeight(total_height)
    
        # Adjust width to show all columns
        table.setMinimumWidth(total_width)
    
        return table

    # 📝 Populate table with calculation results
    def _populate_table(self, table, results, desired_profit):
        for row_idx, result in enumerate(results):
            table_items = self._create_table_items(result, desired_profit)
            for col, item in enumerate(table_items):
                table.setItem(row_idx, col, item)

        self._resize_columns_to_fit_content(table)
        return table

    # 📏 Adjust column widths to fit content
    def _resize_columns_to_fit_content(self, table):
        font = QApplication.font()
        scale_factor = self.scale_factor

        for col in range(table.columnCount()):
            max_width = 0
            for row in range(table.rowCount()):
                item = table.item(row, col)
                if item:
                    item.setFont(font)
                    item_width = table.fontMetrics().horizontalAdvance(item.text()) * scale_factor
                    max_width = max(max_width, item_width)
            table.setColumnWidth(col, int(max_width))

    # ✨ Create styled table items for results display
    def _create_table_items(self, result, desired_profit):
        items = [
            self._create_status_item(result),
            self._create_name_item(result),
            self._create_numeric_item(f"{result.buying_cost:,}", result.is_profitable()),
            self._create_numeric_item(f"{result.sale_price:,}", result.is_profitable()),
            self._create_numeric_item(f"{result.ah_fee:,}", result.is_profitable()),
            self._create_numeric_item(f"{result.net:,}", result.is_profitable()),
            self._create_numeric_item(f"{result.profit_percent:.1f}", result.is_profitable()),
            self._create_numeric_item(f"{result.profit_mesos:,}", result.is_profitable())
        ]

        if desired_profit:
            max_rate_item = self._create_max_rate_item(result, desired_profit)
            items.append(max_rate_item)

        return items

    # ✓ Create status indicator item for table
    def _create_status_item(self, result):
        status_item = QTableWidgetItem("✓" if result.is_profitable() else "✘")
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        status_item.setData(Qt.ItemDataRole.UserRole, result.is_profitable())
        return status_item

    # 📝 Create item name cell for table
    def _create_name_item(self, result):
        name_item = QTableWidgetItem(result.item.name)
        name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        name_item.setData(Qt.ItemDataRole.UserRole, result.is_profitable())
        return name_item

    # 🔢 Create numeric value cell for table
    def _create_numeric_item(self, text, is_profitable=True):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        item.setData(Qt.ItemDataRole.UserRole, is_profitable)
        return item

    # 📊 Create maximum rate cell for table
    def _create_max_rate_item(self, result, desired_profit):
        max_rate_value = result.calculate_max_rate(desired_profit)
        max_rate_item = QTableWidgetItem(f"1: {max_rate_value:,}")
        max_rate_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        max_rate_item.setData(Qt.ItemDataRole.UserRole, result.is_profitable())
        return max_rate_item
 
    def calculate_table(self, save_history=True):
        # Validate inputs
        wc_rate, desired_profit = self._validate_inputs()
        if wc_rate is None:
            return
    
        # Collect and sort results
        results = self._collect_item_results(wc_rate)
        if not results:
            return
        results.sort(key=lambda x: x.profit_percent, reverse=True)
    
        # Save history if requested
        if save_history:
            self.save_calculation_history(results)

        # Check the current table height and retract it from the minimum height
        previous_table_height = 0
        if hasattr(self, 'results_table') and self.results_table:
            previous_table_height = self.results_table.height()
        elif hasattr(self, 'results_frame') and self.results_frame:
            previous_table_height = self.results_frame.height()

        self.results_table = self._setup_table(results, wc_rate, desired_profit)
        self.results_table = self._populate_table(self.results_table, results, desired_profit)
        self.results_table = self._configure_table(self.results_table)
    
        palette = self.palette()
        self.apply_theme_to_table(self.results_table, palette)
    
        delegate = TableItemDelegate(self.results_table)
        self.results_table.setItemDelegate(delegate)
    
        # Clear existing results content
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget and isinstance(widget, QTableWidget):
                widget.setParent(None)
    
        self.results_layout.addWidget(self.results_table)
    
        # Calculate the required height for the table
        table_height = self.results_table.verticalHeader().length() + self.results_table.horizontalHeader().height()
        self.results_table.setFixedHeight(table_height)

        # Resize window
        table_width = self.results_table.horizontalHeader().length() + 40
        self.setMinimumWidth(table_width)
        self.setMinimumHeight(self.height() + table_height - previous_table_height)
        self.resize(table_width, self.height() + table_height - previous_table_height)
        self.adjustSize()

        # Adjust the height dynamically based on the content
        self._adjust_height()

    #endregion

    def closeEvent(self, event):
        settings = QSettings("or1n", "ArtaleWCMerchCalc")
        settings.setValue("merchant_dialog_x", self.x())
        settings.setValue("merchant_dialog_y", self.y())
        super().closeEvent(event)


#region main (Entry Point)
# 🎯 Initialize entry point of the application
def main():
    # Ensure QApplication is created first
    app = QApplication(sys.argv)
    
    # Set application icon for the taskbar
    icon_path = os.path.join(os.path.dirname(__file__), "images", "app_icon.png")  # Ensure the path is correct
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        print(f"Icon not found at {icon_path}")
    
    # Initialize the main window
    calculator = MerchantCalculator()

    # Set the main window icon to ensure it appears in the taskbar
    if os.path.exists(icon_path):
        calculator.setWindowIcon(QIcon(icon_path))

    calculator.show()
    calculator.apply_initial_layout_adjustments()  # Ensure size adjustments on start-up
    
    # Start the event loop
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
#endregion