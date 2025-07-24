
def build_prompt(mode: str, role: str, content: str) -> str:
    if mode == "no-idea":
        prefix = {
            "teacher": "你是一位数学老师，请为以下题目提供详细教学讲解：",
            "student": "请用引导式语言解释以下题目：",
            "parent": "请用通俗方式告诉家长如何讲解以下题目："
        }[role]
    else:
        prefix = {
            "teacher": "你是一位老师，请分析学生解题错误并纠正：",
            "student": "请指出解题错误，并鼓励性指导改正：",
            "parent": "请告诉家长孩子错在哪里，并给出建议："
        }[role]
    return f"{prefix}\n\n{content}\n\n请给出完整结构化解答。"
