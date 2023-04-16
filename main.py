import subprocess
import pandas as pd
import socket
import ipaddress
from tkinter import *
import customtkinter as ctk
import threading
import speedtest

HOSTLIST = pd.DataFrame({
    'global': ['8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1'],
    'intranet': ['digikala.com', 'alibaba.ir', 'www.snapptrip.com', 'ito.gov.ir'],
    'filtered': ['telegram.org', 'youtube.com', 'facebook.com', 'twitter.com']
})

GLOBAL_LIST = HOSTLIST['global'].tolist()
INTRANET_LIST = HOSTLIST['intranet'].tolist()
FILTERED_LIST = HOSTLIST['filtered'].tolist()

SELECTED_FONT = ("B Yekan", 25)

ctk.set_appearance_mode('System')


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('PingPong')
        self.geometry('500x700')
        self.resizable(width=False, height=False)

        # Label
        self.Label = ctk.CTkLabel(self,
                                  text="سرور تست پینگ را انتخاب کنید",
                                  font=SELECTED_FONT,
                                  anchor=CENTER)
        self.Label.place(relx=0.9, rely=0.08, anchor=ctk.E)

        # Radio buttons
        server_options = [("Global", "Global"), ("Intranet", "Intranet"), ("Filtering", "Filtering")]
        self.ServerSelection = ctk.StringVar(value="Global")

        for i, (text, value) in enumerate(server_options):
            radio_button = ctk.CTkRadioButton(self,
                                              text=text,
                                              variable=self.ServerSelection,
                                              value=value,
                                              font=SELECTED_FONT)
            radio_button.place(relx=0.05 + i * 0.3, rely=0.13, anchor=ctk.NW)

        # Start button
        self.button = ctk.CTkButton(master=self, text="شروع تست",
                                    font=SELECTED_FONT, command=self.start_ping_thread)
        self.button.place(relx=0.5, rely=0.20, anchor=ctk.N)

        # Text box
        self.displayBox = ctk.CTkTextbox(self, width=500,
                                         height=320,
                                         font=("Tahoma", 18),
                                         activate_scrollbars=True,
                                         state="disable")
        self.displayBox.place(relx=0.5, rely=0.31, anchor=ctk.N)

        self.progressbar = ctk.CTkProgressBar(master=self,
                                              width=500,
                                              height=20)
        self.progressbar.place(relx=0.5, rely=0.28, anchor=ctk.N)
        self.progressbar.set(0.0)

        self.pingLabel = ctk.CTkLabel(self,
                                      text="پینگ",
                                      font=SELECTED_FONT)
        self.pingLabel.place(relx=0.22, rely=0.83, anchor=ctk.E)

        self.downloadLabel = ctk.CTkLabel(self,
                                          text="دانلود",
                                          font=SELECTED_FONT)
        self.downloadLabel.place(relx=0.5, rely=0.83, anchor='center')

        self.uploadLabel = ctk.CTkLabel(self,
                                        text="آپلود",
                                        font=SELECTED_FONT)
        self.uploadLabel.place(relx=0.78, rely=0.83, anchor=ctk.W)

        self.pingedLabel = ctk.CTkLabel(self,
                                        text="--",
                                        font=("Tahoma", 18))
        self.pingedLabel.place(relx=0.22, rely=0.93, anchor=ctk.E)

        self.downloadedLabel = ctk.CTkLabel(self,
                                            text="--",
                                            font=("Tahoma", 18))
        self.downloadedLabel.place(relx=0.5, rely=0.93, anchor='center')

        self.uploadedLabel = ctk.CTkLabel(self,
                                          text="--",
                                          font=("Tahoma", 18))
        self.uploadedLabel.place(relx=0.78, rely=0.93, anchor=ctk.W)

    def get_ip_address(self, host_check):
        host_check = host_check.strip()
        try:
            ip_address = ipaddress.ip_address(host_check)
            return str(ip_address)
        except ValueError:
            try:
                ip_address = socket.gethostbyname(host_check)
                return ip_address
            except socket.gaierror:
                raise ValueError("Invalid input: {}".format(host_check))

    def get_ping(self, hosts):
        st = speedtest.Speedtest()
        st.get_best_server()
        ip_addresses = [self.get_ip_address(host) for host in hosts]
        loss_percentages = []
        status_bar_progress = float(0)
        self.progressbar.set(status_bar_progress)
        self.button.configure(text="در حال محاسبه")
        self.displayBox.configure(state="normal")
        app.update()

        for ip_address in ip_addresses:
            output = subprocess.run(["ping", "-n", "5", ip_address], stdout=subprocess.PIPE, text=True).stdout

            if "Lost" in output:
                loss_percentage = int(output.split("(")[1].split("%")[0])
                loss_percentages.append(loss_percentage)

            output_lines = output.splitlines()
            output_string = "\n".join(output_lines[-4:])
            self.displayBox.insert(END, output_string + "\n")
            status_bar_progress += 1 / (len(ip_addresses) + 1)
            self.progressbar.set(status_bar_progress)
            app.update()

        self.pingedLabel.configure(text=f"{st.results.ping} ms")
        self.downloadedLabel.configure(text=f"{round(st.download() / 1000 / 1000, 1)} Mbit/s")
        self.uploadedLabel.configure(text=f"{round(st.upload() / 1000 / 1000, 1)} Mbit/s")

        self.displayBox.configure(state="disable")
        self.button.configure(text="در حال محاسبه")
        status_bar_progress += 1 / (len(ip_addresses) + 1)
        self.progressbar.set(status_bar_progress)
        app.update()

        return loss_percentages

    def start_ping_thread(self):
        selected_option = self.ServerSelection.get()
        if selected_option == "Global":
            host_list = HOSTLIST['global'].tolist()
        elif selected_option == "Intranet":
            host_list = HOSTLIST['intranet'].tolist()
        elif selected_option == "Filtering":
            host_list = HOSTLIST['filtered'].tolist()

        threading.Thread(target=self.get_ping, args=(host_list,), daemon=True).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
