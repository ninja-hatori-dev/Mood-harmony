## In the SERVER directory

### 1. Environment Setup
```
python -m venv env
source env/bin/activate  # Use "env\\Scripts\\activate" on Windows
pip install -r requirements.txt
```

### 2. Create a `.env` file as mentioned in `.example.env`
```env
GOOGLE_API_KEY=
```

### 3. Run the `mood_recommendation.py` file
```
python mood_recommendation.py
```

---

## In the CLIENT directory

### 1. Environment Setup
```
npm install
```

### 2. Create a `.env` file as mentioned in `.example.env`
```env
VITE_SERVER_API=(write the URL where the backend is running)
```

### 3. Run the application
```
npm run dev
