import threading

class Utils:
    class error(Exception):
        def __init__(self, message):
            super().__init__(f"Error: {message}")

    @staticmethod
    def setInterval(action, interval_ms):
        def setIntervalHelper(wrapper):
            action()
            wrapper.timer = threading.Timer(interval_ms / 1000, setIntervalHelper, [wrapper])
            wrapper.timer.start()

        class Wrapper:
            def __init__(self):
                self.timer = None

            def cancel(self):
                if self.timer is not None:
                    self.timer.cancel()

        wrapper = Wrapper()
        setIntervalHelper(wrapper)
        return wrapper
