"""Tool schemas and execution functions for the Vinpearl booking assistant."""

import json
from datetime import date, datetime
from typing import Any, Dict, Optional


TOOLS_SCHEMA = [
    {
        "name": "search_rooms",
        "description": (
            "Tìm các loại phòng Vinpearl còn trống theo địa điểm, ngày nhận "
            "phòng, ngày trả phòng và số lượng khách."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Địa điểm/khu nghỉ Vinpearl, ví dụ 'Vinpearl Nha Trang'.",
                },
                "check_in": {
                    "type": "string",
                    "description": "Ngày nhận phòng theo định dạng YYYY-MM-DD.",
                },
                "check_out": {
                    "type": "string",
                    "description": "Ngày trả phòng theo định dạng YYYY-MM-DD.",
                },
                "adults": {
                    "type": "integer",
                    "description": "Số người lớn.",
                    "minimum": 1,
                },
                "children": {
                    "type": "integer",
                    "description": "Số trẻ em.",
                    "minimum": 0,
                },
            },
            "required": ["location", "check_in", "check_out", "adults"],
        },
    },
    {
        "name": "book_room",
        "description": "Đặt phòng Vinpearl sau khi người dùng đã chọn loại phòng.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Địa điểm/khu nghỉ Vinpearl.",
                },
                "room_type": {
                    "type": "string",
                    "description": "Tên loại phòng muốn đặt.",
                },
                "check_in": {
                    "type": "string",
                    "description": "Ngày nhận phòng theo định dạng YYYY-MM-DD.",
                },
                "check_out": {
                    "type": "string",
                    "description": "Ngày trả phòng theo định dạng YYYY-MM-DD.",
                },
                "adults": {
                    "type": "integer",
                    "description": "Số người lớn.",
                    "minimum": 1,
                },
                "children": {
                    "type": "integer",
                    "description": "Số trẻ em.",
                    "minimum": 0,
                },
                "guest_name": {
                    "type": "string",
                    "description": "Họ tên khách đứng tên đặt phòng.",
                },
                "phone": {
                    "type": "string",
                    "description": "Số điện thoại liên hệ của khách.",
                },
            },
            "required": [
                "location",
                "room_type",
                "check_in",
                "check_out",
                "adults",
                "guest_name",
                "phone",
            ],
        },
    },
]


MOCK_ROOMS = {
    "vinpearl nha trang": [
        {"room_type": "Deluxe Ocean View", "capacity": 2, "price_per_night": 2500000, "available": 5},
        {"room_type": "Family Suite", "capacity": 4, "price_per_night": 4200000, "available": 2},
    ],
    "vinpearl phu quoc": [
        {"room_type": "Deluxe Garden View", "capacity": 2, "price_per_night": 2800000, "available": 4},
        {"room_type": "Family Villa", "capacity": 6, "price_per_night": 6500000, "available": 1},
    ],
    "vinpearl da nang": [
        {"room_type": "Deluxe Ocean View", "capacity": 2, "price_per_night": 2300000, "available": 3},
        {"room_type": "Pool Villa", "capacity": 4, "price_per_night": 5500000, "available": 2},
    ],
}


def _result(status: str, **payload: Any) -> str:
    return json.dumps({"status": status, **payload}, ensure_ascii=False)


def _parse_stay(check_in: str, check_out: str) -> tuple[Optional[date], Optional[str]]:
    try:
        start = datetime.strptime(check_in, "%Y-%m-%d").date()
        end = datetime.strptime(check_out, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None, "Ngày nhận/trả phòng phải theo định dạng YYYY-MM-DD."
    if start < date.today():
        return None, "Ngày nhận phòng không được ở trong quá khứ."
    if end <= start:
        return None, "Ngày trả phòng phải sau ngày nhận phòng."
    return start, None


def _validate_guests(adults: int, children: int) -> Optional[str]:
    if not isinstance(adults, int) or isinstance(adults, bool) or adults < 1:
        return "Số người lớn phải là số nguyên dương."
    if not isinstance(children, int) or isinstance(children, bool) or children < 0:
        return "Số trẻ em phải là số nguyên không âm."
    return None


def _find_rooms(location: str, check_in: str, check_out: str, adults: int, children: int):
    _, date_error = _parse_stay(check_in, check_out)
    if date_error:
        return None, date_error
    guest_error = _validate_guests(adults, children)
    if guest_error:
        return None, guest_error
    rooms = MOCK_ROOMS.get(location.strip().lower())
    if rooms is None:
        return None, f"Chưa có dữ liệu phòng cho Vinpearl tại '{location}'."
    guests = adults + children
    return [room for room in rooms if room["available"] > 0 and room["capacity"] >= guests], None


def execute_search_rooms(
    location: str,
    check_in: str,
    check_out: str,
    adults: int,
    children: int = 0,
) -> str:
    """Tra cứu phòng Vinpearl phù hợp với một khoảng thời gian."""
    rooms, error = _find_rooms(location, check_in, check_out, adults, children)
    if error:
        return _result("INVALID_REQUEST", message=error)
    if not rooms:
        return _result(
            "NOT_FOUND",
            message="Không tìm thấy phòng Vinpearl phù hợp với yêu cầu.",
            location=location,
            check_in=check_in,
            check_out=check_out,
        )
    return _result(
        "SUCCESS",
        location=location,
        check_in=check_in,
        check_out=check_out,
        rooms=rooms,
    )


def execute_book_room(
    location: str,
    room_type: str,
    check_in: str,
    check_out: str,
    adults: int,
    guest_name: str,
    phone: str,
    children: int = 0,
) -> str:
    """Đặt một phòng Vinpearl trong dữ liệu mô phỏng."""
    rooms, error = _find_rooms(location, check_in, check_out, adults, children)
    if error:
        return _result("INVALID_REQUEST", message=error)
    if not guest_name.strip() or not phone.strip():
        return _result("INVALID_REQUEST", message="Cần cung cấp họ tên và số điện thoại liên hệ.")

    selected = next(
        (room for room in rooms if room["room_type"].casefold() == room_type.strip().casefold()),
        None,
    )
    if selected is None:
        return _result("NOT_FOUND", message=f"Loại phòng '{room_type}' hiện không còn phù hợp hoặc không tồn tại.")

    nights = (datetime.strptime(check_out, "%Y-%m-%d").date() -
              datetime.strptime(check_in, "%Y-%m-%d").date()).days
    booking_id = f"VP-{location.strip().upper().replace(' ', '-')[:12]}-{check_in.replace('-', '')}"
    return _result(
        "SUCCESS",
        booking_id=booking_id,
        location=location,
        room_type=selected["room_type"],
        check_in=check_in,
        check_out=check_out,
        nights=nights,
        total_price=selected["price_per_night"] * nights,
        guest_name=guest_name.strip(),
        phone=phone.strip(),
        message=f"Đặt phòng thành công tại {location} cho {guest_name.strip()}.",
    )


TOOL_ROUTER = {
    "search_rooms": execute_search_rooms,
    "book_room": execute_book_room,
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Định tuyến và thực thi một tool theo tên được MCP server yêu cầu."""
    tool = TOOL_ROUTER.get(tool_name)
    if tool is None:
        return _result("UNKNOWN_TOOL", error=f"Tool '{tool_name}' không tồn tại.")
    try:
        return tool(**arguments)
    except TypeError as exc:
        return _result("INVALID_REQUEST", error=f"Tham số gọi tool không hợp lệ: {exc}")
