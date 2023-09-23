import sys
from functools import partial
from tkinter import *
from tkinter import ttk, filedialog, messagebox

import PIL.Image
import PIL.ImageTk
import cv2.cv2 as cv

import DetectFace
import VideoInterface

bg_color = 'teal'
bg1_color = '#016064'
bg2_color = 'white'
bg3_color = '#B0E0E6'
active_bg_color = '#00FFFF'

cap: cv.VideoCapture
index_of_record: int
indexes_list: list
global_name = ""


class Root:
    root = Tk()
    root.geometry(newGeometry='902x663+1+1')
    root.title("CHERCHER PERSONNE")
    root.resizable(False, False)
    root.configure(background=bg_color)
    if sys.platform.startswith('win'):
        root.iconbitmap('icons/img_par_defaut.ico')
    else:
        logo = PhotoImage(file='/home/airs/python_projects/detectPersonne/icons/img_par_defaut.png')
        root.tk.call('wm', 'iconphoto', root, logo)

    image_background = PIL.ImageTk.PhotoImage(PIL.Image.open("/home/airs/python_projects/detectPersonne/images/image_background.png"))
    video_background = PIL.ImageTk.PhotoImage(PIL.Image.open("/home/airs/python_projects/detectPersonne/images/video_background.png"))
    cross = PIL.ImageTk.PhotoImage(PIL.Image.open("/home/airs/python_projects/detectPersonne/images/cross.png"))
    refresh = PIL.ImageTk.PhotoImage(PIL.Image.open('/home/airs/python_projects/detectPersonne/images/refresh.png'))


mainobject = Root()


class VideoAnime:
    video_frame = Frame(mainobject.root, background=bg_color, relief=SOLID, borderwidth=1)
    video_frame.place(x='13.51', y='67.34', width='461.99', height='274.11')

    can = Canvas(video_frame, bg=bg_color, width=461, height=274)
    can.create_image(230, 137, image=mainobject.video_background, anchor=CENTER)
    can.pack()

    video_section = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)
    video_section.place(x='128', y='381.17', width='347', height='40.7')


class Image:
    img_frame = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)
    img_frame.place(x='524.53', y='67.34', width='361.97', height='274.11')

    img_section = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)
    img_section.place(x='525', y='381.17', width='361', height='40.7')

    image_show = Label(img_frame, bg=bg1_color, image=mainobject.image_background)
    image_show.pack()


class ClearButtonImage(Image):
    def clearImgLocation(self):
        self.select_img_location.config(text='')
        self.image_show.destroy()
        self.image_show.__init__(self.img_frame, bg=bg1_color, image=mainobject.image_background)
        self.image_show.pack()
        DetectFace.resetFaceEncoding()

    clear_img = Button(Image.img_section, image=mainobject.cross,
                       command=lambda: ClearButtonImage.clearImgLocation(ClearButtonImage.__new__(ClearButtonImage)),
                       width=30, height=30, relief='solid', borderwidth=1,
                       background=bg_color, activebackground=active_bg_color)
    clear_img.pack(side=LEFT)

    select_img_location = Label(Image.img_section, width=28, bg=bg_color)
    select_img_location.pack(side=LEFT, padx=5)


class ClearButtonVideo(VideoAnime):

    def clearVideoLocation(self):
        global cap
        self.select_video_location.config(text='')
        try:
            if cap.isOpened():
                cap.release()
        except:
            print("capture var is not defined yet!")
        self.can.destroy()
        self.can.__init__(self.video_frame, bg=bg_color, width=461, height=274)
        self.can.create_image(230, 137, image=mainobject.video_background, anchor=CENTER)
        self.can.pack()

    clear_video = Button(VideoAnime.video_section, image=mainobject.cross, command=lambda: ClearButtonVideo.
                         clearVideoLocation(ClearButtonVideo.__new__(ClearButtonVideo)),
                         width=30, height=30, relief='solid', borderwidth=1,
                         background=bg_color, activebackground=active_bg_color)
    clear_video.pack(side=LEFT, padx=3)
    select_video_location = Label(VideoAnime.video_section, width=26, bg=bg_color)
    select_video_location.pack(side=LEFT, padx=3)


