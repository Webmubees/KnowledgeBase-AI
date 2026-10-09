
const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const selectedFile = document.getElementById("selected-file");
const uploadButton = document.getElementById("upload-button");

const documentsList = document.getElementById("documents-list");
const documentCount = document.getElementById("document-count");
const refreshButton = document.getElementById("refresh-documents");

const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const appStatus = document.getElementById("app-status");

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"];


// --------------------------------
// Display status messages
// --------------------------------

function showStatus(message, isError = false) {
    appStatus.textContent = message;
    appStatus.classList.toggle("error", isError);
}


// --------------------------------
// Create safe text elements
// --------------------------------

function createTextElement(tag, className, text) {
    const element = document.createElement(tag);

    element.className = className;
    element.textContent = text;

    return element;
}


// --------------------------------
// Load and display documents
// --------------------------------

async function loadDocuments() {
    documentsList.replaceChildren(
        createTextElement("p", "muted small", "Loading documents...")
    );

    try {
        const response = await fetch("/documents");

        if (!response.ok) {
            throw new Error("Could not load documents.");
        }

        const data = await response.json();

        documentCount.textContent = data.total;
        documentsList.replaceChildren();

        if (data.documents.length === 0) {
            documentsList.append(
                createTextElement(
                    "p",
                    "muted small",
                    "No documents yet. Upload your first file above."
                )
            );
            return;
        }

        for (const doc of data.documents) {
            const card = document.createElement("article");
            card.className = "document-card";

            const top = document.createElement("div");
            top.className = "document-top";

            const icon = createTextElement(
                "span",
                "file-icon",
                doc.file_type.toUpperCase()
            );

            const info = document.createElement("div");
            info.className = "document-info";

            info.append(
                createTextElement("div", "document-name", doc.filename)
            );

            info.append(
                createTextElement(
                    "div",
                    "document-meta",
                    `${doc.file_type.toUpperCase()} document`
                )
            );

            top.append(icon, info);

            const bottom = document.createElement("div");
            bottom.className = "document-bottom";

            const status = createTextElement(
                "span",
                `status-label ${doc.status}`,
                doc.status.replace("_", " ")
            );

            const deleteButton = createTextElement(
                "button",
                "delete-button",
                "Delete"
            );

            deleteButton.type = "button";

            deleteButton.addEventListener("click", async () => {
                await deleteDocument(doc.filename);
            });

            bottom.append(status, deleteButton);
            card.append(top, bottom);
            documentsList.append(card);
        }
    } catch (error) {
        documentsList.replaceChildren(
            createTextElement(
                "p",
                "muted small",
                error.message || "Unable to load documents."
            )
        );
    }
}


// --------------------------------
// Upload a document
// --------------------------------

fileInput.addEventListener("change", () => {
    selectedFile.textContent = fileInput.files[0]
        ? fileInput.files[0].name
        : "No file selected";
});

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];

    if (!file) {
        showStatus("Please choose a document first.", true);
        return;
    }

    const extension = file.name
        .slice(file.name.lastIndexOf("."))
        .toLowerCase();

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
        showStatus("Only PDF, DOCX, and TXT files are supported.", true);
        return;
    }

    if (file.size === 0) {
        showStatus("The selected file is empty.", true);
        return;
    }

    if (file.size > MAX_FILE_SIZE) {
        showStatus("The maximum file size is 10 MB.", true);
        return;
    }

    uploadButton.disabled = true;
    uploadButton.textContent = "Uploading and indexing...";
    showStatus("Uploading document. Indexing may take some time.");

    try {
        const formData = new FormData();

        formData.append("file", file);

        const response = await fetch("/documents/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Document upload failed."
            );
        }

        uploadForm.reset();
        selectedFile.textContent = "No file selected";

        showStatus(`${data.filename} uploaded and indexed successfully.`);
        await loadDocuments();
    } catch (error) {
        showStatus(
            error.message || "An error occurred during upload.",
            true
        );
    } finally {
        uploadButton.disabled = false;
        uploadButton.textContent = "Upload and index";
    }
});


// --------------------------------
// Delete a document
// --------------------------------

async function deleteDocument(filename) {
    const confirmed = window.confirm(
        `Are you sure you want to delete "${filename}"?`
    );

    if (!confirmed) {
        return;
    }

    showStatus(`Deleting ${filename}...`);

    try {
        const response = await fetch(
            `/documents/${encodeURIComponent(filename)}`,
            { method: "DELETE" }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Document deletion failed.");
        }

        showStatus(`${filename} deleted successfully.`);
        await loadDocuments();
    } catch (error) {
        showStatus(error.message || "Unable to delete the document.", true);
    }
}

refreshButton.addEventListener("click", loadDocuments);


// --------------------------------
// Chat message helpers
// --------------------------------

function addMessage(role, text, sources = []) {
    const message = document.createElement("article");
    message.className = `message ${role}`;

    message.append(
        createTextElement(
            "div",
            "message-label",
            role === "user" ? "You" : "KnowledgeBase AI"
        )
    );

    message.append(
        createTextElement("div", "message-text", text)
    );

    if (sources.length > 0) {
        const sourceList = document.createElement("div");
        sourceList.className = "source-list";

        // Deduplicate citations for display.
        // PDFs are grouped by filename and page.
        // TXT/DOCX sources are grouped by filename.
        const uniqueSources = new Map();

        for (const source of sources) {
            const key = source.page != null
                ? `${source.source}:page:${source.page}`
                : source.source;

            if (!uniqueSources.has(key)) {
                uniqueSources.set(key, source);
            }
        }

        for (const source of uniqueSources.values()) {
            let label = source.source;

            if (source.page != null) {
                label += ` · Page ${source.page}`;
            }

            const chip = createTextElement(
                "span",
                "source-chip",
                label
            );

            sourceList.append(chip);
        }

        message.append(sourceList);
    }

    chatMessages.append(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;
}


// --------------------------------
// Send a chat question
// --------------------------------

async function sendQuestion(question) {
    const cleanQuestion = question.trim();

    if (!cleanQuestion) {
        return;
    }

    chatMessages.querySelector(".welcome-card")?.remove();

    addMessage("user", cleanQuestion);

    questionInput.value = "";
    questionInput.disabled = true;
    sendButton.disabled = true;

    const loadingMessage = addMessage(
        "assistant",
        "Searching your documents and generating an answer..."
    );

    showStatus("");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: cleanQuestion
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "The chat request failed.");
        }

        loadingMessage.remove();

        addMessage(
            "assistant",
            data.answer,
            data.sources || []
        );
    } catch (error) {
        loadingMessage.remove();

        addMessage(
            "assistant",
            error.message || "Unable to get an answer. Please try again."
        );
    } finally {
        questionInput.disabled = false;
        sendButton.disabled = false;
        questionInput.focus();
    }
}

chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendQuestion(questionInput.value);
});

document.querySelectorAll("[data-question]").forEach((button) => {
    button.addEventListener("click", () => {
        sendQuestion(button.dataset.question);
    });
});


// --------------------------------
// Initial application load
// --------------------------------

loadDocuments();
