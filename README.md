# DeepSeek STM32 Agent

这个项目把用户输入交给DeepSeek判断，并通过串口控制STM32翻转LED。

## 数据流程

用户输入 -> DeepSeek -> Python发送0x01 -> STM32翻转LED -> STM32回传0x01

## 与STM32代码的约定

- 串口：COM7
- 波特率：115200
- 数据位：8
- 停止位：1
- 校验：无
- `0x01`：翻转LED
- STM32执行后回传`0x01`

现有STM32代码已经符合该约定，无需修改。

## 使用方法

### 1. 安装Python

建议使用Python 3.10或更高版本。

### 2. 安装依赖

在项目目录打开命令提示符：

```bat
pip install -r requirements.txt
```

### 3. 设置DeepSeek API Key

仅对当前命令提示符窗口有效：

```bat
set DEEPSEEK_API_KEY=你的DeepSeek_API_Key
```

不要在等号两侧添加空格，也不要把API Key写入Python源代码。

### 4. 关闭串口助手

串口助手和本程序不能同时占用COM7。

### 5. 启动

```bat
python agent_serial.py
```

也可以双击`start.bat`，但需要先在系统环境变量中配置`DEEPSEEK_API_KEY`。

输入示例：

```text
帮我切换一下LED
```

正常结果：

```text
Agent： LED_TOGGLE
STM32：执行成功，LED已翻转
```

## 修改串口号

如果设备管理器显示的不是COM7，请修改`agent_serial.py`：

```python
SERIAL_PORT = "COM7"
```

## 常见错误

- `PermissionError`：串口正在被串口助手等程序占用。
- 找不到COM7：串口号不正确，或者USB转串口没有连接。
- `401`：DeepSeek API Key错误。
- 没有执行确认：检查STM32是否已烧录、波特率是否为115200，以及TX/RX/GND连接。