class BrowsingButton(ClearButtonImage, ClearButtonVideo):
    can_destroy = True
    browse_video = Button(ClearButtonVideo.video_section, text='Browse', relief=SOLID, command=lambda: BrowsingButton.
                          browseVideoFun(BrowsingButton.__new__(ClearButtonVideo)),
                          font=('Ubuntu Condensed', 14),
                          background=bg_color, activebackground=active_bg_color)
    browse_video.pack(side=LEFT)
    browse_img = Button(Image.img_section, text='Browse', relief=SOLID, command=lambda: BrowsingButton.
                        browseImgFun(BrowsingButton.__new__(ClearButtonImage)),
                        font=('Ubuntu Condensed', 14),
                        background=bg_color, activebackground=active_bg_color)
    browse_img.pack(side=LEFT)

    def browseImgFun(self: ClearButtonImage):
        filename = filedialog.askopenfilename(title="select an image",
                                              filetypes=(("Images files", "*.jpeg"), ("PNG files", "*.png"),
                                                         ("JPG files", "*.jpg")))
        self.select_img_location.config(text=filename)
        try:
            if not BrowsingButton.can_destroy:
                self.image_show.destroy()
                ImageProcess.updateImg(BrowsingButton.__new__(ClearButtonImage), filename,
                                       PIL.Image.open(filename).size[0], PIL.Image.open(filename).size[1])
                BrowsingButton.can_destroy = False
            else:
                ImageProcess.updateImg(BrowsingButton.__new__(ClearButtonImage), filename,
                                       PIL.Image.open(filename).size[0], PIL.Image.open(filename).size[1])
        except:
            messagebox.showwarning("nothing selected", "please select a valid image !")

    def browseVideoFun(self: ClearButtonVideo):
        global cap
        filename = filedialog.askopenfilename(title="select a file",
                                              filetypes=(("MP4 files", "*.mp4"), ("AVI files", "*.AVI"),
                                                         ("MKV files", "*.mkv")))
        self.select_video_location.config(text=filename)
        try:
            cap = cv.VideoCapture(filename)
            VideoProcess.takeThumbnail(self=VideoAnime.__new__(VideoAnime), capt=cap)
            duration = VideoInterface.writeInfoOverTime(cap)
            if duration >= 60:
                Information.info.config(text="la duré du video est : %.2f min" % (duration / 60))
            else:
                Information.info.config(text="la duré du video est : %.2f sec" % duration)
        except:
            messagebox.showwarning("nothing selected", "please select a valid video !")


class VideoProcess(BrowsingButton):
    photo = None

    def playVideo(self: VideoAnime, capt):
        global photo
        if capt.isOpened():
            ret, frame, message, faces, similarfaces, nonsimilarfaces = DetectFace.detectFaceVideo(capt)
            frame_with, frame_height = VideoInterface.calculSize(capt.get(cv.CAP_PROP_FRAME_WIDTH),
                                                                 capt.get(cv.CAP_PROP_FRAME_HEIGHT), 'video')
            frame = cv.resize(frame, [int(frame_with), int(frame_height)])
            if message < 30:
                if ret:
                    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                    self.can.create_image(230, 137, image=photo, anchor=CENTER)
                    Information.info.config(text="Nombre des visages : " + str(
                        faces) + "\nNombre des visages similaire au visage d'image de reference: "
                                                 + str(similarfaces) +
                                                 "\nNombre des visages deffirent similaire au visage d'image de reference : " + str(
                        nonsimilarfaces))
                self.video_frame.after(10, lambda: VideoProcess.playVideo(self=VideoProcess.__new__(VideoAnime),
                                                                          capt=cap))
            else:
                Information.info.config(text="le persnne a été trouvé !\n")
                photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.can.create_image(230, 137, image=photo, anchor=CENTER)

    def takeThumbnail(self: VideoAnime, capt: cv.VideoCapture):
        global photo
        ret, frame, message, faces, sim, nonsim = DetectFace.detectFaceVideo(capt)
        frame_with, frame_height = VideoInterface.calculSize(capt.get(cv.CAP_PROP_FRAME_WIDTH),
                                                             capt.get(cv.CAP_PROP_FRAME_HEIGHT), 'video')
        frame = cv.resize(frame, [int(frame_with), int(frame_height)])
        if ret and message < 30:
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.can.create_image(230, 137, image=photo, anchor=CENTER)

    def clickChercher(self):
        global cap, index_of_record
        if SelectVideoType.live_and_video.get() == 'Live':
            cap = cv.VideoCapture(index_of_record)
        self.playVideo(cap)


