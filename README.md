# 🎙️ PodcastAI Platform v3

### *Autonomous Multi-Agent Content Repurposing Engine*

PodcastAI is a  end-to-end automation platform that transforms YouTube podcasts into high-quality blog posts, social media threads, and newsletters. It features a multi-tenant architecture, autonomous event-driven scheduling, and a Retrieval-Augmented Generation (RAG) memory system.

---
## To check out the Demo, when reviewer runs please login through these credentials:
##      Mail:gummakondanithinreddy@gmail.com
##      password:Nithin@12!

---
##  Why i Built This

The "Content Repurposing" process is typically a high-friction bottleneck for creators. For every 1-hour podcast, a human usually spends 4–6 hours writing articles, social posts, and newsletters.

**PodcastAI solves this by:**
- **Reducing Cost:** Uses local LLMs (Ollama) to eliminate per-token costs.
- **Ensuring Consistency:** RAG ensures the AI doesn't hallucinate outside of the creator's established niche.
- **Removing Friction:** The scheduler means the creator only needs to upload to YouTube; the rest happens automatically.
- **Human-in-the-Loop:** Unlike "black box" automations, the UI allows creators to provide feedback and iterate on content versions before publishing.

---

### Prerequisites
- **Python 3.10+**
- **Ollama:** [Download here](https://ollama.com/)

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Setup AI Models
PodcastAI uses high-performance local models. Run these commands to download them:
```powershell
ollama pull phi3              # For logic and writing
ollama pull nomic-embed-text  # For RAG memory
```

### 4. Configuration
Create a `.env` file (one is provided by default) and update your security keys:
```env
SECRET_KEY=your-jwt-secret
ENCRYPTION_KEY=your-fernet-key
```

### 5. Run the Platform
```powershell
streamlit run app.py
```


