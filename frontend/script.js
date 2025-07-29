// 页面元素
const identitySelection = document.getElementById('identity-selection');
const functionSelection = document.getElementById('function-selection');
const uploadSection = document.getElementById('upload-section');
const resultsContainer = document.getElementById('results-container');
const resultImageContainer = document.getElementById('result-image-container');
const resultText = document.getElementById('result-text');
const resultMeta = document.querySelector('.result-meta');
const newQueryBtn = document.getElementById('new-query-btn');
const outputBox = document.getElementById('output-box'); // 保留用于兼容性

// 选择身份
let selectedIdentity = '';

// 角色按钮元素
const identityButtons = [
  document.getElementById('student-btn'),
  document.getElementById('teacher-btn'),
  document.getElementById('parent-btn')
];

// 为每个角色按钮添加点击事件
identityButtons.forEach(btn => {
  btn.onclick = () => {
    // 移除所有按钮的active类
    identityButtons.forEach(b => b.classList.remove('active'));
    // 为当前点击按钮添加active类
    btn.classList.add('active');
    selectedIdentity = btn.id.replace('-btn', '');
  };
});

// 选择功能
// 功能按钮元素
const functionButtons = [
  document.getElementById('upload-wrong-btn'),
  document.getElementById('upload-difficult-btn')
];

// 为每个功能按钮添加点击事件
functionButtons.forEach(btn => {
  btn.onclick = () => {
    // 移除所有按钮的active类
    functionButtons.forEach(b => b.classList.remove('active'));
    // 为当前点击按钮添加active类
    btn.classList.add('active');
    handleUpload(btn.id.includes('wrong') ? 'wrong' : 'difficult');
  };
});

// 上传文件后
// 添加文件选择input元素
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = 'image/*';
fileInput.style.display = 'none';
document.body.appendChild(fileInput);

// 图片选择处理
function chooseImage() {
  fileInput.value = '';
  fileInput.click();
}

// 文件选择变化事件
fileInput.onchange = function(e) {
  if (e.target.files && e.target.files.length > 0) {
    selectedImage = e.target.files[0];
    console.log('图片选择成功:', selectedImage.name, '大小:', selectedImage.size);
    showMessage(`图片选择成功: ${selectedImage.name}`);
    // 显示图片预览
    const previewContainer = document.getElementById('image-preview-container');
    previewContainer.innerHTML = ''; // 清空现有预览
    
    const imgPreview = document.createElement('img');
    imgPreview.style.maxWidth = '300px';
    imgPreview.style.maxHeight = '200px';
    imgPreview.style.border = '1px solid #ddd';
    imgPreview.style.borderRadius = '4px';
    imgPreview.style.padding = '5px';
    
    const reader = new FileReader();
    reader.onload = function(e) {
      imgPreview.src = e.target.result;
    };
    reader.readAsDataURL(selectedImage);
    previewContainer.appendChild(imgPreview);
    
    // 显示已选图片名称
    const fileNameEl = document.createElement('div');
    fileNameEl.id = 'selected-file-name';
    fileNameEl.textContent = `已选择: ${selectedImage.name}`;
    fileNameEl.style.marginTop = '10px';
    fileNameEl.style.color = '#666';
    // 移除之前的文件名显示
    const oldFileNameEl = document.getElementById('selected-file-name');
    if (oldFileNameEl) oldFileNameEl.remove();
    uploadSection.appendChild(fileNameEl);
  } else {
    selectedImage = null;
    showMessage('未选择图片');
    console.log('用户取消了图片选择');
  }
};

// 显示消息提示
function showMessage(text) {
  // 创建简单的消息提示元素
  const messageEl = document.createElement('div');
  messageEl.textContent = text;
  messageEl.style.position = 'fixed';
  messageEl.style.top = '50%';
  messageEl.style.left = '50%';
  messageEl.style.transform = 'translate(-50%, -50%)';
  messageEl.style.padding = '10px 20px';
  messageEl.style.backgroundColor = 'rgba(0,0,0,0.7)';
  messageEl.style.color = 'white';
  messageEl.style.borderRadius = '4px';
  messageEl.style.zIndex = '1000';
  document.body.appendChild(messageEl);
  
  // 1秒后移除提示
  setTimeout(() => messageEl.remove(), 1000);
}

