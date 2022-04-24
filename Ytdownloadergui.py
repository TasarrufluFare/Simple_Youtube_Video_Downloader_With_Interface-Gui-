from pytube import YouTube
import os
import ffmpeg
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

path = ""
path_tmp = ""


# pytube için gerekli fonksiyonların tanımı
def on_complete(stream, filepath):
    download_progress.config(text=f"İndirme tamamlandı.\nKonum: {path}")


def on_progress(stream, chunks, bytes_remaining):
    #Terminalde kontrol etmek için yazılan kod
    #loaded_size = f'{round(100 - (bytes_remaining / stream.filesize * 100), 2)}%'
    #print(loaded_size)
    pass

'''
#Saniye cinsinden video süresini dakika ve saniye cinsinden geri veren fonksiyon
def time(lenght):
    return (str(lenght // 60) + " dakika " + str(lenght % 60) + " saniye")
'''


# Gui Fonksiyonlar
def select_path():
    global path
    global path_tmp
    path = filedialog.askdirectory()
    if not path == "":
        path_tmp = path
        path_label.config(text=f"İndirme konumu: {path}")
    else:
        path = path_tmp
        pass


def download_file1():
    try:
        video_link = link_box.get()
        video_object = YouTube(video_link, on_complete_callback=on_complete, on_progress_callback=on_progress)
        gonna_download = video_object.streams.get_highest_resolution()
        global path
        gonna_download.download(path)
    except:
        messagebox.showerror("Hata!", "Bir şeyler ters gitti. Video linkinin doğru olduğuna emin ol.")


def download_file2():
    try:
        global path
        video_link = link_box.get()
        video_object = YouTube(video_link, on_complete_callback=on_complete, on_progress_callback=on_progress)
        gonna_download = video_object.streams.get_by_itag(251)
        out_file = gonna_download.download(path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    except:
        messagebox.showerror("Hata!", "Bir şeyler ters gitti. Video linkinin doğru olduğuna emin ol.")


def download_file3():
    onaylama = messagebox.askyesno("Uyarı!", "Bu işlem yüksek miktarda işlemci yükü gerektirebilir ve uzun sürebilir?"
                                             "Devam etmek istiyor musun? - İşlem bittiğinde bildirim alacaksınız.")
    if onaylama == 1:
        try:
            global path
            video_link = link_box.get()
            video_object = YouTube(video_link, on_complete_callback=on_complete, on_progress_callback=on_progress)
            gonna_download_video = video_object.streams.filter(resolution="1080p").first().download(
                filename="indirilenvideo.mp4")
            gonna_download_audio = video_object.streams.get_by_itag(251)
            out_file = gonna_download_audio.download(filename="indirilenses")
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            # Dosyaların birleştirilmesi
            infile1 = ffmpeg.input("./" + "indirilenvideo" + ".mp4")
            infile2 = ffmpeg.input("./" + "indirilenses" + ".mp3")
            output_file_name = "indirilenytdownloader_merged.mp4"
            if path != "":
                merged = ffmpeg.concat(infile1, infile2, v=1, a=1).output(path + "/" + output_file_name).run()
            if path == "":
                merged = ffmpeg.concat(infile1, infile2, v=1, a=1).output("./" + output_file_name).run()
            # Ayrılmış durumdaki ses ve görüntünün silinmesi
            if os.path.exists("./" + "indirilenvideo" + ".mp4"):
                os.remove("./" + "indirilenvideo" + ".mp4")
            else:
                messagebox.showinfo("Silinememiş Dosya Var!",
                                    "Birleştirilme sonrası indirme konumunda artık dosya kalmış olabilir.")
            if os.path.exists("./" + "indirilenses" + ".mp3"):
                os.remove("./" + "indirilenses" + ".mp3")
            else:
                messagebox.showinfo("Silinememiş Dosya Var!",
                                    "Birleştirilme sonrası indirme konumunda artık dosya kalmış olabilir.")
            messagebox.showinfo("Bilgilendirme!", "İndirme tamamlandı!")
        except:
            messagebox.showerror("Hata!",
                                 "Bir şeyler ters gitti. Videonun 1080p çözünürlüğe sahip olduğuna ve video linkinin doğru olduğuna emin ol.")
    else:
        download_progress.config(text="Vazgeçtiniz")
        pass

    pass


# Form Hatları
screen = Tk()
title = screen.title("Youtube Video Downloader by Tasarruflu Fare")
canvas = Canvas(screen, width=500, height=570, background="dark green")
screen.resizable(0, 0)
canvas.pack()

# Form logo ve icon tanımı ve yerleştirilmesi
logo_image = PhotoImage(file="ytvideo.png")
main_image = PhotoImage(file="mainlogo.png")
logo_image = logo_image.subsample(12, 12)
main_image = main_image.subsample(3, 3)
screen.iconbitmap("mainlogoicon.ico")
canvas.create_image(85, 550, image=logo_image)
canvas.create_image(250, 80, image=main_image)

# Form elemanlarının tanımlanması
link_box = Entry(screen, width=40)
link_box_label = Label(screen, text="İndirmek istediğiniz videonun linki", font=('Arial', 11), background="Dark Green")
path_label = Label(screen, text="İndirme konumu seçilmedi (Varsayılan konum uygulama konumu)", font=('Arial', 11),
                   background="Dark Green")
Path_btn = Button(screen, text="İndirme konumu seç", font=('Arial', 9), command=select_path)
download_progress = Label(screen, text="İndirilen Dosya Yok", font=('Arial', 9), background="Dark Green")
download_button1 = Button(screen, text="Video Olarak İndir", font=('Arial', 9), command=download_file1)
download_button2 = Button(screen, text="MP3 Olarak indir", font=('Arial', 9), command=download_file2)
download_button3 = Button(screen, text="Yüksek Kaliteli Video Olarak indir - (Optimize Edilmedi)", font=('Arial', 9),
                          command=download_file3)

# From üzerinde çağrılma
canvas.create_window(250, 220, window=link_box)
canvas.create_window(250, 180, window=link_box_label)
canvas.create_window(250, 260, window=Path_btn)
canvas.create_window(250, 300, window=download_button1)
canvas.create_window(250, 340, window=download_button2)
canvas.create_window(250, 380, window=download_button3)
canvas.create_window(250, 420, window=path_label)
canvas.create_window(250, 460, window=download_progress)

screen.mainloop()
