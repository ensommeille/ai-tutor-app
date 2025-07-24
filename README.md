# 后端启动流程
## 首次启动
1. 确保已安装 Python 3.11 及以上版本。
2. 安装项目依赖：
   - 进入 `backend` 目录。
   - 执行 `pip install -r requirements.txt` 安装依赖。
3. 配置环境变量：
   - 进入 `.env` 文件。
   - 添加 `DEEPSEEK_API_KEY` 变量，值为你的 Deepseek API 密钥。
   - 添加 `DEEPSEEK_ENDPOINT` 变量，值为 Deepseek API 端点 URL。
4. 启动后端服务：
   ```
   uvicorn app.main:app --reload --host 0.0.0.0--port 8000
   ```
## 后续启动
- 直接运行 `uvicorn app.main:app --reload` 即可启动后端服务。
- 确保 `.env` 文件中的 API 密钥和端点 URL 配置正确。

# 前端启动流程
- 进入 `frontend` 目录。
- 运行 `python -m http.server 8080` 启动前端服务。
- 浏览器访问 `http://localhost:8080` 即可使用 AI 错题订正助手。
