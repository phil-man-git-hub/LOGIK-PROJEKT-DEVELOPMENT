    def load_environment_summary(self):
        try:
            # Retrieve values from relevant widgets
            projekt_flame_directory = self.get_widget_value("Projekt Flame Directory:")
            setups_directory = self.get_widget_value("Setups Directory:")
            media_cache_directory = self.get_widget_value("Media Cache:")

            software_version = self.combo_box_software_version.currentText()
            sanitized_sw_ver = sanitize_app_name(software_version)
            sanitized_version = sanitize_app_version(software_version)

            the_hostname = GetEnvironment.projekt_hostname() or 'N/A'

            # Calculate xml_project_dir, xml_setup_dir, and xml_media_dir
            xml_project_dir = projekt_flame_directory or f"/default/project/path/{sanitized_version}"
            xml_setup_dir = setups_directory or f"{xml_project_dir}/setups"
            xml_media_dir = media_cache_directory or f"{xml_project_dir}/media"

            # Update the environment summary dictionary
            env_data = {
                'Username': GetEnvironment.projekt_user_name() or 'N/A',
                'Group': GetEnvironment.projekt_primary_group() or 'N/A',
                'Hostname': the_hostname,
                'Software Version': software_version or 'N/A',
                'Projekt Flame Directory': xml_project_dir,
                'Setups Directory': xml_setup_dir,
                'Media Cache': xml_media_dir,
            }
            
            # Update environment summary text
            summary_text = '\n'.join(f"{key}: {value}" for key, value in env_data.items())
            self.environment_summary.setPlainText(summary_text)
        except Exception as e:
            print(f"Error loading environment data: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while loading environment data:\n{e}")

    def get_widget_value(self, label_text):
          """Retrieve the value of a widget based on its label text."""
          for i in range(self.layout.count()):
              item = self.layout.itemAt(i)
              if isinstance(item, QHBoxLayout):
                    label = item.itemAt(0).widget()
                    widget = item.itemAt(1).widget()
                    if isinstance(label, QLabel) and label.text() == label_text:
                        return widget.text() if hasattr(widget, "text") else ""
          return ""



def __init__(self):
    super().__init__()
    # Initialize layout
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    # Initialize projekt name (you might want to make it dynamic)
    self.the_projekt_name = "default_projekt_name"

    # Add widgets
    self.projekt_flame_directory = WidgetFlameProjektDirectory()
    self.setups_directory = WidgetFlameProjektSetupsDir()
    self.media_cache_directory = WidgetFlameProjektMediaCache()

    self.add_labeled_widget("Projekt Flame Directory:", self.projekt_flame_directory)
    self.add_labeled_widget("Setups Directory:", self.setups_directory)
    self.add_labeled_widget("Media Cache:", self.media_cache_directory)

    # Connect signals
    self.projekt_flame_directory.textChanged.connect(self.update_directory_widgets)

    # Set initial values
    self.update_directory_widgets()

def update_directory_widgets(self):
    """Automatically update Setups Directory and Media Cache based on Projekt Flame Directory."""
    base_dir = self.projekt_flame_directory.text().strip()
    if not base_dir:
        return

    setups_dir = os.path.join(base_dir, self.the_projekt_name, "setups")
    media_dir = os.path.join(base_dir, self.the_projekt_name, "media")

    self.setups_directory.setText(setups_dir)
    self.media_cache_directory.setText(media_dir)

def set_projekt_name(self, name):
    """Update the projekt name and refresh dependent directories."""
    self.the_projekt_name = name.strip()
    self.update_directory_widgets()

# C2 A9 32 30 32 35 53 54 52 45 4E 47 54 48 2D 49 4E 2D 4E 55 4D 42 45 52 53 #
