import tkinter as tk

def submit():
    text_content = text.get("1.0", tk.END) 
    print(text_content)

root = tk.Tk()
root.geometry("640x480")

label = tk.Label(root, text="Enter your text:", font=("Arial", 14))
label.place(x=20, y=50)

text = tk.Text(root, width=20, height=10, font=("Arial", 14))
text.place(x=20, y=100)
text.insert(tk.END, "Please grab the red block and then grab the blue block.")

Submit = tk.Button(root, text="Submit", font=("Arial", 14), command=submit)
Submit.place(x=20, y=350)

Quit = tk.Button(root, text="Quit", font=("Arial", 14), command=submit)
Quit.place(x=120, y=350)

root.mainloop()
