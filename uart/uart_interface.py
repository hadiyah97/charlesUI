import uart

class UartInterface:
    def __enter__(self):
        self.uart_obj = uart.Uart()
        print("in interface\n")
        return self.uart_obj

    def __exit__(self, exc_type, exc_value, traceback):
        self.uart_obj.cleanup()