from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Slot
from loguru import logger
from pathlib import Path

from src.core.python.directories import ROOT_PATH

# Dynamically import QAction to handle potential import issues
try:
    from PySide6.QtWidgets import QAction
except ImportError:
    from PySide6.QtGui import QAction

def setup_system_tray(app, window):
    # Debugging logs to ensure tray initialization
    logger.debug("Initializing system tray...")
    if not QSystemTrayIcon.isSystemTrayAvailable():
        logger.error("System tray is not available on this system.")
        raise RuntimeError("System tray is not available on this system.")

    QApplication.setQuitOnLastWindowClosed(False)
    logger.debug("System tray is available and QApplication configured.")

    tray_icon = QSystemTrayIcon()

    # Use an absolute path for the tray icon
    icon_path = ROOT_PATH / "assets/images/logo.ico"
    tray_icon.setIcon(QIcon(str(icon_path)))

    if tray_icon.icon().isNull():
        logger.error(f"Tray icon failed to load. Check the icon path: {icon_path}")
        raise RuntimeError(f"Tray icon failed to load. Check the icon path: {icon_path}")

    logger.debug("Tray icon loaded successfully.")

    # Create tray menu
    tray_menu = QMenu()
    show_action = QAction("Show Window")
    exit_action = QAction("Exit")

    tray_menu.addAction(show_action)
    tray_menu.addAction(exit_action)

    tray_icon.setContextMenu(tray_menu)

    # Define actions
    @Slot()
    def show_window():
        if not window.isVisible():
            window.show()
        try:
            if hasattr(window, 'load'):
                qml_path = "./ui/qml/app.qml"  # Provide the QML file path
                window.load(qml_path)  # Ensure QML is loaded before activating the window
            window.show()  # Ensure the window is visible
            window.raise_()  # Bring the window to the front
        except (AttributeError, ValueError) as e:
            logger.error("Failed to activate window. Ensure QML is loaded and the path is correct.")
            logger.exception(e)

    @Slot()
    def exit_app():
        app.quit()

    show_action.triggered.connect(show_window)
    exit_action.triggered.connect(exit_app)

    # Connect tray icon activation to show the window
    tray_icon.activated.connect(lambda reason: show_window() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)

    # Handle window close event
    def on_close(event):
        event.ignore()
        window.hide()
        tray_icon.showMessage("App Minimized", "The application is minimized to the system tray.", QSystemTrayIcon.MessageIcon.Information, 2000)

    window.closeEvent = on_close

    tray_icon.show()
    return tray_icon
