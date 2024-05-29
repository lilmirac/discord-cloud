document.addEventListener("DOMContentLoaded", function() {
    const fileDrag = document.getElementById("file-drag");
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileDrag.addEventListener(eventName, preventDefaults, false);
    });
    ['dragenter', 'dragover'].forEach(eventName => {
        fileDrag.addEventListener(eventName, highlight, false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
        fileDrag.addEventListener(eventName, unhighlight, false);
    });
    fileDrag.addEventListener('drop', handleDrop, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight() {
    const fileDrag = document.getElementById("file-drag");
    fileDrag.classList.add('highlight');
}

function unhighlight() {
    const fileDrag = document.getElementById("file-drag");
    fileDrag.classList.remove('highlight');
}

function handleDrop(e) {
    const files = e.dataTransfer.files;
    const fileUpload = document.getElementById("file-upload");
    fileUpload.files = files;
}

document.getElementById("upload-form").addEventListener("submit", function(event) {
    event.preventDefault();
    submitForm();
});

async function submitForm() {
    const fileUpload = document.getElementById("file-upload");
    if (fileUpload.files.length === 0) {
        alert("No file selected for upload.");
        return;
    }
    const formData = new FormData(document.getElementById("upload-form"));
    const fileName = fileUpload.files[0].name;
    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        if (response.ok) {
            alert(`${fileName} uploaded successfully!`);
            location.reload();
        } else {
            throw new Error("Network response was not ok");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', async function(event) {
        const fileName = this.getAttribute('data-file-name');
        const confirmDelete = confirm(`Are you sure you want to delete ${fileName}?`);
        if (confirmDelete) {
            const messageId = this.getAttribute('data-message-id');
            try {
                const checkResponse = await fetch(`/check-file/${messageId}`);
                if (!checkResponse.ok) {
                    alert(`Error: file does not exist.`);
                    location.reload();
                    return;
                }
            } catch (error) {
                console.error('Error checking file existence:', error);
                alert(`Error checking file existence.`);
                return;
            }
            try {
                const response = await fetch(`/delete/${messageId}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    this.parentNode.remove();
                } else {
                    console.error('Failed to delete file');
                }
            } catch (error) {
                console.error('Error deleting file:', error);
            }
        }
    });
});
