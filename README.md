# 📘 Smart Contract Assistant

**Smart Contract Assistant** is a **RAG (Retrieval-Augmented Generation)** application for interacting with smart contract documents. Upload Solidity files, PDFs, or text documents and ask questions — the AI retrieves relevant context and gives accurate, sourced answers.

---

## 🚀 Key Features

- **Multi-Format Ingestion:** Upload `.pdf`, `.txt`, `.md`, and `.sol` files
- **RAG Pipeline:** Chunks documents, embeds them using Google Gemini, and stores in a vector database
- **Conversational AI:** Chat interface powered by Google Gemini LLM
- **Dual Interface:** Gradio UI for users + FastAPI for programmatic access
- **Cloud Embeddings:** Uses Google Gemini Embeddings (auto-detects available model)

---

## 🛠️ Technology Stack

| Component       | Technology                          |
|----------------|-------------------------------------|
| Framework       | LangChain, FastAPI                  |
| LLM             | Google Gemini (`gemini-2.5-flash`)  |
| Frontend        | Gradio UI                           |
| Vector Store    | FAISS                               |
| Embeddings      | Google Gemini Embeddings (`gemini-embedding-001`) |
| Document Parsing| PyPDFLoader, TextLoader             |



## 🏗️ How It Works

1. **Ingestion:** Documents are loaded, split into chunks (1000 chars, 200 overlap)
2. **Embedding:** Chunks are embedded using Google Gemini Embeddings
3. **Storage:** Embeddings are stored in a FAISS vector store on disk
4. **Retrieval:** User question is embedded → top 4 similar chunks retrieved
5. **Generation:** Gemini LLM generates an answer using the retrieved context



## 📘 نظرة عامة

**مساعد العقود الذكية** هو تطبيق يعتمد على تقنية **RAG** للتفاعل مع مستندات العقود الذكية. ارفع ملفات Solidity أو PDF أو نصوص واسأل أسئلة — الذكاء الاصطناعي يسترجع السياق المناسب ويعطيك إجابات دقيقة.

### الأدوات والتقنيات

| المكون          | التقنية المستخدمة                              |
|----------------|-----------------------------------------------|
| إطار العمل      | LangChain, FastAPI                            |
| نموذج اللغة    | Google Gemini (`gemini-2.5-flash`)            |
| واجهة المستخدم  | Gradio UI                                     |
| مخزن المتجهات   | FAISS                                         |
| تمثيل البيانات | Google Gemini Embeddings (`gemini-embedding-001`) |
| تحليل الملفات  | PyPDFLoader, TextLoader                       |

### سير العمل

1. **الاستيعاب:** رفع الملفات وتقسيمها لأجزاء صغيرة
2. **التمثيل:** تحويل الأجزاء لـ embeddings باستخدام Google Gemini Embeddings
3. **التخزين:** حفظ الـ embeddings في FAISS على القرص
4. **الاسترجاع:** سؤال المستخدم يتحول لـ embedding → يتم استرجاع أقرب 4 أجزاء
5. **التوليد:** Gemini LLM ينشئ الإجابة بناءً على السياق المسترجع
