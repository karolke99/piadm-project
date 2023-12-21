import customtkinter

from tkinter.colorchooser import askcolor
from tkinter.filedialog import askdirectory

customtkinter.set_appearance_mode('system')
customtkinter.set_default_color_theme('blue')


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.background_color = 'gray'
        self.model_color = 'white'
        self.working_dir = '...'

        self.title('Marching cubes 3D models')
        self.geometry(f'{600}x{300}')

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nesw")

        self.select_color_label = customtkinter.CTkLabel(master=self.frame, text='Select color for background')
        self.select_color_label.grid(row=0, column=1, padx=10, pady=5)
        self.select_color_button = customtkinter.CTkButton(master=self.frame, fg_color=self.background_color,
                                                           border_width=2, text='',
                                                           command=self.select_background_color)
        self.select_color_button.grid(row=0, column=3, padx=10, pady=5)

        self.select_model_label = customtkinter.CTkLabel(master=self.frame, text='Select color for model')
        self.select_model_label.grid(row=1, column=1, padx=10, pady=5)
        self.select_model_color_button = customtkinter.CTkButton(master=self.frame, fg_color=self.model_color,
                                                                 border_width=2, text='',
                                                                 command=self.select_model_color)
        self.select_model_color_button.grid(row=1, column=3, padx=10, pady=5)

        self.select_working_dir_label = customtkinter.CTkLabel(master=self.frame, text='Select working directory')
        self.select_working_dir_label.grid(row=2, column=1, padx=10, pady=5)
        self.select_working_dir_button = customtkinter.CTkButton(master=self.frame, fg_color='transparent',
                                                                 border_width=2, text=self.working_dir,
                                                                 command=self.select_working_dir)
        self.select_working_dir_button.grid(row=2, column=3, padx=10, pady=5)

    def select_background_color(self):
        self.background_color = askcolor(title='Select color')
        self.select_color_button.configure(fg_color=f'{self.background_color[1]}')

    def select_model_color(self):
        self.model_color = askcolor(title='Select color')
        self.select_model_color_button.configure(fg_color=f'{self.model_color[1]}')

    def select_working_dir(self):
        self.working_dir = askdirectory(title='Select directory')
        self.select_working_dir_button.configure(text=self.working_dir)


if __name__ == '__main__':
    app = App()
    app.mainloop()
