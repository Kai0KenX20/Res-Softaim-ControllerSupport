import customtkinter
import os
from PIL import Image
import subprocess
from pyMeow import get_display_resolution
import inputs
from inputs import devices  # Updated import to use devices for detection

displayResolution = get_display_resolution()

def get_model_files():
    return [f for f in os.listdir() if f.endswith(('.engine', '.pt', '.onnx'))]

def create_model_selector(parent, row, column, model_files, default_model):
    customtkinter.CTkLabel(parent, text="Select Model").grid(row=row, column=column, pady=(10, 0), padx=(10, 0), sticky="w")
    model_selector = customtkinter.CTkComboBox(parent, values=model_files)
    model_selector.set(default_model)
    model_selector.grid(row=row, column=column + 1, pady=(10, 0), padx=(10, 10), sticky="w")
    return model_selector

def is_gamepad_connected():
    """Return True if a gamepad is connected, False otherwise."""
    return len(devices.gamepads) > 0

def create_keybind_selector(parent, row, column, activationKey):
    customtkinter.CTkLabel(parent, text="Select Activation Key").grid(row=row, column=column, pady=(10, 0), padx=(10, 0), sticky="w")
    key_list = CKEYS if is_gamepad_connected() else KKEYS
    keybind_selector = customtkinter.CTkComboBox(parent, values=key_list)
    keybind_selector.set(activationKey if activationKey in key_list else key_list[0])
    keybind_selector.grid(row=row, column=column + 1, pady=(10, 0), padx=(10, 10), sticky="w")
    return keybind_selector

def set_initial_values(entry_widget, config_value):
    entry_widget.insert(0, str(config_value))

def set_switch(switch, value):
    if hasattr(switch, 'get'):
        current_value = switch.get()
        if current_value != value:
            if value:
                switch.select()
            else:
                switch.deselect()

KKEYS = [
    "VK_LBUTTON", "VK_RBUTTON", "VK_CANCEL", "VK_MBUTTON", "VK_BACK", "VK_TAB", "VK_CLEAR", "VK_RETURN",
    "VK_SHIFT", "VK_CONTROL", "VK_MENU", "VK_PAUSE", "VK_CAPITAL", "VK_ESCAPE", "VK_SPACE", "VK_PRIOR",
    "VK_NEXT", "VK_END", "VK_HOME", "VK_LEFT", "VK_UP", "VK_RIGHT", "VK_DOWN", "VK_SELECT", "VK_PRINT",
    "VK_EXECUTE", "VK_SNAPSHOT", "VK_INSERT", "VK_DELETE", "VK_HELP", "VK_LWIN", "VK_RWIN", "VK_APPS",
    "VK_NUMPAD0", "VK_NUMPAD1", "VK_NUMPAD2", "VK_NUMPAD3", "VK_NUMPAD4", "VK_NUMPAD5", "VK_NUMPAD6",
    "VK_NUMPAD7", "VK_NUMPAD8", "VK_NUMPAD9", "VK_MULTIPLY", "VK_ADD", "VK_SEPARATOR", "VK_SUBTRACT",
    "VK_DECIMAL", "VK_DIVIDE", "VK_F1", "VK_F2", "VK_F3", "VK_F4", "VK_F5", "VK_F6", "VK_F7", "VK_F8",
    "VK_F9", "VK_F10", "VK_F11", "VK_F12", "VK_NUMLOCK", "VK_SCROLL",
]