class ImageProcess(Image):
    image = None

    def updateImg(self: Image, filename, init_width, init_height):
        global image
        image_to_show = DetectFace.detectFaceImage(image_path=filename)
        image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image_to_show).
                                       resize((VideoInterface.calculSize
                                               (init_width,
                                                init_height, 'image'))))
        self.image_show.config(image=image)
        self.image_show.pack(padx=1, pady=1)


class RefreshButton:
    refresh_btn = Button(VideoAnime.video_section, bg=bg_color, image=mainobject.refresh,
                         command=lambda: LiveCamera.getCameras(RefreshButton.__new__(RefreshButton)),
                         width=30, height=30, relief='solid', activebackground=active_bg_color, borderwidth=1)
    live_camera_capture_chose = ttk.Combobox(VideoAnime.video_section, state='readonly',
                                             justify='center',
                                             font=('Ubuntu Condensed', 16), width=20)

    def getIndex(event):
        global index_of_record, global_name, indexes_list, cap
        if cap is not None:
            print("cap rel")
            cap.release()
        tmp_name = RefreshButton.live_camera_capture_chose.get()
        for i in range(len(RefreshButton.live_camera_capture_chose['value'])):
            if tmp_name in global_name[i]:
                index_of_record = indexes_list[i]

    live_camera_capture_chose.bind("<<ComboboxSelected>>", partial(getIndex))


class LiveCamera(RefreshButton):
    def getCameras(self: RefreshButton):
        global indexes_list, global_name, index_of_record
        if sys.platform.startswith('win'):
            names = VideoInterface.getCameraWin()
            indexes = VideoInterface.getIndexWin()
            self.live_camera_capture_chose.config(values=names)
            self.live_camera_capture_chose.current(0)
        else:
            names, indexes = VideoInterface.getNameIndex()
            self.live_camera_capture_chose.config(values=names)
            self.live_camera_capture_chose.current(0)
        index_of_record = indexes[0]
        global_name = names
        indexes_list = indexes


class ControlButton:
    control_button = Frame(mainobject.root, bg=bg_color)
    control_button.place(x='17.7', y='464.4', width='220.633', height='171.5')

    chercher_button = Button(control_button, text='Chercher', width='20', relief=SOLID,
                             font=('Ubuntu Condensed', 16), command=lambda:
                             VideoProcess.clickChercher(VideoProcess.__new__(VideoProcess)),
                             background=bg_color, activebackground=active_bg_color)

    quitter_bottom = Button(control_button, text='Quitter', width='20', command=quit, relief=SOLID,
                            default='disabled', font=('Ubuntu Condensed', 16),
                            background=bg_color, activebackground=active_bg_color)
    about_button = Button(control_button, text="About", width='20', relief=SOLID,
                          command=lambda: AboutButton.showAbout(AboutButton.__new__(AboutButton)),
                          font=('Ubuntu Condensed', 16),
                          background=bg_color, activebackground=active_bg_color
                          )
    chercher_button.pack()
    quitter_bottom.pack(pady='25')
    about_button.pack()


class Information:
    info_box = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)
    info_box.place(x='323.7', y='505.16', width='562.8', height='130.8')

    info = Label(info_box, text="", bg=bg_color, font=('Ubuntu Condensed', 14))
    info.pack()


