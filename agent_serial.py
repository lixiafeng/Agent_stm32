import os
import sys

import serial
from openai import OpenAI


# 与STM32程序保持一致
SERIAL_PORT = "COM7"
BAUD_RATE = 115200
MODEL = "deepseek-flash"


def create_client():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：没有设置 DEEPSEEK_API_KEY")
        print('请先执行：set DEEPSEEK_API_KEY=你的DeepSeek_API_Key')
        sys.exit(1)

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )


def ask_agent(client, user_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是STM32控制命令分类器。"
                    "如果用户提到LED或灯，并要求翻转、切换、打开或关闭，"
                    "你必须只回答LED_TOGGLE。"
                    "其他情况只回答UNKNOWN。"
                ),
            },
            {
                "role": "user",
                "content": user_text,
            },
        ],
        max_tokens=100,
        reasoning_effort="none",
        extra_body={"thinking": {"type": "disabled"}},
    )

    return response.choices[0].message.content.strip()


def main():
    client = create_client()

    try:
        stm32 = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
        )
    except serial.SerialException as error:
        print(f"无法打开串口 {SERIAL_PORT}：{error}")
        print("请确认串口号正确，并关闭串口助手。")
        sys.exit(1)

    print(f"已连接STM32：{SERIAL_PORT}，{BAUD_RATE} baud")
    print("输入控制命令，例如：翻转LED")
    print("输入 exit 退出")

    try:
        while True:
            user_text = input("\n你：").strip()

            if user_text.lower() in {"exit", "quit"}:
                break
            if not user_text:
                continue

            try:
                command = ask_agent(client, user_text)
                print("Agent原始结果：", repr(command))

                if "LED_TOGGLE" in command.upper():
                    stm32.reset_input_buffer()
                    stm32.write(b"\x01")
                    stm32.flush()

                    reply = stm32.read(1)

                    if reply == b"\x01":
                        print("STM32：执行成功，LED已翻转")
                    else:
                        print("STM32：已发送0x01，但没有收到回传确认")
                else:
                    print("Agent未生成有效的LED控制命令")

            except Exception as error:
                print(f"Agent调用失败：{error}")

    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        stm32.close()


if __name__ == "__main__":
    main()
