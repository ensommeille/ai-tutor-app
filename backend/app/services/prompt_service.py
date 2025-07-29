
import os
from pathlib import Path

def build_prompt(mode: str, role: str, content: str) -> str:
    # 映射mode到prompt文件关键词
    mode_map = {"difficult": "不会做", "wrong": "做错了"}
    # 映射role到prompt文件关键词
    role_map = {"student": "学生视角", "teacher": "老师视角", "parent": "家长视角"}
    # 构建prompt文件路径
    prompt_dir = Path(__file__).resolve().parent.parent.parent.parent / "prompts"
    filename = f"{role_map.get(role, '学生视角')}{mode_map.get(mode, '做错了')}.txt"
    file_path = prompt_dir / filename
    
    # 读取prompt文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prefix = f.read()
    except FileNotFoundError:
        raise ValueError(f"找不到对应的prompt文件: {file_path}")
    
    return f"{prefix} \n题目如下：\n{content} \n 请直接给出按给定格式的结构化解答"
