##  📖 fs_TTS_for_yuedu：为开源阅读软件打造的 Fish Speech 中转服务器

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)

本项目是一个轻量级中转服务器，利用 [Fish Speech (FS)](https://github.com/fishaudio/fish-speech) 项目为开源阅读软件提供高质量的文本转语音 (TTS) 功能。

### ✨ 特色

* **简易搭建**: 完全使用 Python 开发，模拟 WebSocket Secure (WSS) 提交，部署轻松便捷。
* **双音色朗读**: 支持为文本的正常部分和引号内的部分使用不同的音色朗读，增强朗读表现力。只需在提交请求时同时附带 `speaker`  `speaker2` 参数即可体验。
* **高效音频处理**: 利用 FFmpeg 将 WAV 格式音频转换为 MP3 格式，大幅缩小传输体积，提升效率。

### 🚀 快速上手

1. **克隆项目**: 将本仓库克隆到您的计算机。
2. **安装ffmpeg** 请您自行搜索如何在您使用的系统上安装ffmpeg。
3. **安装依赖**: 在项目根目录下，打开终端并执行 `pip install -r requirements.txt` 安装所需依赖。
4. **启动服务器**: 在终端输入 `uvicorn main:app --host 0.0.0.0` 启动项目。

### ⚙️ 配置选项

* **端口**: 使用 `--port` 参数指定脚本监听的端口，例如 `uvicorn main:app --host 0.0.0.0 --port 8080`。
* **多线程**: 使用 `--worker` 参数指定多线程启动，例如 `uvicorn main:app --host 0.0.0.0 --worker 4`，以优化性能。

### ⚠️  注意事项

* **FFmpeg 依赖**: 本项目需要系统已安装 FFmpeg 以进行音频格式转换。请自行搜索如何在您的系统上安装 FFmpeg。
* **请求方式**: 项目目前仅接受 POST 请求。
* **文本长度**:  建议在阅读软件内对过长的文本进行处理，以避免潜在问题。
* **并发率**:  在阅读软件内导入 TTS 服务器时，建议将并发率参数设置为大于 1 的值，以提高生成音频的连贯性，并减少生成速度慢于朗读速度的情况。
* **应该如何在开源阅读构建url?**: 'http(s)://your_ip:your_port/process?text={{java.encodeURI(speakText)}}&speaker=角色_ZH(&speaker2=角色2_ZH)'
### 🤝 兼容性

本项目针对当前版本的 Fish Speech 做了一些调整，例如：

* `speed` 参数暂时无效，无法修改朗读速度。
* 对提交的文本进行了少量预处理。

## 🎉 欢迎贡献

欢迎提交 issue 和 pull request，一起完善本项目！ 
