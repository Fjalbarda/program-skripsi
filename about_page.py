import tkinter as tk


def display_about_page():
    # Create the main window
    window = tk.Tk()
    window.title("Tentang Identifikasi Bahasa Isyarat Indonesia")
    window.geometry("600x400")
    window.config(bg="#4C1D95")  # Set the background color

    # Create a text widget to display the content
    # Set the text widget's background color and foreground color
    text_widget = tk.Text(window, wrap="word", bg="#EDE9FE", fg="black")
    text_widget.pack(fill="both", expand=True)

    # Configure the text widget's appearance
    text_widget.config(font=("Open Sans", 12), padx=10, pady=10)
    text_widget.tag_configure("title", font=("Open Sans", 16, "bold"))
    text_widget.tag_configure("content", font=("Open Sans", 14, "italic"))

    # Insert the content into the text widget
    text_widget.insert("end", "Tentang Aplikasi\n", "title")
    text_widget.insert("end", "\n")
    text_widget.insert(
        "end", "Aplikasi ini menggunakan algoritma algoritma MobileNetV2, Bahasa Pemrograman Python 3.10.11, Tkinter dan Google Text-To-Speech untuk mengidentifikasi abjad A-Z dalam Bahasa Isyarat Indonesia.\n", "content")
    text_widget.insert("end", "\n")
    text_widget.insert("end", "Algoritma MobileNetV2 adalah sistem deteksi objek waktu nyata yang dapat mendeteksi dan mengklasifikasikan objek dalam gambar atau aliran video. Dalam aplikasi ini, algoritma ini dilatih untuk mengenali isyarat tangan yang sesuai dengan huruf A-Z dalam Bahasa Isyarat Indonesia.\n", "content")
    text_widget.insert("end", "\n")
    text_widget.insert("end", "Untuk menggunakan aplikasi ini, pengguna dapat memilih menu Identifikasi abjad BISINDO, setelah itu pengguna dapat memilih identifikasi melalui 3 opsi yaitu deteksi melalui video, realtime, dan melalui gambar. Algoritma akan mendeteksi dan menampilkan abjad bahasa isyarat BISINDO yang terindentifikasi.", "content")

    # Disable text widget editing
    text_widget.config(state="disabled")

    # Start the GUI event loop
    window.resizable(False, False)
    window.mainloop()


# Panggil fungsi untuk menampilkan halaman "Tentang"
display_about_page()
