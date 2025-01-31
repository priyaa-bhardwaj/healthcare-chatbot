## 🏥 AI-Powered Healthcare Chatbot  
This is a **Django-based API** for a **healthcare chatbot** that helps users diagnose symptoms and provides possible remedies. It uses **LMStudio’s locally hosted LLaMA model** to generate responses based on user queries.  

### 🚀 Features  
- Allows users to ask health-related questions  
- Uses a **locally hosted LLaMA model** via LMStudio for generating responses  
- Stores all **user queries and responses** in a database  
- Provides an **appointment booking system**  

---

### Technologies Used
**Django**: Web framework for building the backend.
**Django REST Framework (DRF):** Used for creating API endpoints.
**LMStudio:** Provides the language model for generating chatbot responses.
**SQLite:** For storing user data, questions, and chatbot responses.

## 🛠️ Setup Instructions  

### 1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-username/healthcare-chatbot.git  
cd healthcare-chatbot
```

### 2️⃣ **Create a Virtual Environment** (Optional but recommended)  
```bash
python -m venv venv  
source venv/bin/activate  # For macOS/Linux  
venv\Scripts\activate      # For Windows  
```

### 3️⃣ **Install Dependencies**  
Ensure all required packages (including `requests`) are installed using:  
```bash
pip install -r requirements.txt  
```

---

## 🏗️ How the LLM Model is Accessed  

This project integrates **LMStudio’s LLaMA model** as a **local API endpoint**. The model is **hosted locally** and accessed at:  

```
http://127.0.0.1:1234
```

### **API Request to the LLaMA Model**  

When a user submits a health-related query, the chatbot calls the **locally running LLaMA model** using an HTTP `POST` request.  

#### **📌 Code Snippet (Integration with LLaMA Model)**
```python
import requests
import json

class ChatBot(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            question = serializer.validated_data["question"]

            # Call LMStudio's LLaMA model
            response = self.get_llama_response(question)

            # Store the response in the database
            chat = Question.objects.create(user=user, question=question, answer=response)

            return Response({"question": question, "answer": response}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_llama_response(self, question):
        url = "http://127.0.0.1:1234/v1/completions"  # LMStudio's API
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "llama-3.2-1b-instruct",  # Your LMStudio model identifier
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 250
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException:
            return "Error: Unable to connect to LLaMA model. Please check the server."
```

### **📝 Prompt Used for the Model**
```python
prompt = f"""
        You are a healthcare chatbot designed to provide possible cause and remedy for both physical and mental health symptoms.  
        Your responses should be short along with **medically safe, research-backed, and concise**.  
        In addition to identifying possible causes and remedies, consider the user's behavior, stress levels, and emotional well-being.  
        If a symptom is serious or suggests a mental health crisis, advise the user to consult a doctor or mental health professional.  

        User: {question}  
        AI: *Possible Cause:* [Identify potential medical, lifestyle, or psychological reasons]  
        AI: *Remedy:* [Provide safe treatments, self-care tips, and coping strategies]  

        - If symptoms suggest high stress, anxiety, or emotional distress, recommend mindfulness techniques, relaxation exercises, or seeking professional counseling.  
        - If symptoms indicate lifestyle-related issues (e.g., poor sleep, diet, exercise), guide the user toward healthy habits.  
        - If the condition is unclear or potentially serious, strongly advise consulting a doctor or therapist.  
        """
```

---

## 📡 API Endpoints  

| Endpoint                  | Method | Description |
|---------------------------|--------|-------------|
| `/chatbot/`               | `POST` | Sends a symptom-related question and gets an AI-generated response |
| `/appointments/`          | `GET`  | Retrieves all booked appointments |
| `/appointments/`          | `POST` | Books a new appointment |
| `/questions/`             | `GET`  | Fetches all stored questions and responses |

---

## 🎯 Running the Django Server  
To start the Django backend, use:  
```bash
python manage.py runserver
```
The API will now be available at:  
```plaintext
http://127.0.0.1:8000/
```

---

## 📌 Running the LLaMA Model in LMStudio  
1. **Open LMStudio**  
2. **Load the model:** `"llama-3.2-1b-instruct"`  
3. **Start the local server at** `http://127.0.0.1:1234`  
4. The Django backend will now communicate with the model.

---
## 🎯 Next Steps  
- Add **user authentication**
- Implement **role-based access control** (RBAC)
- Improve **response fine-tuning** using **custom prompts**
- Advanced Error Handling **Improve error responses for better debugging**.
- Add **Front-end Interface** for a user to interact with the chatbot, possibly using Reactjs.

---
