import tkinter as tk

def send_message():
    user_input = user_entry.get()
    user_entry.delete(0, tk.END)  # 清空用户输入
    chat_box.config(state=tk.NORMAL)  # 设置聊天框可编辑
    chat_box.insert(tk.END, "You: " + user_input + "\n")  # 将用户输入添加到聊天框
    chat_box.config(state=tk.DISABLED)  # 设置聊天框为只读

    # 在这里添加机器人的回应
    bot_response = "Bot: " + "Hello, I'm a bot. You said: " + user_input + "\n"
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, bot_response)
    chat_box.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("Chat Room")

# 创建聊天框
chat_box = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD)
chat_box.pack()

# 创建用户输入框和发送按钮
user_entry = tk.Entry(root)
user_entry.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

root.mainloop()