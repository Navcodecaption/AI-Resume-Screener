# 🚀 Live Deployment Guide

## Option 1: Streamlit Cloud (Recommended - FREE & EASY)

### Step 1: GitHub Repository Ready
✅ Already done! Your code is at: https://github.com/kunwardhruv/AI-Resume-Screener

### Step 2: Streamlit Cloud Setup

1. **Streamlit Cloud pe jao:**
   - https://share.streamlit.io/ pe jao
   - "Sign in" click karo
   - GitHub account se login karo

2. **New App Create Karo:**
   - "New app" button click karo
   - Settings:
     - **Repository**: `kunwardhruv/AI-Resume-Screener`
     - **Branch**: `main`
     - **Main file path**: `app.py`
     - **App URL**: (auto-generate hoga, ya custom name de sakte ho)
   
3. **Advanced Settings (Optional):**
   - Python version: 3.10
   - Secrets: (agar environment variables chahiye)

4. **Deploy!**
   - "Deploy" button click karo
   - 2-3 minutes me app live ho jayega!

### Step 3: Access Your App
- Streamlit Cloud apko ek URL dega: `https://your-app-name.streamlit.app`
- Ye URL share kar sakte ho kisi ko bhi!

---

## Option 2: Other Platforms

### Railway.app (Alternative)
1. https://railway.app pe jao
2. "New Project" → "Deploy from GitHub repo"
3. Repository select karo
4. Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
5. Start command: `streamlit run app.py --server.port $PORT`

### Render.com (Alternative)
1. https://render.com pe jao
2. "New Web Service" → GitHub repo connect karo
3. Settings:
   - Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

## ⚠️ Important Notes

1. **First Deployment Time:**
   - Models download honge (spaCy, sentence-transformers)
   - 5-10 minutes lag sakte hain pehli baar

2. **Memory Requirements:**
   - Streamlit Cloud free tier: 1GB RAM (sufficient hai)
   - Agar memory issue aaye, to model size optimize karo

3. **File Upload Limits:**
   - Streamlit Cloud: 200MB per file
   - Resume files usually small hote hain, so no issue

4. **Environment Variables:**
   - Agar API keys chahiye, Streamlit Cloud secrets use karo

---

## 🔧 Troubleshooting

### Issue: "Module not found"
**Solution**: `requirements.txt` me sab dependencies check karo

### Issue: "spaCy model not found"
**Solution**: Deployment me `python -m spacy download en_core_web_sm` command add karo

### Issue: "Out of memory"
**Solution**: 
- Smaller model use karo
- Or upgrade to paid tier

---

## ✅ Deployment Checklist

- [ ] GitHub repository public hai
- [ ] `requirements.txt` updated hai
- [ ] `app.py` main file hai
- [ ] `.streamlit/config.toml` created (optional)
- [ ] Streamlit Cloud account created
- [ ] App deployed successfully
- [ ] Test kiya - upload resume, analyze kiya

---

**Best Option: Streamlit Cloud - Free, Easy, Fast! 🎉**

