from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from datetime import datetime
from thing.models import Things, Boards
from k_api.serializers import BoardsSerializer
from django.contrib.auth.decorators import login_required
from celery_background.tasks import listen_usb_serial_ports
from django.contrib import messages


@login_required
def home(request: HttpRequest) -> HttpResponse:
    things = Things.objects.all()
    print(f"Things: {things}")
    return render(
        request, "index.html", {"year": datetime.now().year, "things": things}
    )


@login_required
def boards(request: HttpRequest) -> HttpResponse:
    boards = Boards.objects.all()
    connected_boards = listen_usb_serial_ports()

    online_boards = []

    for board in boards:
        key = f"{board.vid},{board.pid}"
        if key in connected_boards:
            online_boards.append(
                {"board": board, "port": connected_boards[key], "online": True}
            )
        else:
            online_boards.append({"board": board, "port": "N/A", "online": False})

    print(f"Boards: {online_boards}")
    return render(
        request,
        "boards.html",
        {"year": datetime.now().year, "boards": online_boards},
    )


def online_boards(request: HttpRequest) -> HttpResponse:
    boards = Boards.objects.all()
    connected_boards = listen_usb_serial_ports()

    serializer = BoardsSerializer(boards, many=True)
    serialized_data = serializer.data

    for data in serialized_data:
        key = f"{data['vid']},{data['pid']}"
        if key in connected_boards:
            data["port"] = connected_boards[key]
            data["online"] = True
        else:
            data["port"] = "N/A"
            data["online"] = False

    print(f"Serialized Boards: {serializer.data}")

    return JsonResponse(serializer.data, safe=False)


@login_required
def add_board(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST

        board_name = data.get("board-name")
        if not board_name:
            messages.error(request, "Board name is required")
            return redirect("board-add")

        description = data.get("description")

        vid_pid = data.get("device")
        if not vid_pid:
            messages.error(request, "Device is required")
            return redirect("board-add")

        vid = vid_pid.split(",")[0]
        pid = vid_pid.split(",")[1]

        baudrate = data.get("baudrate")
        if not baudrate or not baudrate.isnumeric():
            messages.error(request, "Baudrate is required and must be a number")
            return redirect("board-add")

        data_format = data.get("data-format")
        if not data_format:
            messages.error(request, "Data format is required")
            return redirect("board-add")

        data_headers = data.get("data-headers")
        if not data_headers:
            messages.error(request, "Data headers is required")
            return redirect("board-add")
        try:
            board = Boards.objects.create(
                name=board_name,
                description=description,
                vid=vid,
                pid=pid,
                baudrate=int(baudrate),
                data_format=data_format,
                data_headers=data_headers,
            )
        except Exception as e:
            messages.error(request, f"Error creating board: {e}")
            return redirect("board-add")
        board.save()
        return redirect("boards")

    connected_devices: dict[dict] = (
        listen_usb_serial_ports()
    )  # {"vid,pid": "/dev/ttyUSB0", ...}
    devices_in_database = Boards.objects.all()
    unconnected_device = {}

    for device_key, _ in connected_devices.items():
        board = Boards.objects.filter(
            vid=device_key.split(",")[0], pid=device_key.split(",")[1]
        )
        if not board:
            unconnected_device[device_key] = connected_devices[device_key]

    print(f"\t>Unconnected Devices: {unconnected_device}")

    return render(
        request,
        "board_add.html",
        {"year": datetime.now().year, "devices": unconnected_device},
    )


@login_required
def update_board(request: HttpRequest, pk: int) -> HttpResponse:
    board = Boards.objects.get(pk=pk)
    if request.method == "POST":
        data = request.POST

        print(f"Data: {data}")

        board_name = data.get("board-name")
        if not board_name:
            messages.error(request, "Board name is required")
            return redirect("board-update", pk=pk)

        description = data.get("description")

        baudrate = data.get("baudrate")
        if not baudrate or not baudrate.isnumeric():
            messages.error(request, "Baudrate is required and must be a number")
            return redirect("board-update", pk=pk)

        data_format = data.get("data-format")
        if not data_format:
            messages.error(request, "Data format is required")
            return redirect("board-update", pk=pk)

        data_headers = data.get("data-headers")
        if not data_headers:
            messages.error(request, "Data headers is required")
            return redirect("board-update", pk=pk)

        try:
            board.name = board_name
            board.description = description
            board.baudrate = int(baudrate)
            board.data_format = data_format
            board.data_headers = data_headers
            board.save()
        except Exception as e:
            messages.error(request, f"Error updating board: {e}")
            return redirect("board-update", pk=pk)

        # navigate to previous page if available
        previous_url = request.META.get("HTTP_REFERER")

        if previous_url:
            return redirect(previous_url)

        return redirect("boards")

    # GET
    board = Boards.objects.get(pk=pk)
    connected_boards: dict = listen_usb_serial_ports()

    print(f"Connected Boards: {connected_boards}")

    for connected_board, _ in connected_boards.items():
        if connected_board == f"{board.vid},{board.pid}":
            print(f"Connected Board: {connected_board}, {_}")
            break

    return render(
        request,
        "board_details.html",
        {
            "year": datetime.now().year,
            "board": board,
            "connected_boards": connected_boards,
        },
    )


@login_required
def delete_board(request: HttpRequest, pk: int) -> HttpResponse:
    board = Boards.objects.get(pk=pk)
    board.delete()
    return redirect("boards")
