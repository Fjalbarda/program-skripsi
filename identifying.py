import cv2
import tkinter as tk
from pathlib import Path
from tkinter import Label, filedialog
from ultralytics import YOLO
from PIL import Image, ImageTk
from ultralytics.yolo.utils.plotting import Annotator
from gtts import gTTS, gTTSError
from tkinter import messagebox
import pygame
import os

ASSETS_PATH = Path(__file__).resolve().parent / "assets/images"

model = YOLO('models/best4.pt')

window = tk.Tk()
window.title('Deteksi BISINDO')
window.config(bg='#023564')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = 800
window_height = 680

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f'{window_width}x{window_height}+{x}+{y}')

label_judul = tk.Label(window, fg='#FFF', width=540, font=(
    "Open Sans", 14, "bold"), text="Deteksi Bahasa Isyarat Indonesia (BISINDO)", bg='#023564')
label_judul.pack(ipadx=5, ipady=5, pady=10)

# Create a label for the initial image
initial_image_label = Label(window, bg='#023564')
initial_image_label.place(x=85, y=140, width=640, height=480)
original_image_path = ASSETS_PATH / "library-gambar-sign-language-bisindo-grid.jpg"


def reset_image():
    initial_image = Image.open(original_image_path)
    initial_image = initial_image.resize((640, 480), Image.Resampling.LANCZOS)
    initial_image_tk = ImageTk.PhotoImage(initial_image)
    initial_image_label.config(image=initial_image_tk)
    initial_image_label.image = initial_image_tk


def open_video():
    filetypes = [("Video files", ("*.mp4", "*.mov"))]

    video_path = filedialog.askopenfilename(title="Select Video", filetypes=filetypes)

    if video_path:
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = frame_width / frame_height

        if aspect_ratio > 1:
            output_width = 640
            output_height = int(output_width / aspect_ratio)
        else:
            output_height = 640
            output_width = int(output_height * aspect_ratio)

        while cap.isOpened():
            success, video_frame = cap.read()

            if success:
                resized_frame = cv2.resize(
                    video_frame, (output_width, output_height))

                results = model(resized_frame)

                annotated_frame = results[0].plot()

                cv2.imshow("Detection by Video", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()


previous_objects = []  # Definisikan variabel global sebelum fungsi perform_object_detection()

def perform_object_detection(image_frame):
    global previous_objects  # Tambahkan global keyword untuk menggunakan variabel global

    results = model.predict(image_frame, verbose=False)
    annotator = Annotator(image_frame)
    detected_objects = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            c = box.cls
            annotator.box_label(b, model.names[int(c)])
            detected_objects.append(model.names[int(c)])

    annotated_frame = annotator.result()
    annotated_image = results[0].plot()

    if detected_objects:
        if detected_objects != previous_objects:
            text_to_speech = ", ".join(detected_objects)

            try:
                tts = gTTS(text=text_to_speech, lang='id')
                tts.save("output.mp3")
                play_speech()
            except gTTSError:
                pass

        previous_objects = detected_objects

    return annotated_frame, annotated_image


def open_camera():
    reset_image()  # Reset gambar hasil prediksi sebelumnya sebelum memulai mode kamera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_rate = 30
    delay = int(1000 / frame_rate)

    while True:
        ret, camera_frame = cap.read()
        if not ret:
            break

        annotated_frame, annotated_image = perform_object_detection(camera_frame)

        cv2.imshow('Detection Realtime', annotated_image)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    reset_image()  # Menghapus gambar hasil prediksi setelah keluar dari mode kamera


def open_image():
    filetypes = [("JPEG Image", "*.jpg"), ("JPEG Image", "*.jpeg"), ("PNG Image", "*.png")]

    image_path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

    if image_path:
        image = cv2.imread(image_path)
        results = model(image)
        annotated_image = results[0].plot()
        resized_image = cv2.resize(annotated_image, (640, 480))
        pil_image = Image.fromarray(
            cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
        tk_image = ImageTk.PhotoImage(pil_image)

        # Update the initial image label with the selected image
        initial_image_label.config(image=tk_image)
        initial_image_label.image = tk_image

        detected_objects = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                c = box.cls
                detected_objects.append(model.names[int(c)])

        if detected_objects:
            text_to_speech = ", ".join(detected_objects)
        else:
            text_to_speech = "Objek tidak terdeteksi"

        tts = gTTS(text=text_to_speech, lang='id')
        tts.save("output.mp3")

        # Validation
        last_folder_name = os.path.basename(os.path.dirname(image_path))
        prediction = ", ".join(detected_objects)

        if prediction == last_folder_name:
            result_message = f"Hasil Identifikasi adalah {prediction}"
            result_icon = "info"
        else:
            result_message = f"Hasil Identifikasi adalah {prediction}"
            result_icon = "info"

        # Update the initial image label
        initial_image_label.update()

        # Play speech
        play_speech()

        # Show message box with prediction result
        messagebox.showinfo("Hasil Identifikasi Abjad BISINDO",
                            result_message, icon=result_icon)

        # Bind 'q' key to clear_image() function
        initial_image_label.bind('<KeyPress-q>', lambda event: clear_image())

        # Set focus to initial_image_label to capture key events
        initial_image_label.focus_set()


def clear_image():
    reset_image()


def play_speech():
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    os.remove("output.mp3")


frame = tk.Frame(window, bg='#F2B33D')

btn_video = tk.PhotoImage(file=ASSETS_PATH / "detect-by-video.png")
video_button = tk.Button(
    image=btn_video, borderwidth=0, highlightbackground="#023564", highlightthickness=30,
    command=open_video, relief="flat")
video_button.place(x=70, y=70, width=203, height=39)

btn_camera = tk.PhotoImage(file=ASSETS_PATH / "realtime-detection.png")
camera_button = tk.Button(
    image=btn_camera, borderwidth=0, highlightbackground="#023564", highlightthickness=30,
    command=open_camera, relief="flat")
camera_button.place(x=310, y=70, width=203, height=39)

btn_image = tk.PhotoImage(file=ASSETS_PATH / "detect-by-image.png")
image_button = tk.Button(
    image=btn_image, command=open_image, highlightbackground="#023564", highlightthickness=30)
image_button.place(x=540, y=70, width=203, height=39)

# Set initial image
reset_image()

copyright_text = tk.Label(
    text="© 2023 Fajri J. Albarda • 2011501588",
    bg="#023564", fg="white", justify="left",
    font=("Open Sans", 10, "italic"))
copyright_text.place(x=325.0, y=635.0)

window.resizable(False, False)
frame.pack(expand=True)
window.mainloop()