// 提交按钮点击事件 - 调用后端API
document.getElementById('submit-btn').onclick = async () => {
  // 验证所有必要参数
  if (!selectedIdentity) {
    showMessage('请先选择身份');
    loadingEl.remove();
    return;
  }
  if (!uploadType) {
    showMessage('请先选择功能类型');
    loadingEl.remove();
    return;
  }
  if (!selectedImage) {
    showMessage('请先选择图片');
    loadingEl.remove();
    return;
  }

  // 显示加载状态
  const loadingEl = document.createElement('div');
  loadingEl.textContent = '正在处理...';
  loadingEl.style.position = 'fixed';
  loadingEl.style.top = '50%';
  loadingEl.style.left = '50%';
  loadingEl.style.transform = 'translate(-50%, -50%)';
  loadingEl.style.padding = '10px 20px';
  loadingEl.style.backgroundColor = 'rgba(0,0,0,0.7)';
  loadingEl.style.color = 'white';
  loadingEl.style.borderRadius = '4px';
  loadingEl.style.zIndex = '1000';
  document.body.appendChild(loadingEl);

  const formData = new FormData();
  formData.append("image", selectedImage); // 确认字段名以匹配后端要求
  formData.append("mode", uploadType);
  formData.append("role", selectedIdentity);

  try {
    // 调试日志：确认FormData内容
    console.log('上传文件:', selectedImage);
    for (let pair of formData.entries()) {
      console.log('FormData字段:', pair[0], pair[1]);
    }
    
    // 添加请求超时
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30秒超时

const res = await fetch("http://localhost:8000/api/tutor/solve", {
  method: "POST",
  body: formData,
  signal: controller.signal
});

clearTimeout(timeoutId);
console.log('后端响应状态:', res.status);

if (!res.ok) {
  throw new Error(`上传失败: HTTP状态码 ${res.status}`);
}

// 显示结果容器  
resultsContainer.style.display = 'block';
resultText.innerHTML = ''; // 清空现有内容



// 处理流式响应
loadingEl.style.display = 'none';
  const reader = res.body.getReader();
const decoder = new TextDecoder();
let fullAnswer = '';

resultMeta.textContent = `处理中... ${new Date().toLocaleString()}`;

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value, { stream: true });
    fullAnswer += chunk;
    // 使用marked.js渲染完整Markdown内容
    resultText.innerHTML = marked.parse(fullAnswer);
    // 自动滚动到底部
    resultText.scrollTop = resultText.scrollHeight;
}

// 处理完成
resultMeta.textContent = `处理完成: ${new Date().toLocaleString()}`;
  } catch (e) {
      console.error('上传过程错误:', e);
      // 显示错误信息在结果界面
      uploadSection.style.display = 'none';
      resultsContainer.style.display = 'block';
      resultText.innerHTML = `<div class='error-message'>上传失败: ${e.message}</div>`;
      resultImageContainer.innerHTML = '';
      resultMeta.textContent = `错误发生时间: ${new Date().toLocaleString()}`;
    }
};

let selectedImage = null; // 存储选中的图片对象

let uploadType = '';  // 用来存储上传的类型（错误的题目或难题）

// 新查询按钮事件
newQueryBtn.onclick = function() {
  // 重置所有状态
  resultsContainer.style.display = 'none';
  identitySelection.style.display = 'block';
  selectedIdentity = '';
  uploadType = '';
  selectedImage = null;
  resultText.innerHTML = '';
  resultImageContainer.innerHTML = '';
  resultMeta.textContent = '';
  // 移除可能存在的文件名显示
  const fileNameEl = document.getElementById('selected-file-name');
  if (fileNameEl) fileNameEl.remove();
};

function handleUpload(type) {
  uploadType = type;
  uploadSection.style.display = 'block';
  // chooseImage(); // 自动触发图片选择
}
