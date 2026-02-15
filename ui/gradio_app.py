import gradio as gr
from pathlib import Path
import shutil

from app.config import DOCS_DIR
from app.ingestion import ingest
from app.qa_chain import ask


def handle_question(question: str, history: list) -> tuple:
    if not question.strip():
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": "Please enter a question."})
        return history, ""

    try:
        result = ask(question)
        answer = result["answer"]

        if result["sources"]:
            answer += "\n\n**Sources:**\n"
            for i, src in enumerate(result["sources"], 1):
                meta = src.get("metadata", {})
                source_name = meta.get("source", "Unknown")
                answer += f"  {i}. `{Path(source_name).name}`\n"

        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
    except FileNotFoundError:
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content":
            "**Vector store not found!**\n\n"
            "Please upload documents and click **Ingest Documents** first."
        })
    except Exception as e:
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": f"**Error:** {str(e)}"})

    return history, ""


def handle_upload(files) -> str:
    if not files:
        return "No files selected."

    docs_path = Path(DOCS_DIR)
    docs_path.mkdir(parents=True, exist_ok=True)

    uploaded = []
    for file in files:
        dest = docs_path / Path(file.name).name
        shutil.copy2(file.name, dest)
        uploaded.append(Path(file.name).name)

    return f"Uploaded {len(uploaded)} file(s):\n" + "\n".join(f"  - {f}" for f in uploaded)


def handle_ingest() -> str:
    try:
        chunks_count = ingest()
        return f"**Ingestion complete!**\n\n{chunks_count} chunks stored in vector store."
    except FileNotFoundError as e:
        return f"**Error:** {str(e)}"
    except ValueError as e:
        return f"**Warning:** {str(e)}"
    except Exception as e:
        return f"**Error:** {str(e)}"


def list_documents() -> str:
    docs_path = Path(DOCS_DIR)
    if not docs_path.exists():
        return "No documents directory found."

    files = list(docs_path.iterdir())
    if not files:
        return "No documents found. Please upload some files."

    file_list = []
    for f in sorted(files):
        if f.is_file():
            size_kb = f.stat().st_size / 1024
            file_list.append(f"  - **{f.name}** ({size_kb:.1f} KB)")

    return f"**{len(file_list)} document(s):**\n" + "\n".join(file_list)


APP_CSS = """
.main-header {
    text-align: center;
    margin-bottom: 1rem;
}
.main-header h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.2rem;
}
"""

APP_THEME = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
)


def create_app() -> gr.Blocks:
    with gr.Blocks(title="Smart Contract Assistant") as app:

        gr.HTML("""
        <div class="main-header">
            <h1>Smart Contract Assistant</h1>
            <p style="color: #6b7280; font-size: 1.1rem;">
                AI-powered Q&A for Solidity & Smart Contract Development
            </p>
        </div>
        """)

        with gr.Tabs():
            with gr.Tab("Ask Questions", id="qa"):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=450,
                    placeholder="Ask me anything about smart contracts...",
                )

                with gr.Row():
                    question_input = gr.Textbox(
                        label="Your Question",
                        placeholder="e.g., What is a reentrancy attack?",
                        scale=5,
                        show_label=False,
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)

                gr.Examples(
                    examples=[
                        "What is a smart contract?",
                        "Explain the reentrancy vulnerability",
                        "How to use OpenZeppelin SafeMath?",
                        "What is the difference between memory and storage in Solidity?",
                    ],
                    inputs=question_input,
                    label="Example Questions",
                )

                send_btn.click(
                    handle_question,
                    inputs=[question_input, chatbot],
                    outputs=[chatbot, question_input],
                )
                question_input.submit(
                    handle_question,
                    inputs=[question_input, chatbot],
                    outputs=[chatbot, question_input],
                )

            with gr.Tab("Manage Documents", id="docs"):
                gr.Markdown("### Upload & Ingest Documents")
                gr.Markdown(
                    "Upload `.pdf`, `.txt`, `.md`, or `.sol` files, "
                    "then click **Ingest** to process them."
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        file_upload = gr.File(
                            label="Upload Documents",
                            file_count="multiple",
                            file_types=[".pdf", ".txt", ".md", ".sol"],
                        )
                        upload_btn = gr.Button("Upload Files", variant="secondary")
                        upload_status = gr.Markdown(label="Upload Status")

                    with gr.Column(scale=1):
                        ingest_btn = gr.Button(
                            "Ingest Documents",
                            variant="primary",
                            size="lg",
                        )
                        ingest_status = gr.Markdown(label="Ingestion Status")

                gr.Markdown("---")
                refresh_btn = gr.Button("Refresh Document List")
                docs_list = gr.Markdown(value=list_documents())

                upload_btn.click(handle_upload, inputs=[file_upload], outputs=[upload_status])
                ingest_btn.click(handle_ingest, outputs=[ingest_status])
                refresh_btn.click(list_documents, outputs=[docs_list])

    return app
