import base64
import json
import tkinter as tk
import platform

try:  # This allows Windows 10 to scale the window for high DPI monitors.
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# For some reason, the right-click binding is swapped with middle click on MacOS
if platform.system() == "Darwin":
    RIGHT_CLICK = "<Button-2>"
else:
    RIGHT_CLICK = "<Button-3>"


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TkBase64")
        self.window.minsize(300, 400)
        self.window.geometry("300x400")
        # self.window.resizable(False, False)

        self.swapped = False

        self.frame = tk.Frame(self.window, background="#1f1f1f")

        self.text_input = tk.Text(
            self.frame,
            background="#404040",
            foreground="white",
            highlightbackground="#1f1f1f",
            highlightcolor="#5e5e5e",
            insertbackground="white",
        )
        self.text_input.bind("<KeyRelease>", lambda e: self.utf8_to_base64())
        self.text_input.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.m = tk.Menu(self.window, tearoff=0)
        self.m.add_command(
            label="Select All", command=lambda: self.select_all(self.text_input)
        )
        self.m.add_command(
            label="Replace with Clipboard",
            command=lambda: self.replace_from_clipboard(
                self.text_input, self.utf8_to_base64
            ),
        )
        self.m.add_separator()
        self.m.add_command(label="JSON Prettify", command=self.prettify_json)
        self.m.add_separator()
        self.m.add_command(label="Clear", command=self.clear)
        self.text_input.bind(RIGHT_CLICK, lambda e: self.menu_popup(self.m, e))

        self.swap_button = tk.Label(
            self.frame,
            text="Swap 🔄",
            background="#626262",
            foreground="white",
            relief="raised",
        )
        self.swap_button.bind(
            "<Button-1>", lambda e: self.swap_button.configure(bg="#848484")
        )
        # In order to fire multiple events on the same keypress,
        # It's necessary to add a "+" at the end of the binding.
        # https://docs.python.org/3/library/tkinter.html#bindings-and-events
        self.swap_button.bind("<ButtonRelease-1>", self.swap_boxes)
        self.swap_button.bind(
            "<ButtonRelease-1>",
            lambda e: self.swap_button.configure(bg="#525252"),
            add="+",
        )
        self.swap_button.grid(row=1, column=0, sticky="ew", padx=10)

        self.base64_input = tk.Text(
            self.frame,
            background="#404040",
            foreground="#ffe78f",
            highlightbackground="#1f1f1f",
            highlightcolor="#5e5e5e",
            insertbackground="white",
        )
        self.base64_input.bind("<KeyRelease>", lambda e: self.base64_to_utf8())
        self.base64_input.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.m2 = tk.Menu(self.window, tearoff=0)
        self.m2.add_command(
            label="Select All", command=lambda: self.select_all(self.base64_input)
        )
        self.m2.add_command(
            label="Replace with Clipboard",
            command=lambda: self.replace_from_clipboard(
                self.base64_input, self.base64_to_utf8
            ),
        )
        self.m2.add_separator()
        self.m2.add_command(label="Clear", command=self.clear)
        self.base64_input.bind(RIGHT_CLICK, lambda e: self.menu_popup(self.m2, e))

        self.copy_button = tk.Label(
            self.frame,
            text="Copy to Clipboard 📋",
            background="#626262",
            foreground="white",
            relief="raised",
        )
        self.copy_button.bind(
            "<Button-1>",
            lambda e: self.copy_to_clipboard(
                self.text_input if self.swapped else self.base64_input
            ),
        )
        self.copy_button.bind(
            "<Button-1>", lambda e: self.copy_button.configure(bg="#848484"), add="+"
        )
        self.copy_button.bind(
            "<ButtonRelease-1>", lambda e: self.copy_button.configure(bg="#525252")
        )
        self.copy_button.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Makes sure the frame sticks to all sides
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        # Start the application
        self.window.mainloop()

    def utf8_to_base64(self):
        try:
            text = self.text_input.get("1.0", "end-1c")
            text_encoded = base64.b64encode(bytes(text, "utf-8"))
            self.base64_input.config(state="normal")
            self.base64_input.delete(1.0, "end")
            self.base64_input.insert("end", text_encoded)
        except ValueError:
            self.base64_input.config(text=f"ERROR", state="disabled")

    def base64_to_utf8(self):
        try:
            text = self.base64_input.get("1.0", "end-1c")
            text_decoded = base64.b64decode(text)
            self.text_input.config(state="normal")
            self.text_input.delete(1.0, "end")
            self.text_input.insert("end", text_decoded)
        except ValueError:
            self.text_input.delete(1.0, "end")
            self.text_input.insert("end", "<Invalid BASE64>")

    def swap_boxes(self, _):
        # This replicates the behavior of canceling the action
        # in case the click is released outside the widget.
        # widget_under_cursor = event.widget.winfo_containing(event.x_root, event.y_root)
        # if widget_under_cursor != event.widget:
        #     return

        self.swapped = not self.swapped

        if self.swapped:
            self.text_input.grid(row=2)
            self.base64_input.grid(row=0)
        else:
            self.text_input.grid(row=0)
            self.base64_input.grid(row=2)

        self.window.update()

    def copy_to_clipboard(self, widget):
        widget.clipboard_clear()
        widget.clipboard_append(widget.get("1.0", "end-1c"))
        self.copy_button.configure(text="Copied! ✅")
        self.frame.after(
            1000, lambda: self.copy_button.configure(text="Copy to Clipboard 📋")
        )

    def menu_popup(self, menu, event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def prettify_json(self):
        try:
            text = self.text_input.get("1.0", "end-1c")
            result = json.loads(text)
            self.text_input.delete(1.0, "end")
            self.text_input.insert("end", json.dumps(result, indent=4))
            self.utf8_to_base64()
        except ValueError:
            pass

    def select_all(self, widget):
        widget.tag_add(tk.SEL, "1.0", "end-1c")
        widget.mark_set(tk.INSERT, "1.0")
        widget.see(tk.INSERT)

    def clear(self):
        self.text_input.delete(1.0, "end")
        self.base64_input.delete(1.0, "end")

    def replace_from_clipboard(self, widget, convert_func):
        widget.delete(1.0, "end")
        widget.insert("end", widget.clipboard_get())
        convert_func()


if __name__ == "__main__":
    App()
