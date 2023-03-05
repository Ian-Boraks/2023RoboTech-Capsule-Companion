import cv2
import subprocess

def display_fullscreen_window():
    # Set the screen resolution to the MacBook's Retina display resolution
    subprocess.call(["/usr/bin/osascript", "-e", "tell application \"System Events\" to tell process \"Finder\" to set frontmost to true"])
    subprocess.call(["/usr/bin/osascript", "-e", "tell application \"System Events\" to keystroke \"j\" using {command down, shift down}"])
    subprocess.call(["/usr/bin/osascript", "-e", "tell application \"System Events\" to keystroke \"2\" using {shift down}"])
    subprocess.call(["/usr/bin/osascript", "-e", "tell application \"System Events\" to keystroke return"])

    # Load the video file
    video = cv2.VideoCapture('path/to/video/file')

    # Create a window and set it to fullscreen
    cv2.namedWindow('fullscreen', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('fullscreen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Loop through the frames and display them in the fullscreen window
    while True:
        ret, frame = video.read()
        if not ret:
            break
        cv2.imshow('fullscreen', frame)
        if cv2.waitKey(1) == ord('q'):  # Press 'q' to exit
            break

    # Release the video and destroy the window
    video.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    display_fullscreen_window()