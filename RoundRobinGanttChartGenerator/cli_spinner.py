import multiprocessing
import time

class CLI_Spinner:
    def __init__(self, message="", speed = 0.1) -> None:
        self.message=message
        self.speed=speed

        #Multithreating 
        self.process = multiprocessing. Process( # the actual displaying of the spinni thing
            target= self.spin,
            args=(),
            name="CLI Spinner"
        )

    def spin(self):
        spinner =  ["|","/","-","\\"] # this loops through 
        n=0
        x=0
        loading = ["","|||","||||||","|||||||||"]
        l=0 # increments of 5
        progress= 0
        while True:
            print(f"\r{self.message}{loading[l]}{spinner[n]}", end="") ##"\r" is ascii to take the cursors back to the beginning of a line
                         ## Typing over the previous one
            n +=1
            x +=1
            progress+=1
            if x > 45:#3/3*10:
                l=3
            elif x > 25: #2/3*10:
                l=2
            elif x > 10:#1/3*10:
                l=1
            if n>= len(spinner):
                n = 0
            time.sleep(self.speed)# the timer....            
                        
    def start(self):
        #.start() form the multiprocessing library
        self.process.start() #a process from multiprocessing library has two commands .start() and .terminate()

    def stop(self):
        if not self.process.is_alive():
            print("Warning: CLI spinner not running.")
        else:
            #.terminate() form the multiprocessing library
            self.process.terminate()
            print()
        
if __name__ == "__main__":
    spinner = CLI_Spinner("Loading:", 0.2)
    spinner.start()
    print("Program Logic...")
    time.sleep(10)
    print(f"\r|||||||||")
    print("Process Complete")
    spinner.stop()
