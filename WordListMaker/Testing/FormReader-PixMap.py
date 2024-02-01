
#pdf_path = 'N3NoKatakanaShuffleRemoved-interactive.pdf'
#   output_folder_path = "output_images"

import time
import pygetwindow as gw
import pyautogui

def take_window_screenshot(window_title, file_path="window_screenshot.png"):
    # Get the specified window by title
    window = gw.getWindowsWithTitle(window_title)

    if not window:
        print(f"Window with title '{window_title}' not found.")
        return

    # Get the position and size of the window
    window = window[0]
    window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height

    # Activate the window (optional, but may be necessary on some systems)
    window.activate()
    time.sleep(1)
    # Take a screenshot of the specified window
    screenshot = pyautogui.screenshot(region=(window_x, window_y, window_width, window_height))

    # Save the screenshot to the specified file path
    screenshot.save(file_path)

    print(f"Screenshot of '{window_title}' saved to {file_path}")

if __name__ == "__main__":
    # Specify the title of the window you want to capture
    window_title = "N3NoKatakanaShuffleRemoved-interactive"#N3NoKatakanaShuffleRemoved-interactive - Google Chrome

    take_window_screenshot(window_title)



