import sim800l

class SimModule:
    def __init__(self, port="/dev/serial0"):
        self.sim = sim800l.SIM800L(port)

    def send_message(self, message):
        """Send a message via SIM800L"""
        self.sim.send_sms('+18325382561', message)

    def get_sig_strength(self):
        """Get the Signal Strength of 2G to the Sim Card"""
        return self.sim.get_signal_strength()