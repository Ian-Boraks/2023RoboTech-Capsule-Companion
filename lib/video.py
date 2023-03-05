import tkinter as tk
import cv2
from PIL import Image, ImageTk

def create_fullscreen_window():
    # Initialize the tkinter window
    root = tk.Tk()

    # Set the window to fullscreen
    root.attributes("-fullscreen", True)

    # Hide the mouse cursor
    root.config(cursor="none")

    # Create a canvas in the window to display content
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack()

    # Set the video file path
    video_path = "wave.mp4"

    # Initialize the video capture object
    cap = cv2.VideoCapture(video_path)

    # Loop the video
    def loop_video():
        # Read a frame from the video
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            # Restart the video if the end is reached
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        # Convert the frame to RGB format and resize it to fit the canvas
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (root.winfo_screenwidth(), root.winfo_screenheight()))

        # Create a PIL image object from the frame
        image = Image.fromarray(frame)

        # Create a Tkinter-compatible photo image from the PIL image object
        photo = ImageTk.PhotoImage(image=image)

        # Display the photo on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        # Schedule the next frame update
        root.after(1, loop_video)

    # Start the video loop
    loop_video()

    # Return the tkinter window and canvas objects
    return root, canvas

if __name__ == "__main__":
    root, canvas = create_fullscreen_window()

    # Start the tkinter main loop
    root.mainloop()