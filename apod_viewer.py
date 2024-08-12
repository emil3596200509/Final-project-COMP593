from tkinter import *
import apod_desktop

# Initialize the image cache
apod_desktop.init_apod_cache()

# Create the GUI
root = Tk()
root.geometry('600x400')
root.title("NASA APOD Viewer")

# Create a frame to hold the image
image_frame = Frame(root, width=600, height=300)
image_frame.pack(pady=20)

# Create a label to display the image
image_label = Label(image_frame)
image_label.pack()

# Create a frame to hold the buttons
button_frame = Frame(root)
button_frame.pack(pady=20)

# Create a button to download and set the APOD image
def dd_and_set_apod_img():
    image_url = apod_desktop.get_apod_image_url()
    image_data = apod_desktop.download_image(image_url)
    if image_data:
        image_path = "apod_image.jpg"
        if apod_desktop.save_image_file(image_data, image_path):
            apod_desktop.set_desktop_background_image(image_path)
            image = PhotoImage(file=image_path)
            image_label.config(image=image)
            image_label.image = image
            print("APOD image downloaded and set successfully")
        else:
            print("Failed to save APOD image")
    else:
        print("Failed to download APOD image")

apod_button = Button(button_frame, text="Download and Set APOD Image", command=download_and_set_apod_image)
apod_button.pack(side=LEFT, padx=10)

# Create a button to quit the application
def quit_app():
    root.destroy()

quit_button = Button(button_frame, text="Quit", command=quit_app)
quit_button.pack(side=RIGHT, padx=10)

root.mainloop()