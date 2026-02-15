# 📘 Project Overview

The **Smart Contract Summary & Q&A Assistant** is a specialized **RAG (Retrieval-Augmented Generation)** app to help users interact with long documents like contracts, insurance policies, and legal reports. Using **LLM pipelines**, it supports smooth document ingestion and conversational querying with built-in guardrails.

---

## 🚀 Key Features

- **Multi-Format Ingestion:** Upload PDF and DOCX files.  
- **Intelligent RAG Pipeline:** Extracts, chunks, and embeds content for precise retrieval.  
- **Conversational AI:** Interactive chat interface with conversation tracking.  
- **Factuality & Safety:** Guardrails ensure grounded answers and citations.  
- **Automated Summarization:** Optional high-level summaries for complex contracts.

---

## 🛠️ Technology Stack

| Component        | Technology Used                   |
|-----------------|----------------------------------|
| Framework        | LangChain, LangServe, FastAPI    |
| Frontend         | Gradio UI                        |
| Vector Store     | Chroma or FAISS                  |
| Embeddings       | SentenceTransformers or OpenAI   |
| Parsing          | PyMuPDF, pdfplumber, python-docx |

---

## 🏗️ Architecture & Workflow

1. **Ingestion:** Upload, parse, and split files into chunks.  
2. **Storage:** Convert chunks into embeddings and store in vector DB.  
3. **Retrieval:** Perform semantic search to find relevant sections.  
4. **Generation:** LLM generates answers using retrieved context with citations.

---

# 📘 نظرة عامة على المشروع

مساعد **تلخيص العقود الذكية والأسئلة والأجوبة** هو تطبيق متخصص يعتمد على تقنية **RAG** لمساعدة المستخدمين على التعامل مع مستندات طويلة مثل العقود، بوالص التأمين، والتقارير القانونية. باستخدام **LLM pipelines**، يمكن استيعاب المستندات والدردشة معها مع ضوابط أمان مدمجة.

---

## 🚀 الميزات الرئيسية

- **دعم صيغ متعددة:** رفع ملفات PDF و DOCX.  
- **خط معالجة ذكي (RAG):** استخراج النصوص، تقسيمها، وتحويلها إلى **Embeddings** لدقة الاسترجاع.  
- **ذكاء اصطناعي تفاعلي:** واجهة دردشة مع تتبع حالة الحوار.  
- **المصداقية والأمان:** ضوابط لضمان إجابات واقعية مع ذكر المصادر.  
- **تلخيص تلقائي:** ميزة اختيارية لتوليد ملخصات للعقود المعقدة.

---

## 🛠️ الأدوات والتقنيات

| المكون          | التقنية المستخدمة                |
|----------------|---------------------------------|
| إطار العمل      | LangChain, LangServe, FastAPI  |
| واجهة المستخدم  | Gradio UI                       |
| مخزن المتجهات   | Chroma أو FAISS                 |
| تمثيل البيانات | SentenceTransformers أو OpenAI  |
| تحليل الملفات  | PyMuPDF, pdfplumber, python-docx|

---

## 🏗️ الهيكلية وسير العمل

1. **الاستيعاب (Ingestion):** رفع الملفات، تحليلها، وتقسيمها لأجزاء صغيرة.  
2. **التخزين (Storage):** تحويل الأجزاء إلى تمثيلات رقمية وتخزينها في قاعدة بيانات متجهة.  
3. **الاسترجاع (Retrieval):** البحث الدلالي لإيجاد الأجزاء المتعلقة بسؤال المستخدم.  
4. **التوليد (Generation):** نموذج اللغة ينشئ الإجابة بناءً على السياق مع توثيق المصادر.

