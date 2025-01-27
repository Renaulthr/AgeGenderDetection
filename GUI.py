# Importing necessary libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.image import thumbnail
import numpy as np

# Loading the Model
from keras.models import load_model
model = load_model('Age_Sex_Detection.keras')

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age & Gender Detection GUI')
top.configure(background='#CDCDCD')

#Initializing the Labels for Age & Sex!
label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
sign_image = Label(top)

# Defining Detect function which detects the age and gender of the person in image using the model.
def Detect(file_path):
    global label_packed
    from PIL import Image  # Ensure Image is correctly imported within this function

    # Open the image file using PILs Image class
    image = Image.open(file_path)

    # Resize the image to (48, 48) as required by the model
    image = image.resize((48, 48))  # Correct tuple format for resize

    # Convert image to numpy array for model processing
    image = np.array(image)

    # Ensure the image has the correct number of channels (RGB) for the model
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input image must have 3 channels (RGB).")

    # Normalize the image data and reshape to fit model input
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize values to range [0, 1]

    # Predict age and gender using the model
    predictions = model.predict(image)
    age = int(np.round(predictions[1][0]))
    sex = int(np.round(predictions[0][0]))

    # Map prediction results to readable text
    sex_f = ["Male", "Female"]
    print(f"Predicted Age is {age}")
    print(f"Predicted Gender is {sex_f[sex]}")

    # Update labels with the detected values
    label1.configure(foreground="#011638", text=f"Age: {age}")
    label2.configure(foreground="#011638", text=f"Gender: {sex_f[sex]}")


# Defining show_detect button func.
def show_Detect_Button(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, "bold"))
    Detect_b.place(relx=0.79, rely=0.46)

# Defining Upload Image Func.
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_Detect_Button(file_path)
    except:
        pass    

upload = Button(top, text="Upload An Image", command=upload_image, padx=10, pady=15)
upload.configure(background="#364156", foreground='white', font=('arial', 10, "bold"))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)

label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text="Age and Gender Detector", pady=20, font=('arial', 20, "bold"))
heading.configure(background='#CDCDCD', foreground="#364156")
heading.pack()
top.mainloop()