CKEYS = [
    "BTN_SELECT", "BTN_START", "BTN_WEST", "BTN_NORTH", "BTN_EAST", "BTN_SOUTH", "BTN_THUMBR", "BTN_THUMBL",
    "BTN_TR", "BTN_TL", "ABS_Z", "ABS_RZ",
]

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        import config

        def run():
            print("Started Running 'main_tensorrt.py'")
            selected_model = model_selector.get()
            subprocess.Popen(['python', 'main_tensorrt.py', selected_model])
            exit()

        def save_settings():
            selected_model = model_selector.get()
            selected_activation_key = activationKey_entry1.get()
            use_mask_value = use_mask_switch.get() == 1
            auto_game_detection_value = auto_game_detection_switch.get() == 1
            cps_display_value = cps_display_switch.get() == 1
            visuals_value = visuals_switch.get() == 1
            realtime_overlay_value = realtime_overlay_switch.get() == 1
            center_of_screen_value = center_of_screen_switch.get() == 1
            random_body_part_value = random_body_part_switch.get() == 1
            triggerBot_value = triggerBot_switch.get() == 1
            showFOVCircle_value = showFOVCircle_switch.get() == 1
            showTracers_value = showTracers_switch.get() == 1
            showBoxes_value = showBoxes_switch.get() == 1
            toggle_aimbot_value = toggle_aimbot_switch.get() == 1
            showStatus_value = showStatus_switch.get() == 1

            with open('config.py', 'w') as config_file:
                config_file.write(f"screenShotHeight = {screen_shot_height_entry.get()}\n")
                config_file.write(f"screenShotWidth = {screen_shot_width_entry.get()}\n")
                config_file.write(f"jitterValueX = {jitterX_value_box.get()}\n")
                config_file.write(f"jitterValueY = {jitterY_value_box.get()}\n")
                config_file.write(f"jitterStrength = {jitterStrength_entry.get()}\n")
                config_file.write(f"useMask = {use_mask_value}\n")
                config_file.write(f"maskWidth = {mask_width_entry.get()}\n")
                config_file.write(f"maskHeight = {mask_height_entry.get()}\n")
                config_file.write(f"autoGameDetection = {auto_game_detection_value}\n")
                config_file.write(f"gameName = '{game_name_entry.get()}'\n")
                config_file.write(f"aaMovementAmp = {float(aa_movement_amp_entry.get())}\n")
                config_file.write(f"aaMovementAmpHipfire = {float(aa_movement_amp_hipfire_entry.get())}\n")
                config_file.write(f"confidence = {float(confidence_entry.get())}\n")
                config_file.write(f"fovCircleSize = {fov_circle_size_entry.get()}\n")
                config_file.write(f"aaQuitKey = '{aa_quit_key_entry.get()}'\n")
                config_file.write(f"aaTriggerBotKey = '{aa_trigger_bot_key_entry.get()}'\n")
                config_file.write(f"aaPauseKey = '{aa_pause_key_entry.get()}'\n")
                config_file.write(f"cpsDisplay = {cps_display_value}\n")
                config_file.write(f"visuals = {visuals_value}\n")
                config_file.write(f"realtimeOverlay = {realtime_overlay_value}\n")
                config_file.write(f"centerOfScreen = {center_of_screen_value}\n")
                config_file.write(f"onnxChoice = {int(onnx_choice_entry.get())}\n")
                config_file.write(f"selectedModel = '{selected_model}'\n")
                config_file.write(f"BodyPart = '{body_part_selector.get()}'\n")
                config_file.write(f"RandomBodyPart = {random_body_part_value}\n")
                config_file.write(f"showTracers = {showTracers_value}\n")
                config_file.write(f"showBoxes = {showBoxes_value}\n")
                config_file.write(f"triggerBot = {triggerBot_value}\n")
                config_file.write(f"triggerbot_actdistance = {triggerbot_actdistance_entry.get()}\n")
                config_file.write(f"showFOVCircle = {showFOVCircle_value}\n")
                config_file.write(f"overlayColor = '{overlayColor_entry.get()}'\n")
                config_file.write(f"toggleAimbot = {toggle_aimbot_value}\n")
                config_file.write(f"activationKey = '{selected_activation_key}'\n")
                config_file.write(f"showStatus = {showStatus_value}\n")
                print("Saved Settings")

        def create_setting_widget(parent, label, row, column, widget_type=customtkinter.CTkEntry, **options):
            customtkinter.CTkLabel(parent, text=label).grid(row=row, column=column, pady=(10, 0), padx=(10, 0), sticky="w")
            if widget_type == customtkinter.CTkCheckBox and 'text' not in options:
                options['text'] = ""
            widget = widget_type(parent, **options)
            widget.grid(row=row, column=column + 1, pady=(10, 0), padx=(10, 10), sticky="w")
            return widget

        themes_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "themes")
        customtkinter.set_default_color_theme(os.path.join(themes_path, "red.json"))

        self.title("Res Softaim Menu")
        self.iconbitmap("icon.ico")
        self.geometry("700x500")
        self.resizable(False, False)

        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon-removebg-preview.png")), size=(84, 84))
        self.screen_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "screen.png")), size=(20, 20))
        self.mask_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "mask.png")), size=(20, 20))
        self.gameaim_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "gameaim.png")), size=(20, 20))
        self.advanced_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "advanced.png")), size=(20, 20))
        self.hardware_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "hardware.png")), size=(20, 20))
        self.overlay_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "overlay.png")), size=(20, 20))

        # Create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(8, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.logo_image)
        self.navigation_frame_label.grid(row=7, column=0, padx=20, pady=20)
        self.run_button = create_setting_widget(self.navigation_frame, "", 8, 0, widget_type=customtkinter.CTkButton, text="Run Softaim", command=run)
        self.run_button.grid(row=8, column=0)
        self.save_button = create_setting_widget(self.navigation_frame, "", 9, 0, widget_type=customtkinter.CTkButton, text="Save Settings", command=save_settings)
        self.save_button.grid(row=9, column=0)
        self.display = create_setting_widget(self.navigation_frame, "", 10, 0, widget_type=customtkinter.CTkLabel, text=str(displayResolution[0]) + " x " + str(displayResolution[1]))
        self.display.grid(row=10, column=0)

        self.screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Screen",
                                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                     image=self.screen_image, anchor="w", command=self.screen_button_event)
        self.screen_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Mask",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.mask_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Game & Aim",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.gameaim_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Overlay",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.overlay_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Advanced",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.advanced_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.frame_6_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Hardware",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.hardware_image, anchor="w", command=self.frame_6_button_event)
        self.frame_6_button.grid(row=6, column=0, sticky="ew")

        # Create screen frame
        self.screen_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.screen_frame.grid_columnconfigure(0, weight=1)

        screen_shot_height_entry = create_setting_widget(self.screen_frame, "Screen Shot Height", 0, 0)
        screen_shot_width_entry = create_setting_widget(self.screen_frame, "Screen Shot Width", 1, 0)

        # Create mask frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        use_mask_switch = create_setting_widget(self.second_frame, "Use Mask", 0, 0, widget_type=customtkinter.CTkSwitch, text="")
        mask_width_entry = create_setting_widget(self.second_frame, "Mask Width", 1, 0)
        mask_height_entry = create_setting_widget(self.second_frame, "Mask Height", 2, 0)

        # Create game & aim frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(3, weight=1)

        game_name_entry = create_setting_widget(self.third_frame, "Game Name", 1, 0)
        aa_movement_amp_entry = create_setting_widget(self.third_frame, "Softaim ADS Sensitivity", 2, 0, widget_type=customtkinter.CTkEntry)
        aa_movement_amp_hipfire_entry = create_setting_widget(self.third_frame, "Softaim Hipfire Sensitivity", 3, 0, widget_type=customtkinter.CTkEntry)
        confidence_entry = create_setting_widget(self.third_frame, "Aim Confidence", 4, 0)
        fov_circle_size_entry = create_setting_widget(self.third_frame, "FOV Circle Size", 5, 0)
        body_part_selector = create_setting_widget(self.third_frame, "Body Part Selector", 6, 0, widget_type=customtkinter.CTkComboBox, values=["Head", "Neck", "Body", "Pelvis"])
        body_part_selector.set(config.BodyPart)
        jitterStrength_entry = create_setting_widget(self.third_frame, "Jitter Strength", 7, 0)
        jitterX_value_box = create_setting_widget(self.third_frame, "Jitter X Range", 8, 0)
        jitterY_value_box = create_setting_widget(self.third_frame, "Jitter Y Range", 9, 0)
        auto_game_detection_switch = create_setting_widget(self.third_frame, "Automatic Game Detection", 1, 2, widget_type=customtkinter.CTkSwitch, text="")
        random_body_part_switch = create_setting_widget(self.third_frame, "Randomized Body Part", 2, 2, widget_type=customtkinter.CTkSwitch, text="")
        triggerBot_switch = create_setting_widget(self.third_frame, "Trigger Bot", 3, 2, widget_type=customtkinter.CTkSwitch, text="")
        triggerbot_actdistance_entry = create_setting_widget(self.third_frame, "Activation Distance", 4, 2, widget_type=customtkinter.CTkEntry)
        center_of_screen_switch = create_setting_widget(self.third_frame, "Center of Screen Selection", 5, 2, widget_type=customtkinter.CTkSwitch, text="")

        # Create overlay frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure(0, weight=1)

        overlayColor_entry = create_setting_widget(self.fourth_frame, "Choose Overlay Color (HEX Format)", 1, 0, widget_type=customtkinter.CTkEntry)
        realtime_overlay_switch = create_setting_widget(self.fourth_frame, "Realtime Overlay", 2, 0, widget_type=customtkinter.CTkSwitch, text="")
        showFOVCircle_switch = create_setting_widget(self.fourth_frame, "Fov Circle", 3, 0, widget_type=customtkinter.CTkSwitch, text="")
        showTracers_switch = create_setting_widget(self.fourth_frame, "Tracers", 4, 0, widget_type=customtkinter.CTkSwitch, text="")
        showBoxes_switch = create_setting_widget(self.fourth_frame, "Boxes", 5, 0, widget_type=customtkinter.CTkSwitch, text="")
        showStatus_switch = create_setting_widget(self.fourth_frame, "On/Off Status", 6, 0, widget_type=customtkinter.CTkSwitch, text="")

        # Create advanced frame
        self.fifth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fifth_frame.grid_columnconfigure(0, weight=1)

        cps_display_switch = create_setting_widget(self.fifth_frame, "Display CPS", 1, 0, widget_type=customtkinter.CTkSwitch, text="")
        visuals_switch = create_setting_widget(self.fifth_frame, "Enable Softaim View", 2, 0, widget_type=customtkinter.CTkSwitch, text="")
        toggle_aimbot_switch = create_setting_widget(self.fifth_frame, "Toggle Aimbot", 3, 0, widget_type=customtkinter.CTkSwitch, text="")
        activationKey_entry1 = create_keybind_selector(self.fifth_frame, 4, 0, config.activationKey)
        aa_quit_key_entry = create_setting_widget(self.fifth_frame, "Softaim Quit Key", 5, 0)
        aa_pause_key_entry = create_setting_widget(self.fifth_frame, "Softaim Pause Key", 6, 0)
        aa_trigger_bot_key_entry = create_setting_widget(self.fifth_frame, "Trigger Bot Key", 7, 0)
        model_files = get_model_files()
        model_selector = create_model_selector(self.fifth_frame, 8, 0, model_files, config.selectedModel)

        # Create hardware frame
        self.sixth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.sixth_frame.grid_columnconfigure(0, weight=1)

        onnx_choice_entry = create_setting_widget(self.sixth_frame, "ONNX Choice (1-CPU, 2-AMD, 3-NVIDIA)", 1, 0)

        set_initial_values(screen_shot_height_entry, config.screenShotHeight)
        set_initial_values(screen_shot_width_entry, config.screenShotWidth)
        set_initial_values(mask_width_entry, config.maskWidth)
        set_initial_values(mask_height_entry, config.maskHeight)
        set_initial_values(game_name_entry, config.gameName)
        set_initial_values(aa_movement_amp_entry, config.aaMovementAmp)
        set_initial_values(aa_movement_amp_hipfire_entry, config.aaMovementAmpHipfire)
        set_initial_values(confidence_entry, config.confidence)
        set_initial_values(fov_circle_size_entry, config.fovCircleSize)
        set_initial_values(aa_quit_key_entry, config.aaQuitKey)
        set_initial_values(aa_trigger_bot_key_entry, config.aaTriggerBotKey)
        set_initial_values(aa_pause_key_entry, config.aaPauseKey)
        set_initial_values(onnx_choice_entry, config.onnxChoice)
        set_initial_values(jitterX_value_box, config.jitterValueX)
        set_initial_values(jitterY_value_box, config.jitterValueY)
        set_initial_values(triggerbot_actdistance_entry, config.triggerbot_actdistance)
        set_initial_values(overlayColor_entry, config.overlayColor)
        set_initial_values(jitterStrength_entry, config.jitterStrength)

        set_switch(use_mask_switch, config.useMask)
        set_switch(auto_game_detection_switch, config.autoGameDetection)
        set_switch(cps_display_switch, config.cpsDisplay)
        set_switch(visuals_switch, config.visuals)
        set_switch(center_of_screen_switch, config.centerOfScreen)
        set_switch(random_body_part_switch, config.RandomBodyPart)
        set_switch(triggerBot_switch, config.triggerBot)
        set_switch(realtime_overlay_switch, config.realtimeOverlay)
        set_switch(showFOVCircle_switch, config.showFOVCircle)
        set_switch(showTracers_switch, config.showTracers)
        set_switch(showBoxes_switch, config.showBoxes)
        set_switch(toggle_aimbot_switch, config.toggleAimbot)
        set_switch(showStatus_switch, config.showStatus)

        # Select default frame
        self.select_frame_by_name("frame_3")

    def select_frame_by_name(self, name):
        self.screen_button.configure(fg_color=("gray75", "gray25") if name == "screen" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")

        if name == "screen":
            self.screen_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.screen_frame.grid_forget()

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()

        if name == "frame_6":
            self.sixth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sixth_frame.grid_forget()

    def screen_button_event(self):
        self.select_frame_by_name("screen")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")

    def frame_6_button_event(self):
        self.select_frame_by_name("frame_6")

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        print(str(e))
        print("")
        input()
