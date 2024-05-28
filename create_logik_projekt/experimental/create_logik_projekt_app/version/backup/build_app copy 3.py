#!/usr/bin/env python3

'''
File Name:        build_app.py
'''

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel, QTextEdit
from PySide6.QtGui import QFont, QScreen
from define_popup_menus import popup_menu_definitions

def generate_template():
    print("Generate LOGIK-PROJEKT Template button clicked")
    # Add functionality to generate LOGIK-PROJEKT template here

def create_popup_menu(items, label_text):
    label = QLabel(label_text)
    label.setStyleSheet("color: #CCCCCC; font-weight: bold;")  # Slightly less than white

    popup_menu = QComboBox()
    popup_menu.setStyleSheet("background-color: #111111; color: white;")  # Darker than the background, text color white
    popup_menu.addItems(items)
    popup_menu.currentIndexChanged.connect(update_summary)  # Connect the signal to update summary when value changes
    
    return label, popup_menu

def update_summary():
    global proj_res, proj_res_h, proj_res_v, proj_aspect_ratio, proj_color_depth, proj_fcm, proj_color_science, default_start_frame
    
    try:
        selected_resolution = resolution_menu.currentText()
        proj_res_h, proj_res_v = selected_resolution.split(' x ')
        proj_res_h = int(proj_res_h.strip())  # Extract numeric part and convert to integer
        proj_res_v = int(proj_res_v.split()[0].strip())  # Extract numeric part and convert to integer

        proj_res = f"{proj_res_h} x {proj_res_v}"
        proj_aspect_ratio = float(proj_res_h) / float(proj_res_v)
    except ValueError:
        proj_res = "Invalid resolution"
        proj_aspect_ratio = "N/A"

    proj_color_depth = bit_depth_menu.currentText()
    proj_fcm = frame_rate_menu.currentText()
    proj_color_science = color_science_menu.currentText()
    default_start_frame = start_frame_menu.currentText()
    
    # Update summary text
    summary_textbox.clear()
    summary_textbox.append(f"Client Name:   {client_name_entry.text()}")
    summary_textbox.append(f"Campaign Name: {campaign_name_entry.text()}")
    summary_textbox.append(f"Resolution:    {proj_res}")
    summary_textbox.append(f"Aspect Ratio:  {proj_aspect_ratio}")
    summary_textbox.append(f"Color Depth:   {proj_color_depth}")
    summary_textbox.append(f"Frame Rate:    {proj_fcm}")
    summary_textbox.append(f"Color Science: {proj_color_science}")
    summary_textbox.append(f"Start Frame:   {default_start_frame}")

def build_app():
    global client_name_entry, campaign_name_entry, summary_textbox
    global resolution_menu, bit_depth_menu, frame_rate_menu, color_science_menu, start_frame_menu
    
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("LOGIK-PROJEKT")
    window.resize(640, 720)  # Increase the vertical size of the window

    # Set the background color to much darker grey
    window.setStyleSheet("background-color: #333333;")

    layout = QVBoxLayout()

    # Text Entry Boxes
    client_name_entry = QLineEdit()
    client_name_entry.setStyleSheet("background-color: #808080;")  # Set text entry box color to 50% grey
    client_name_entry.setPlaceholderText("Enter client name")
    client_name_entry.textChanged.connect(update_summary)  # Connect text change signal to update summary
    client_name_label = QLabel("Client Name:")
    client_name_label.setStyleSheet("color: #CCCCCC; font-weight: bold;")  # Slightly less than white
    layout.addWidget(client_name_label)
    layout.addWidget(client_name_entry)

    campaign_name_entry = QLineEdit()
    campaign_name_entry.setStyleSheet("background-color: #808080;")  # Set text entry box color to 50% grey
    campaign_name_entry.setPlaceholderText("Enter campaign name")
    campaign_name_entry.textChanged.connect(update_summary)  # Connect text change signal to update summary
    campaign_name_label = QLabel("Campaign Name:")
    campaign_name_label.setStyleSheet("color: #CCCCCC; font-weight: bold;")  # Slightly less than white
    layout.addWidget(campaign_name_label)
    layout.addWidget(campaign_name_entry)

    # Pop-Up Menus
    resolution_label, resolution_menu = create_popup_menu(popup_menu_definitions["Resolution"], "Resolution")
    layout.addWidget(resolution_label)
    layout.addWidget(resolution_menu)

    bit_depth_label, bit_depth_menu = create_popup_menu(popup_menu_definitions["Bit Depth"], "Bit Depth")
    layout.addWidget(bit_depth_label)
    layout.addWidget(bit_depth_menu)

    frame_rate_label, frame_rate_menu = create_popup_menu(popup_menu_definitions["Frame Rate"], "Frame Rate")
    layout.addWidget(frame_rate_label)
    layout.addWidget(frame_rate_menu)

    color_science_label, color_science_menu = create_popup_menu(popup_menu_definitions["Color Science"], "Color Science")
    layout.addWidget(color_science_label)
    layout.addWidget(color_science_menu)

    start_frame_label, start_frame_menu = create_popup_menu(popup_menu_definitions["Start Frame"], "Start Frame")
    layout.addWidget(start_frame_label)
    layout.addWidget(start_frame_menu)

    # Summary Text Box
    summary_label = QLabel("Projekt Summary:")
    summary_label.setStyleSheet("color: #CCCCCC; font-weight: bold;")  # Slightly less than white
    layout.addWidget(summary_label)

    summary_textbox = QTextEdit()
    summary_textbox.setStyleSheet("background-color: #555555; color: white;")  # Darker than the background, text color white
    summary_textbox.setFixedHeight(150)  # Set fixed height to avoid scrollbars
    summary_textbox.setReadOnly(True)  # Make the summary text box read-only
    layout.addWidget(summary_textbox)

    # Generate Template Button
    generate_button = QPushButton("Generate LOGIK-PROJEKT Template")
    generate_button.clicked.connect(generate_template)
    generate_button.setStyleSheet("color: white; font-weight: bold;")
    layout.addWidget(generate_button)

    # Cancel Button
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(window.close)  # Close the window when the Cancel button is clicked
    cancel_button.setStyleSheet("color: white; font-weight: bold;")
    layout.addWidget(cancel_button)

    window.setLayout(layout)

    # Get the geometry of the screen
    screen_geometry = app.primaryScreen().geometry()

    # Get the center position of the screen
    center_point = screen_geometry.center()

    # Calculate the top-left corner position of the window
    top_left_corner = center_point - window.rect().center()

    # Move the window to the calculated position
    window.move(top_left_corner)

    # Set the minimum font size for labels
    font = window.font()
    font.setFamily("Courier")  # Set the font family to a generic monospace font
    font.setPointSize(24)  # Set the minimum font size to 24 points
    window.setFont(font)

    # Call update_summary to populate the summary initially
    update_summary()

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    build_app()
