const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('audioFile');
const fileInfo = document.getElementById('fileInfo');
const predictBtn = document.getElementById('predictBtn');
const result = document.getElementById('result');
const emotionLabel = document.getElementById('emotionLabel');
const loader = document.getElementById('loader');
const errorMsg = document.getElementById('errorMsg');

let selectedFile = null;

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

function handleFile(file) {
  if (!file.name.endsWith('.wav')) {
    showError('Please upload a .wav file only.');
    return;
  }
  selectedFile = file;
  fileInfo.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
  fileInfo.classList.remove('hidden');
  predictBtn.disabled = false;
  result.classList.add('hidden');
  errorMsg.classList.add('hidden');
}

predictBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  loader.classList.remove('hidden');
  result.classList.add('hidden');
  errorMsg.classList.add('hidden');
  predictBtn.disabled = true;

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('/predict', { method: 'POST', body: formData });
    const data = await response.json();

    if (data.emotion) {
      emotionLabel.textContent = data.emotion;
      result.classList.remove('hidden');
    } else {
      showError(data.error || 'Something went wrong.');
    }
  } catch (err) {
    showError('Could not connect to server. Make sure app.py is running.');
  } finally {
    loader.classList.add('hidden');
    predictBtn.disabled = false;
  }
});

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove('hidden');
}
