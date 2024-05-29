document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', document.getElementById('file-upload').files[0]);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    document.getElementById('upload-result').style.display = 'block';
    document.getElementById('uploaded-filename').innerText = data.filename;
});
