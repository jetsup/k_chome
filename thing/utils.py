from serial.tools import list_ports
import serial
from .models import Boards

# global variable to store the boards that are connected
global boards_database # type: dict[dict]


def read_port(port: serial.Serial) -> str:
    print(port.read().decode("utf-8"), end="")
    return port.read().decode("utf-8")


def write_port(port: serial.Serial, data: str) -> int | None:
    written_data = port.write(data.encode("utf-8"))
    print(f"Written {written_data} bytes to port")
    return written_data


# a function that will run in the thread to detect when a board is plugged in
def detect_board(boards_database: dict[dict]):
    device_list = list_ports.comports()
    for device in device_list:
        if device.vid != None or device.pid != None:
            port = device.device
            vid = "{:04X}".format(device.vid)
            pid = "{:04X}".format(device.pid)
            print(f"Port\t: {port}\nVID\t: {vid}\nPID\t: {pid}")
            # check if the board is already in database
            if (vid, pid) in boards_database and boards_database[(vid, pid)][
                "is_connected"
            ] == False:
                # connect to the board
                stored_board = Boards.objects.get(vid=vid, pid=pid)
                try:
                    board = serial.Serial(port, stored_board.baudrate, timeout=1)
                    boards_database[(vid, pid)]["port"] = board
                    boards_database[(vid, pid)]["is_connected"] = True
                    print(f"Connected to board at port {port}")
                except serial.SerialException as e:
                    print(f"Failed to connect to board at port {port}. E: {e}")
    return boards_database
