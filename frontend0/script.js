let selectedRole = null;
let selectedMode = null;

document.getElementById("student-btn").addEventListener("click", () => {
  selectedRole = "student"; showFunctionSelection();
});
document.getElementById("teacher-btn").addEventListener("click", () => {
  selectedRole = "teacher"; showFunctionSelection();
});
document.getElementById("parent-btn").addEventListener("click", () => {
  selectedRole = "parent"; showFunctionSelection();
});

document.getElementById("upload-wrong-btn").addEventListener("click", () => {
  selectedMode = "wrong"; showUploadSection();
});
document.getElementById("upload-difficult-btn").addEventListener("click", () => {
  selectedMode = "no-idea"; showUploadSection();
});

document.getElementById("submit-btn").addEventListener("click", async () => {
  const file = document.getElementById("upload-file").files[0];
  if (!file || !selectedRole || !selectedMode) {
    alert("请完整选择身份、功能并上传图片！");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);
  formData.append("mode", selectedMode);
  formData.append("role", selectedRole);

  try {
    const res = await fetch("http://localhost:8000/api/tutor/solve", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    showOutput(data.answer);
  } catch (e) {
    showOutput("错误：" + e.message);
  }
});

function showFunctionSelection() {
  document.getElementById("function-selection").style.display = "block";
  document.getElementById("upload-section").style.display = "none";
  document.getElementById("output-area").style.display = "none";
}
function showUploadSection() {
  document.getElementById("upload-section").style.display = "block";
  document.getElementById("output-area").style.display = "none";
}
function showOutput(text) {
  document.getElementById("output-area").style.display = "block";
  document.getElementById("output-box").textContent = text;
}
