"""Minh hoạ FUNCTION CALLING thuần với OpenRouter API (OpenAI-compatible).

Tool `get_weather` được định nghĩa schema thủ công VÀ thực thi ngay trong
chính file app này. Model chỉ QUYẾT ĐỊNH gọi tool nào; app mới là nơi chạy.

Cách chạy:
    pip install -r ../requirements.txt
    export OPENROUTER_API_KEY=...
    python weather_function_calling.py
"""

import json
import os
from openai import OpenAI

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY or "dummy_key",
)

# Có thể cấu hình bất kỳ model nào trên OpenRouter
MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash")

SYSTEM_INSTRUCTION = (
    "Bạn là trợ lý thời tiết thân thiện, trả lời bằng tiếng Việt tự nhiên. "
    "Dùng emoji phù hợp (🌧️ 🌤️ 💨 💧). "
    "Tóm tắt ngắn gọn, dễ hiểu, và đưa ra lời khuyên thực tế "
    "(ví dụ: mang ô, mặc áo mỏng, ...)."
)

# 1. App tự định nghĩa schema của tool (chuẩn JSON schema / OpenAI Tool Format)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Lấy thời tiết hiện tại của một thành phố",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Tên thành phố (ví dụ: Hà Nội, Hồ Chí Minh, Đà Nẵng)"
                    }
                },
                "required": ["city"],
            },
        },
    }
]


# 2. App tự thực thi tool (trong thực tế sẽ gọi API thời tiết thật)
def get_weather(city: str) -> str:
    """Trả về thời tiết (mock) của *city*. Dùng làm tool cho model."""
    mock_data = {
        "Hà Nội": {
            "nhiệt_độ": "29°C",
            "thời_tiết": "trời mưa nhẹ",
            "độ_ẩm": "82%",
            "gió": {"hướng": "Đông Nam", "tốc_độ": "12 km/h"},
        },
        "Hồ Chí Minh": {
            "nhiệt_độ": "33°C",
            "thời_tiết": "mưa rào",
            "độ_ẩm": "75%",
            "gió": {"hướng": "Tây Nam", "tốc_độ": "15 km/h"},
        },
        "Đà Nẵng": {
            "nhiệt_độ": "30°C",
            "thời_tiết": "nhiều mây",
            "độ_ẩm": "78%",
            "gió": {"hướng": "Đông", "tốc_độ": "10 km/h"},
        },
    }
    default = {"nhiệt_độ": "28°C", "thời_tiết": "không có dữ liệu chi tiết"}
    return json.dumps({"city": city, **mock_data.get(city, default)}, ensure_ascii=False)


def run(prompt: str) -> str:
    """Gửi *prompt* tới OpenRouter, tự động xử lý function calling và trả về câu trả lời cuối."""
    if not OPENROUTER_API_KEY:
        print("⚠️  OPENROUTER_API_KEY chưa được thiết lập!")
        print("    Vui lòng chạy: export OPENROUTER_API_KEY='sk-or-v1-...'")
        return "Chưa cấu hình OPENROUTER_API_KEY."

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": prompt}
    ]

    # 3. Gọi model — model quyết định có gọi tool hay không
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    msg = resp.choices[0].message

    # 4. Vòng lặp: nếu model yêu cầu tool, app TỰ THỰC THI rồi đưa kết quả trả lại
    while msg.tool_calls:
        # Thêm phản hồi của model vào lịch sử hội thoại
        messages.append(msg)

        for tc in msg.tool_calls:
            func_name = tc.function.name
            func_args = json.loads(tc.function.arguments)
            print(f"  [model yêu cầu] {func_name}({func_args})")
            
            if func_name == "get_weather":
                result = get_weather(**func_args)  # <-- app chạy, không phải model
            else:
                result = json.dumps({"error": f"Unknown tool {func_name}"})
                
            print(f"  [app thực thi]  -> {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": func_name,
                "content": result,
            })

        # Gửi kết quả tool trả về cho model
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        msg = resp.choices[0].message

    # 5. Model tổng hợp câu trả lời cuối
    return msg.content or ""


if __name__ == "__main__":
    question = "Thời tiết Hà Nội và Đà Nẵng hôm nay thế nào?"
    print(f"User: {question}\n")
    print("Trả lời:", run(question))
