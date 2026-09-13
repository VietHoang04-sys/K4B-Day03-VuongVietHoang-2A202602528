# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Điền Họ và Tên]  
> **Mã Sinh Viên / Mã Học viên:** [Điền MSSV]  
> **Chủ đề Lựa chọn:** Agent tìm kiếm và đặt phòng tại Vinpearl

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **5 / 5** | Agent phải trích xuất địa điểm, ngày nhận/trả phòng, số khách, sau đó tìm phòng phù hợp và chỉ tiến hành đặt khi khách đã chọn loại phòng và cung cấp đủ thông tin liên hệ. |
| **2. Tool Interaction** | **5 / 5** | Agent sử dụng MCP Server để gọi hai tool chuyên biệt: `search_rooms` tra cứu phòng trống và `book_room` tạo booking; kết quả được trả về từ execution layer thay vì do agent tự suy đoán. |
| **3. Dynamic Decision** | **5 / 5** | Hành động tiếp theo phụ thuộc vào Observation: nếu có phòng thì tư vấn lựa chọn, nếu không có phòng thì thông báo `NOT_FOUND`, nếu đủ thông tin mới gọi `book_room`, còn thiếu dữ liệu thì yêu cầu khách bổ sung. |
| **4. Long Horizon Goal** | **4 / 5** | Agent duy trì mục tiêu hoàn tất đặt phòng qua chuỗi tìm kiếm → lựa chọn → xác nhận thông tin → booking, đồng thời giữ nhất quán địa điểm, thời gian và số khách trong toàn bộ phiên. |
| **TỔNG ĐIỂM AGENTIC FIT** | **19 / 20** | *Agent đặt phòng Vinpearl có mức độ phù hợp rất cao với kiến trúc Agentic System vì kết hợp suy luận đa bước, gọi tool và ra quyết định theo trạng thái phòng thực tế.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_rooms",
    "arguments": {
      "location": "Vinpearl Nha Trang",
      "check_in": "2026-10-01",
      "check_out": "2026-10-03",
      "adults": 2,
      "children": 0
    },
    "observation": {
      "status": "SUCCESS",
      "location": "Vinpearl Nha Trang",
      "check_in": "2026-10-01",
      "check_out": "2026-10-03",
      "rooms": [
        {
          "room_type": "Deluxe Ocean View",
          "capacity": 2,
          "price_per_night": 2500000,
          "available": 5
        }
      ]
    },
    "latency_ms": 120.5
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** ___ / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** ___ lượt.
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
