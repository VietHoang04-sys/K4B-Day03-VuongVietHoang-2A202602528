# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Vương Việt Hoàng
> **Mã Sinh Viên / Mã Học viên:** 2A202602528
> **Chủ đề Lựa chọn:** Trợ lý lên gợi ý lịch trình du lịch và đặt phòng Vinpearl

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** |5 / 5 | Agent phải trích xuất địa điểm, ngày nhận/trả phòng, số khách, sau đó tìm phòng phù hợp và chỉ tiến hành đặt khi khách đã chọn loại phòng và cung cấp đủ thông tin liên hệ.|
| **2. Tool Interaction** |5 / 5 | Agent sử dụng MCP Server để gọi hai tool chuyên biệt: `search_rooms` tra cứu phòng trống và `book_room` tạo booking; kết quả được trả về từ execution layer thay vì do agent tự suy đoán.|
| **3. Dynamic Decision** |5 / 5 |Hành động tiếp theo phụ thuộc vào Observation: nếu có phòng thì tư vấn lựa chọn, nếu không có phòng thì thông báo `NOT_FOUND`, nếu đủ thông tin mới gọi `book_room`, còn thiếu dữ liệu thì yêu cầu khách bổ sung. |
| **4. Long Horizon Goal** |4 / 5 |Agent duy trì mục tiêu hoàn tất đặt phòng qua chuỗi tìm kiếm → lựa chọn → xác nhận thông tin → booking, đồng thời giữ nhất quán địa điểm, thời gian và số khách trong toàn bộ phiên. |
| **TỔNG ĐIỂM AGENTIC FIT** | **19/ 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Tìm phòng Vinpearl Nha Trang từ 01/10/2026 đến 03/10/2026 cho 10 người lớn.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_rooms",
    "arguments": {
      "location": "Vinpearl Nha Trang",
      "adults": 10,
      "check_in": "2026-10-01",
      "check_out": "2026-10-03",
      "children": 0
    },
    "observation": {
      "status": "NOT_FOUND",
      "message": "Không tìm thấy phòng Vinpearl phù hợp với yêu cầu.",
      "location": "Vinpearl Nha Trang",
      "check_in": "2026-10-01",
      "check_out": "2026-10-03"
    },
    "latency_ms": 3136.96
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [y] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5/ 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt.
- **Kết quả đẩy Repo nộp bài:** [y ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
