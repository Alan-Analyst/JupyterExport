import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import nbformat
from nbconvert import PDFExporter, HTMLExporter
import os
import threading
import subprocess


ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# Load an image
icon_path = os.path.join(ASSETS_DIR, 'icon.ico')

#########
# Theme #
#########
theme_path = os.path.join(ASSETS_DIR, 'Anthracite.json')
ctk.set_appearance_mode(theme_path)  # default
ctk.set_default_color_theme(theme_path)  # default

#######
# GUI #
#######


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('JupyterExport')
        self.iconbitmap(default=icon_path)
        self.configure(fg_color='#35374B')
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width = 250
        app_height = 270

        # Calculate the position to center the window
        x = (screen_width/2) - (app_width/2)
        y = (screen_height/2) - (app_height/2)

        # Set the window size and position
        self.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.resizable('False', 'False')

        # Bind the on_closing function to the window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ###########
        # Widgets #
        ###########
        frame_main = ctk.CTkFrame(self, fg_color='transparent', border_width=0)
        frame_main.pack(fill=tk.BOTH, expand=True, pady=20)

        # Create a StringVar variable
        self.text_variable = ctk.StringVar()
        self.text_variable.set("No file selected")  # Set initial value

        open_button = ctk.CTkButton(frame_main, text="Notebook File", command=self.open_file_dialog)
        open_button.pack()

        # Create a Label widget and connect it to the StringVar variable
        label = ctk.CTkLabel(frame_main, textvariable=self.text_variable, text_color='white')
        label.pack()

        self.convert_to = ctk.StringVar(value="PDF")
        option_menu = ctk.CTkOptionMenu(frame_main, values=["PDF", "HTML"],
                                        variable=self.convert_to)
        option_menu.pack()

        self.output_file_var = ctk.StringVar()
        self.output_file_var.set("output")
        output_file_ent = ctk.CTkEntry(frame_main, textvariable=self.output_file_var)
        output_file_ent.pack(pady=20)

        self.convert_btn = ctk.CTkButton(frame_main, text="Convert", command=self.check_fun)
        self.convert_btn.pack(pady=20)

        self.conversion_in_progress_flag = False

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Check if a conversion is in progress
            if self.conversion_in_progress_flag:
                # Prompt the user to confirm canceling the conversion
                messagebox.showwarning("Warning", "Conversion in progress. Please wait until the conversion is "
                                                  "complete before closing the application.")

            else:
                # Close the application
                self.destroy()

    def open_file_dialog(self):
        global file
        file = filedialog.askopenfilename(
            title="Select IPython Notebook File",
            filetypes=[("IPython Notebook Files", "*.ipynb")]
        )

        if file:
            # Extract the filename from the path
            file_name = os.path.basename(file)
            self.text_variable.set(file_name)
        else:
            self.text_variable.set("No file selected")

    def check_fun(self):
        # Create a new thread for the long-running function
        if self.text_variable.get() != "No file selected":
            self.convert_ipynb_threaded(file, self.output_file_var.get())
        else:
            messagebox.showerror("Error", "Please choose a file to convert!")

    @staticmethod
    def open_file_in_browser(output):
        """
        Open the file in the default file browser.
        """
        # get location of output file
        output_path = os.path.abspath(output)

        # Open the directory where the output file is located
        output_dir = os.path.dirname(output_path)
        try:
            if os.name == 'nt':
                # For Windows
                os.startfile(output_dir)
            elif os.name == 'posix':
                # For macOS and Linux
                subprocess.Popen(['open', output_dir])
            else:
                subprocess.Popen(['xdg-open', output_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory: {str(e)}")

    def convert_ipynb_threaded(self, ipynb_file, output):
        # Start a new thread to run the conversion function
        thread = threading.Thread(target=self.convert_ipynb, args=(ipynb_file, output))
        thread.start()

    def convert_ipynb(self, ipynb_file, output):
        self.conversion_in_progress_flag = True

        self.configure(cursor='wait')
        self.convert_btn.configure(state='disabled')

        if self.convert_to.get() == 'PDF':
            # Read the IPython Notebook
            with open(ipynb_file, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)

            # Initialize the PDF exporter
            pdf_exporter = PDFExporter()

            # Convert the notebook to PDF
            body, resources = pdf_exporter.from_notebook_node(nb)

            # Write the PDF
            with open(f'{output}.pdf', 'wb') as f:
                f.write(body)
        else:
            # Read the IPython Notebook
            with open(ipynb_file, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)

            # Initialize the HTML exporter
            html_exporter = HTMLExporter()

            # Convert the notebook to HTML
            body, resources = html_exporter.from_notebook_node(nb)

            # Write the HTML
            with open(f'{output}.html', 'w', encoding='utf-8') as f:
                f.write(body)

        self.convert_btn.configure(state='normal')
        self.configure(cursor="")
        messagebox.showinfo("Success", "Operation completed successfully!")
        self.conversion_in_progress_flag = False

        self.open_file_in_browser(output)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
