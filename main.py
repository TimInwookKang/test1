import time
import signal
import os
import sys
import keyboard

class LogComponent:
    def __init__(self, directory: str):
        self.directory = directory
        self.yesterday = 999
        #check if the logger is writing string to the file
        self.writing = False
        # Interrupt handler
        self.interrupt= 0
        keyboard.add_hotkey('q+a', self.signal_handler_1)
        keyboard.add_hotkey('q+b', self.signal_handler_2)
    
    def signal_handler_1(self):
        self.interrupt = 1
        print(self.interrupt)
    
    def signal_handler_2(self):
        print("Interrupting writing")
        self.interrupt = 2
        print(self.interrupt)
    

    def timestamp(self):
        now = 1970 + time.time()/(60*60 * 24 *365.25)
        year = int(now)
        month = int((now % 1) * 12 + 1)
        day =(now - year)*365.25 + 1
        months = [31, int(year % 4 == 0 )+ 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for m in range(month -1):
            day -= months[m]
        hour = (day % 1) * 24
        minutes = hour % 1 * 60
        seconds = minutes % 1 * 60
        day = int(day)
        hour = int(hour)
        minutes = int(minutes)
        seconds = int(seconds)
        return "%d-%02d-%02d %02d:%02d:%02d" % (year, month, day, hour, minutes, seconds), year, month, day, hour, minutes, seconds

    def write(self, text : str, time_stamp : tuple, file : str):
        self.writing = True
        print(time_stamp + "\n" + "Writing text to file")
        with open(os.path.join(self.directory, file), "a") as file:
            file.write(time_stamp + "\n")
            for char in text:
                if self.interrupt == 2:
                    print('Writing cancelled.')
                    return                    
                file.write(char)
            file.write("\n")
        self.writing = False
        print("Text written to file")
    
    def log(self):
        while True:
            writable = False
            while (not writable):
                if self.interrupt > 0:
                    return
                try:
                    text = input("Enter text to be logged: ")
                    writable = True
                except:
                    print("Invalid input, text not written to file.")
            time_stamp = self.timestamp()
            today = time_stamp[3]
            if (today != self.yesterday):
                print("Logging to a new file")
                file = "log_%d-%02d-%02d.txt" % (time_stamp[1], time_stamp[2], time_stamp[3])
            else:
                print("Logging to the same file")
                file = file

            self.write(text, time_stamp[0], file)
            if self.interrupt > 0:
                print("Quitting the program")
                return

            self.yesterday = today

def main():
    logger = LogComponent("./Desktop")
    logger.log()
    print("program finished")

if __name__ == "__main__":
    main()
