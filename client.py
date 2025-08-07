import tkinter as tk
from tkinter import scrolledtext
import ollama
from tkinter import ttk
from secrets import token_hex
import requests
import bsave

class ClientApp:
    def __init__(self, master):
        self.master = master
        self.conversation_id = token_hex(12)
        self.app_key = ""
        m = ollama.ps()
        master.resizable(False, False)
    
        if ( m['models'] == []):
            master.title("(-.-)zZ")
            self.model_name = []
            self.model_expire = []
        else:
            master.title("(^-^)*")
            for i in m['models']:
                self.model_name = i.name
                self.model_expire = i.expires_at

        self.url = tk.StringVar(value="http://localhost:5000/706e676e2d6e616e")  
        self.session_id = token_hex(12)
        self.chat_history = []
        self.input_text = tk.Text(master, height=3, width=50, wrap=tk.WORD)
        self.input_text.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.c_mode = False
        self.send_button = ttk.Button(master, text="Send", command=self.send_request)
        self.send_button.grid(row=1, column=1,  pady=10)
        self.session_button = tk.Button(master, command=self.sessions_window, text="Sessions")
        self.session_button.grid(row=1, column=2, pady=10)
        self.conversation_mode = ttk.Checkbutton(master, text="chat", variable=self.c_mode, command=self.new_conversation_id)
        self.conversation_mode.grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
        self.master.withdraw()
        self.context_definitions = []
        self.sessions = []
        
        
    def submit_key(self):
        self.key = self.key_entry.get()
        
        self.splash_window.grab_release()
        self.master.deiconify()
        self.splash_window.destroy()
        
    def splash(self):
        self.splash_window = tk.Toplevel()
        self.splash_window.grab_set()
        self.splash_window.title("Enter key to decrypt")
        self.splash_window.resizable(False, False)
        self.key_entry = ttk.Entry(self.splash_window, textvariable="Enter Decryption Key", width=40)
        self.key_entry.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        
        self.submit_button = ttk.Button(self.splash_window, text="Submit", command=self.submit_key)
        self.submit_button.grid(row=1, column=1,  pady=10)        

    def new_conversation_id(self):
        if (self.c_mode is False):
            self.c_mode = True
        elif (self.c_mode is True):
            self.c_mode = False
        
    def open_context_window(self, conv_id):
        """Opens a new context window with the given title and data."""
        self.context_window = tk.Toplevel() 
        self.context_window.title("( 0-0)_/")
        self.context_window.resizable(False, True)
        self.context_window_frame = tk.Frame(self.context_window, width=400, height=20)
        self.context_window_frame.pack()
        
        i=0
        j=0
        
        for chat in self.sessions:
            if (chat["conversation_id"] == conv_id):
                if (chat["role"] == "user"):       
                    self.text_area = tk.Text(self.context_window_frame, height=3, width=100, wrap=tk.WORD)
                    self.text_area.grid(row=i, column=j,pady=10, padx=10)
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, chat['content'])
                    #self.text_area.config(state=tk.DISABLED)
    
                    if (i >= 1):
                        j+=1
                        i = 0
                    else:
                        i+=1
                        
                elif (chat["role"] == "assistant"):
                    self.text_area2 = tk.Text(self.context_window_frame, height=35, width=100, wrap=tk.WORD)
                    self.text_area2.grid(row=i, column=j,pady=10, padx=10)
                    self.text_area2.delete("1.0", tk.END)
                    self.text_area2.insert(tk.END, chat['content'])
                    #self.text_area2.config(state=tk.DISABLED)
                    
                    if (i >= 1):
                        j+=1
                        i = 0
                    else:
                        i+=1
        
       # return context_window
        
    def sessions_window(self):
        #load db to file or load from file
        self.sessions = wtf.load()
        x=0
        i=0
        j=0
        
        self.session_window = tk.Toplevel(self.master)
        self.session_window.title("( 0-0)_/")
        #self.session_window.geometry("300x400+10+10")
        self.session_window_frame = tk.Frame(self.session_window, width=400, height=20)
        self.session_window_frame.pack()
        prev_conv_id = 0
        
        for data in self.sessions:
            if (data["role"] == "user"):
                if (data["conversation_id"] != prev_conv_id): # Change to !=
                    
                        
                    self.session_button = tk.Button(self.session_window_frame, text=data["content"][:35], command=lambda cid=data["conversation_id"]: self.open_context_window(cid))
                    
                    self.session_button.grid(row=i, column=j,pady=10, padx=10, sticky="nsew")
                    #i+=1
                    if (i >= 10):
                        j += 1
                        i = 0
                    else:
                        i += 1
                    
            prev_conv_id = data["conversation_id"]
            
            
    def create_response_window(self, rx):
        self.response_window = tk.Toplevel()#self.master)
        self.response_window.title("(^O^)_/")
        #self.response_window.geometry("600x400+100+50")
        
        self.response_window.resizable(False, True)
        
        
        self.response_window_text = tk.Text(self.response_window, height=30, width=100, wrap=tk.WORD)
        self.response_window_text.grid(row=2, column=1, padx=5, pady=5)
        self.response_window_text.delete("1.0", tk.END)
        self.response_window_text.insert(tk.END, rx["message"]["content"])
        self.response_window_text.config(state=tk.DISABLED)
        #self.response_window.grab_set()
        
    def send_request(self):
        data = self.input_text.get("1.0", tk.END)
        is_model_running = ollama.ps()
        mn = is_model_running["models"]
        
        if ( is_model_running['models'] == []):
            self.master.title("(-.-)zZ")
            self.model_name = []
            self.model_expire = []
        else:
            self.master.title("(^-^)*/")
            
            for i in is_model_running['models']:
                self.model_name = i.name
                self.model_expire = i.expires_at
        
        if (self.model_name):
            if (not self.c_mode):
                self.chat_history = []
                self.conversation_id = token_hex(12)
                #print(f"new conversation id: {self.conversation_id}")
            
            msg = {"model": self.model_name, "role": "user", "content": data, "session_id": self.session_id, "conversation_id": self.conversation_id}
            self.chat_history.append(msg)
            wtf.save(msg)
            
            if (data):
                Rx: ollama.ChatResponse = ollama.chat(model=self.model_name,messages=[{'role': "user",'content': data}])
                
                if (Rx["message"]["content"]):
                    msg_resp = {"model": self.model_name, "role": "assistant", "content": Rx["message"]["content"], "session_id": self.session_id, "conversation_id": self.conversation_id}
                    self.chat_history.append(msg_resp)
                    wtf.save(msg_resp)
                    #self.sessions.append(self.chat_history)
                    self.create_response_window(Rx)
                    
        elif (not self.model_name):
            self.master.title('(-.-)zZ')
 
if __name__ == "__main__":
    wtf = bsave.PersistentStorage("static", ["model","role","content","session_id","conversation_id"]) #send to server every message
    root = tk.Tk()

    app = ClientApp(root)
    app.splash()
    root.mainloop()

