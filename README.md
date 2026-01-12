# 🏥 SWASTHYA SETU  
**Multilingual Rural Healthcare Assistant**

SWASTHYA SETU is a multilingual, WhatsApp-based rural healthcare assistant designed to provide **symptom-based health guidance**, **Primary Health Centre (PHC) appointment booking**, and **emergency escalation**.  
The system focuses on improving healthcare accessibility for rural populations by leveraging commonly used communication channels such as WhatsApp and SMS.

---

## 🎯 Problem Statement & Goals

Rural healthcare in India faces critical challenges such as:
- Limited doctor availability at PHCs
- Language barriers for non-English speakers
- Delayed emergency response
- Heavy dependence on ASHA workers for first-level care

SWASTHYA SETU aims to bridge these gaps by offering:
- Easy access to basic health triage via WhatsApp
- Multilingual support for rural users
- Seamless PHC appointment assistance
- Rapid escalation during medical emergencies

---

## 🚀 Core Features

### 🗣️ Multilingual Chatbot
- Supports **English, Hindi, and Odia**
- Responds to common symptoms like **fever, cough, headache**
- Structured **Help Menu** for first-time users

### 🏥 PHC Appointment Support
- Lists nearby government **Primary Health Centres**
- Allows basic outpatient appointment booking
- Aligned with India’s **PHC-based public healthcare model**

### 🚨 Emergency Detection & Escalation
- Keyword-based emergency detection (e.g., chest pain, breathing difficulty, high fever)
- Triggers immediate escalation workflows
- Ensures faster response during critical conditions

---

## 👩‍⚕️ ASHA Worker & Emergency Flow

- Emergency messages are mapped to a **mock ASHA worker registry**
- Alerts include:
  - User phone number
  - Reported symptoms
  - Timestamp
- If ASHA escalation fails, the system shares **official Indian emergency numbers (108, 102)**  
- This design mirrors real-world rural healthcare workflows in India

---

## 🛠️ Tech Stack & Architecture

- **Backend:** FastAPI (asynchronous REST APIs)
- **Database:** MongoDB (chat logs & appointment history)
- **Messaging Platform:** Twilio WhatsApp API
- **Tunneling:** ngrok (for exposing local FastAPI server to Twilio)

### Architecture Flow
1. User sends message via WhatsApp
2. Twilio forwards message to FastAPI webhook
3. NLP logic processes intent and symptoms
4. MongoDB stores interactions
5. System responds or escalates as needed

---

## 🌍 Impact & Positioning

- Low-cost and easily deployable for rural environments
- Designed to **complement government digital health initiatives**
- Reduces load on PHCs by enabling basic triage
- Empowers villagers with healthcare access in their **native language**
- Strengthens ASHA-based frontline healthcare response

---

## 🔮 Future Enhancements
- ML-based symptom classification
- Voice input for low-literacy users
- Integration with live government health portals
- Deployment on cloud infrastructure

---

## 👨‍💻 Author
**Danish**  
GitHub: https://github.com/Daniishhhhh

---

## 📜 License
This project is licensed under the **MIT License**.