class SelectVideoType(RefreshButton):
    def selectedElement(event):
        global cap
        if SelectVideoType.live_and_video.get() == 'Video':
            RefreshButton.live_camera_capture_chose.destroy()
            RefreshButton.refresh_btn.destroy()
            ClearButtonVideo.clear_video.pack(side=LEFT, padx=3)
            ClearButtonVideo.select_video_location.pack(side=LEFT, padx=3)
            BrowsingButton.browse_video.pack(side=LEFT)
            RefreshButton.live_camera_capture_chose.__init__(VideoAnime.video_section, state='readonly',
                                                             justify='center',
                                                             font=('Ubuntu Condensed', 16), width=20)
            RefreshButton.refresh_btn.__init__(VideoAnime.video_section, bg=bg_color, image=mainobject.refresh,
                                               command=lambda:
                                               LiveCamera.getCameras(RefreshButton.__new__(RefreshButton)),
                                               activebackground=active_bg_color, width=30, height=30, relief='solid',
                                               borderwidth=1)

        else:
            ClearButtonVideo.select_video_location.destroy()
            BrowsingButton.browse_video.destroy()
            RefreshButton.refresh_btn.pack(side=LEFT, padx=10)
            RefreshButton.live_camera_capture_chose.pack(side=LEFT, padx=10, pady=3)
            ClearButtonVideo.clear_video.pack(side=RIGHT, padx=20)
            ClearButtonVideo.select_video_location.__init__(VideoAnime.video_section, width=26, bg=bg_color)
            BrowsingButton.browse_video.__init__(VideoAnime.video_section, text='Browse',
                                                 command=lambda: BrowsingButton.browseVideoFun(
                                                     BrowsingButton.__new__(ClearButtonVideo)),
                                                 relief=SOLID,
                                                 font=('Ubuntu Condensed', 14),
                                                 background=bg_color, activebackground=active_bg_color)
            LiveCamera.getCameras(LiveCamera.__new__(LiveCamera))
            RefreshButton.live_camera_capture_chose.bind("<<ComboboxSelected>>", partial(RefreshButton.getIndex))
        ClearButtonVideo.clearVideoLocation(ClearButtonVideo.__new__(ClearButtonVideo))

    select_type = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)
    select_type.place(x='13.1', y='381.17', width='102', height='40.7')

    live_and_video = ttk.Combobox(select_type, state='readonly',
                                  justify='center',
                                  font=('Ubuntu Condensed', 16), width=7)
    live_and_video['value'] = ['Live', 'Video']
    live_and_video.current(1)
    live_and_video.bind("<<ComboboxSelected>>", partial(selectedElement))
    live_and_video.pack(pady=3)


class Titles:
    video_frame_title = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)

    img_frame_title = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)

    info_box_title = Frame(mainobject.root, bg=bg_color, relief=SOLID, borderwidth=1)

    video_frame_title.place(x='13.51', y='26.939', width='461.982', height='40.45')

    img_frame_title.place(x='524.53', y='26.94', width='361.97', height='40.45')

    info_box_title.place(x='323.7', y='464.4', width='562.8', height='40.7')

    video_title_label = Label(video_frame_title, width=100, height=2, text='Video',
                              font=('Ubuntu Condensed', 16),
                              bg=bg_color)
    video_title_label.pack()

    img_title_label = Label(img_frame_title, width=100, height=2, text='Image De Reference',
                            font=('Ubuntu Condensed', 14),
                            bg=bg_color)
    img_title_label.pack()

    info_title = Label(info_box_title, text='Information Sur La Recherche', bg=bg_color,
                       font=('Ubuntu Condensed', 16))
    info_title.pack(pady='5')


class AboutButton:

    def showAbout(self):
        from tkhtmlview import HTMLLabel

        about_window = Tk()
        about_window.geometry(newGeometry='541x200+1+1')
        about_window.title("About")
        about_window.config(background='gray')
        about_window.resizable(False, False)

        def quitAbout():
            about_window.destroy()

        about_frame = Frame(about_window, background='gray')
        about_frame.pack()
        about_info = Label(about_frame, background='gray')
        text_link = HTMLLabel(about_frame,
                              html='<a href="https://face-recognition.readthedocs.io/en/latest/face_recognition.html"> '
                              'Face-Recognition </a>',
                              background='gray', borderwidth=-1, width=20, height=2)

        about = "Projet de fin d'étude à la faculté polydiciplanaire Ouarzazate l'année 2022/2023\n" \
                "Abdelaziz El-adarissi - El alaoui Mohamed - Naji Abderrahim\n" \
                "Encadrée par prof.Salma Gaou \n" \
                "Nous avons utilisé Face-Recognition pour détecté les déffirents\n" \
                " visages dans un video/temps réel \n" \
                "et les comparées avec l'image de personne rechercher(image de référence) . \n" \
                "pour plus d'information sur Face-Recognition voir:"
        about_info.config(text=about)
        about_info.pack()
        text_link.pack()
        leave_about = Button(about_window, text="OK", width=15, background='gray', relief='flat', borderwidth=-1,
                             activebackground='gray',
                             command=quitAbout, font=('Ubuntu Condensed', 14))
        leave_about.pack(anchor=S)


# --------------------------------------------------------------------------
if __name__ == '__main__':
    mainobject.root.mainloop()
