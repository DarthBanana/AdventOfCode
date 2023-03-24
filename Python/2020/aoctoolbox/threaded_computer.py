import threading



class ThreadedComputerEnvironment:
    def __init__(self, computer, name, start_event = None):
        self.computer = computer  
        self.name = name      
        self.start_event = start_event
        self.thread = None
        #threading.Thread(target=self._run_computer, args=(computer,), daemon=True)
        self.verbose = False
        self.wait_for_signal = False

    def _run_computer(self):
        if self.wait_for_signal:
            print("Computer", self.name, "waiting to start...")
            self.start_event.wait()
        
        print("Computer", self.name, "starting")
        while (self.computer.can_continue()):
            self.computer.run()
        print("Computer", self.name, "exiting")
        
    def run_now(self, verbose = False):

        self.thread = threading.Thread(target=self._run_computer, daemon=True)
        self.wait_for_signal = False
        self.thread.start()
    
    def run_on_signal(self):
        self.thread = threading.Thread(target=self._run_computer, daemon=True)
        self.wait_for_signal = True
        self.thread.start()
    
    
