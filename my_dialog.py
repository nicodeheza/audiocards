from aqt import qt, mw
from . import utils
from . import text_to_speech



class MyDialog(qt.QDialog):
    def __init__(self, browser, parent=None)->None:
        super().__init__(parent)
        self.selected_notes = browser.selectedNotes()
        
        config = mw.addonManager.getConfig(__name__)

        layout= qt.QVBoxLayout()
        layout.addWidget(qt.QLabel("Selected Notes: " + str(len(self.selected_notes))))

        self.grid_layout= qt.QGridLayout()

        common_fields = utils.getCommonFields(self.selected_notes)

        if len(common_fields) < 1:
            qt.QMessageBox.critical(mw, "Error", f"The chosen notes share no fields in common. Make sure you're not selecting two different note types")
        elif len(common_fields) == 1:
            qt.QMessageBox.critical(mw, "Error", f"The chosen notes only share a single field in common '{list(common_fields)[0]}'. You need an front and back field")
            
        self.front_combo = qt.QComboBox()
        self.back_combo = qt.QComboBox()
        
        last_front_field = config.get('last_front_field') or None
        last_back_field = config.get('last_back_field') or None
        front_field_index = 0
        back_field_index = 0
        i = 0
        for field in common_fields:
            if last_back_field is None:
                if "expression" == field.lower() or "sentence" == field.lower():
                    back_field_index = i
            elif field == last_back_field: 
                back_field_index = i
                
            if last_front_field is None:
                if "audio" == field.lower():
                    front_field_index= i
            elif field == last_front_field:
                front_field_index = i
            self.front_combo.addItem(field)
            self.back_combo.addItem(field)
            i+=1

        self.front_combo.setCurrentIndex(front_field_index)
        self.back_combo.setCurrentIndex(back_field_index)
        
        front_label= qt.QLabel("Card Front Field: ")
        front_tooltip= "The field that have the front of the card data."
        front_label.setToolTip(front_tooltip)
        
        back_label= qt.QLabel("Card Back Field: ")
        back_tooltip= "The field that have the back of the card data."
        back_label.setToolTip(back_tooltip)
        
        self.front_combo.setToolTip(front_tooltip)
        self.back_combo.setToolTip(back_tooltip)
        
        self.grid_layout.addWidget(front_label, 0,0)
        self.grid_layout.addWidget(self.front_combo, 0,1)
        self.grid_layout.addWidget(back_label, 0,2)
        self.grid_layout.addWidget(self.back_combo, 0,3)
        
        self.front_lang_combo = qt.QComboBox()
        self.back_lang_combo = qt.QComboBox()
        
        languages= text_to_speech.getLanguages()
        front_lang_index = 0
        back_lang_index = 0
        last_front_lang_field = config.get('last_front_lang_field') or None
        last_back_lang_field = config.get('last_back_lang_field') or None
        
        for i, lang in enumerate(languages):
            if last_front_lang_field is None:
                front_lang_index = i
            elif lang == last_front_lang_field:
                front_lang_index = i
            
            if last_back_lang_field is None:
                back_lang_index = i
            elif lang == last_back_lang_field:
                back_lang_index = i
                
            self.front_lang_combo.addItem(lang)
            self.back_lang_combo.addItem(lang)
            
        self.front_lang_combo.setCurrentIndex(front_lang_index)
        self.back_lang_combo.setCurrentIndex(back_lang_index)
        
        front_lang_combo_label = qt.QLabel("Front language: ")
        back_lang_combo_label = qt.QLabel("Back language: ")

        self.grid_layout.addWidget(front_lang_combo_label, 1,0)
        self.grid_layout.addWidget(self.front_lang_combo, 1,1)
        self.grid_layout.addWidget(back_lang_combo_label, 1,2)
        self.grid_layout.addWidget(self.back_lang_combo, 1,3)
        
        delay_label= qt.QLabel("Delay time in s: ") 
        self.delay_input = qt.QLineEdit()
        self.delay_input.setValidator(qt.QIntValidator(1, 999, self))
        delay = config.get("delay") or "0"
        self.delay_input.setText(delay)
        self.grid_layout.addWidget(delay_label, 2,0)
        self.grid_layout.addWidget(self.delay_input, 2,1)

        pattern_label= qt.QLabel("Audio pattern: ")
        self.pattern_input = qt.QLineEdit()
        self.pattern_input.setValidator(qt.QRegularExpressionValidator(qt.QRegularExpression("^[fb]*$"), self))
        pattern = config.get("pattern") or ""
        self.pattern_input.setText(pattern)
        self.grid_layout.addWidget(pattern_label, 2,2)
        self.grid_layout.addWidget(self.pattern_input, 2,3)
        
        self.add_bip_checkbox = qt.QCheckBox("Add a beep at the beginning")
        add_bip= config.get("add_bip") or "false"
        self.add_bip_checkbox.setChecked(True if add_bip == "true" else False)
        self.grid_layout.addWidget(self.add_bip_checkbox, 3,0)
        
        directory_label= qt.QLabel("Save directory: ")
        self.directory_input = qt.QLineEdit()
        self.directory_input.setFixedWidth(300)
        self.directory_button = qt.QPushButton("Choose Directory", self)
        directory= config.get("directory") or ""
        self.directory_input.setText(directory)
        self.directory_button.clicked.connect(self.onSelectInputBtnClicked)
        self.grid_layout.addWidget(directory_label, 4,0)
        self.grid_layout.addWidget(self.directory_input, 4,1)
        self.grid_layout.addWidget(self.directory_button, 4,2)

        self.accept_button= qt.QPushButton("Accept", self)
        self.accept_button.clicked.connect(self.onAccept)
        self.grid_layout.addWidget(self.accept_button, 5,0)

        layout.addLayout(self.grid_layout)
        self.setLayout(layout)
    
    def onSelectInputBtnClicked(self):
        directory= str(qt.QFileDialog.getExistingDirectory(self,"Select Directory"))
        self.directory_input.setText(directory)

    def onAccept(self):
        if self.pattern_input.text() == "" :
            qt.QMessageBox.critical(mw, "Error","Pattern field is required")
        elif self.directory_input.text() == "" :
            qt.QMessageBox.critical(mw, "Error", "Directory field is required")
        else:
            self.accept()


        

            



        
