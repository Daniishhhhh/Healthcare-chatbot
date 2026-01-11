import os

# Enhanced project structure with new competitive features
structure = {
    "healthchatbot-backend": {
        "app": {
            "routes": {
                "__init__.py": "",
                "health.py": "# 🚦 Person A - Basic health check endpoint\n",
                "ask.py": "# 🤖 Person B - AI query processing\n", 
                "alerts.py": "# 📡 Person E - Government health alerts\n",
                "escalate.py": "# 🚦 Person A / 🔄 Person F - Manual escalation\n",
                "whatsapp.py": "# 🚦 Person A - WhatsApp webhook integration\n",
                "appointments.py": "# 🚦 Person A - PHC/CHC booking system\n",
                "emergency.py": "# 🚦 Person A - ASHA worker escalation\n",
                "voice.py": "# 🚦 Person A - IVR/Voice interface\n",
                "community.py": "# 📡 Person E - Village health groups\n",
                "sms.py": "# 🚦 Person A - SMS-only interface\n"
            },
            "models": {
                "__init__.py": "",
                "user.py": "# 🚦 Person A - User data models\n",
                "query.py": "# 🚦 Person A - Query/response models\n",
                "alert.py": "# 📡 Person E - Health alert models\n",
                "escalation.py": "# 🔄 Person F - Escalation models\n",
                "appointment.py": "# 🚦 Person A - Appointment booking models\n",
                "clinic.py": "# 🚦 Person A - PHC/CHC data models\n",
                "asha_worker.py": "# 🚦 Person A - ASHA worker models\n",
                "community.py": "# 📡 Person E - Village group models\n",
                "emergency.py": "# 🚦 Person A - Emergency escalation models\n"
            },
            "services": {
                "__init__.py": "",
                "user_service.py": "# 🚦 Person A - User management logic\n",
                "query_service.py": "# 🚦 Person A / 🤖 Person B - Query processing\n",
                "alert_service.py": "# 📡 Person E - Alert management\n",
                "escalation_service.py": "# 🔄 Person F - Escalation logic\n",
                "appointment_service.py": "# 🚦 Person A - Booking logic\n",
                "emergency_service.py": "# 🚦 Person A - Emergency handling\n",
                "location_service.py": "# 🚦 Person A - Geographic services\n",
                "notification_service.py": "# 🚦 Person A - SMS/WhatsApp sending\n",
                "community_service.py": "# 📡 Person E - Village group management\n",
                "translation_service.py": "# 🤖 Person B - Multilingual support\n"
            },
            "data": {
                "__init__.py": "",
                "clinics": {
                    "odisha_phcs.json": '[\n  {\n    "clinic_id": "PHC_KLD_001",\n    "name": "Kalahandi Primary Health Centre",\n    "district": "Kalahandi",\n    "location": "Bhawanipatna",\n    "phone": "+91-9876543210",\n    "available_slots": ["09:00", "11:00", "14:00", "16:00"]\n  },\n  {\n    "clinic_id": "CHC_BBR_001", \n    "name": "Bhubaneswar Community Health Centre",\n    "district": "Khordha",\n    "location": "Bhubaneswar",\n    "phone": "+91-9876543211",\n    "available_slots": ["10:00", "12:00", "15:00", "17:00"]\n  }\n]',
                    "asha_workers.json": '[\n  {\n    "asha_id": "ASHA_KLD_001",\n    "name": "Sunita Devi",\n    "district": "Kalahandi",\n    "village": "Bhawanipatna",\n    "phone": "+91-8765432109",\n    "languages": ["odia", "hindi"]\n  },\n  {\n    "asha_id": "ASHA_BBR_001",\n    "name": "Mamta Singh", \n    "district": "Khordha",\n    "village": "Bhubaneswar",\n    "phone": "+91-8765432108",\n    "languages": ["odia", "english"]\n  }\n]',
                    "clinic_schedules.json": '{\n  "monday": ["09:00-12:00", "14:00-17:00"],\n  "tuesday": ["09:00-12:00", "14:00-17:00"],\n  "wednesday": ["09:00-12:00", "14:00-17:00"],\n  "thursday": ["09:00-12:00", "14:00-17:00"],\n  "friday": ["09:00-12:00", "14:00-17:00"],\n  "saturday": ["09:00-13:00"],\n  "sunday": ["Emergency Only"]\n}'
                },
                "health": {
                    "symptoms_odia.json": '{\n  "ଜ୍ୱର": "ଜ୍ୱର ହେଲେ ବିଶ୍ରାମ ନିଅନ୍ତୁ, ଅଧିକ ପାଣି ପିଅନ୍ତୁ। ୧୦୧°F ଉପରେ ହେଲେ ଡାକ୍ତରଙ୍କ ପାଖକୁ ଯାଆନ୍ତୁ।",\n  "କାଶ": "କାଶ ପାଇଁ ଗରମ ପାଣି ପିଅନ୍ତୁ, ମହୁ ଖାଆନ୍ତୁ। ୨ ସପ୍ତାହ ରହିଲେ ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ।",\n  "ମୁଣ୍ଡବିନ୍ଧା": "ମୁଣ୍ଡବିନ୍ଧା ପାଇଁ ବିଶ୍ରାମ ନିଅନ୍ତୁ, ଅନ୍ଧାର ଘରେ ରୁହନ୍ତୁ। ପାଣି ପିଅନ୍ତୁ।"\n}',
                    "symptoms_hindi.json": '{\n  "बुखार": "बुखार में आराम करें, पानी पिएं। 101°F से ज्यादा हो तो डॉक्टर को दिखाएं।",\n  "खांसी": "खांसी के लिए गर्म पानी पिएं, शहद लें। 2 हफ्ते तक रहे तो डॉक्टर के पास जाएं।",\n  "सिरदर्द": "सिरदर्द में आराम करें, अंधेरे में रहें। पानी पिएं।"\n}',
                    "seasonal_alerts.json": '{\n  "monsoon": {\n    "diseases": ["डेंगू", "मलेरिया", "चिकुनगुनिया"],\n    "prevention": "मच्छरदानी का प्रयोग करें, पानी जमा न होने दें।",\n    "alert_level": "high"\n  },\n  "winter": {\n    "diseases": ["निमोनिया", "सर्दी-जुकाम"],\n    "prevention": "गर्म कपड़े पहनें, बुजुर्गों का ख्याल रखें।",\n    "alert_level": "medium"\n  },\n  "summer": {\n    "diseases": ["हीट स्ट्रोक", "डिहाइड्रेशन"],\n    "prevention": "ORS पिएं, धूप से बचें।",\n    "alert_level": "high"\n  }\n}',
                    "emergency_protocols.json": '{\n  "high_fever": {\n    "threshold": "103°F",\n    "action": "immediate_escalation",\n    "message": "तुरंत ASHA कार्यकर्ता से संपर्क करें। 108 पर कॉल करें।"\n  },\n  "chest_pain": {\n    "keywords": ["chest pain", "सीने में दर्द", "ଛାତି ଯନ୍ତ୍ରଣା"],\n    "action": "emergency_escalation",\n    "message": "तुरंत 108 पर कॉल करें। नजदीकी अस्पताल जाएं।"\n  },\n  "breathing_difficulty": {\n    "keywords": ["breathing", "सांस", "ନିଶ୍ୱାସ"],\n    "action": "emergency_escalation", \n    "message": "तुरंत 108 पर कॉल करें।"\n  }\n}'
                },
                "locations": {
                    "districts.json": '[\n  {"name": "Kalahandi", "odia_name": "କଳାହାଣ୍ଡି", "code": "KLD"},\n  {"name": "Khordha", "odia_name": "ଖୋର୍ଦ୍ଧା", "code": "KHR"},\n  {"name": "Cuttack", "odia_name": "କଟକ", "code": "CTC"},\n  {"name": "Puri", "odia_name": "ପୁରୀ", "code": "PRI"},\n  {"name": "Ganjam", "odia_name": "ଗଞ୍ଜାମ", "code": "GNJ"}\n]',
                    "villages.json": '[\n  {"village": "Bhawanipatna", "district": "Kalahandi", "phc": "PHC_KLD_001"},\n  {"village": "Bhubaneswar", "district": "Khordha", "phc": "CHC_BBR_001"},\n  {"village": "Kesinga", "district": "Kalahandi", "phc": "PHC_KLD_001"},\n  {"village": "Jatni", "district": "Khordha", "phc": "CHC_BBR_001"}\n]'
                }
            },
            "utils": {
                "__init__.py": "",
                "language_detector.py": "# 🤖 Person B - Language identification\n",
                "location_matcher.py": "# 🚦 Person A - Geographic matching\n", 
                "time_helpers.py": "# 🚦 Person A - Scheduling utilities\n",
                "validators.py": "# 🔄 Person F - Input validation\n",
                "formatters.py": "# 🚦 Person A - Response formatting\n"
            },
            "integrations": {
                "__init__.py": "",
                "twilio_client.py": "# 🚦 Person A - Twilio API wrapper\n",
                "cowin_api.py": "# 📡 Person E - Vaccination data\n",
                "government_apis.py": "# 📡 Person E - Gov health data APIs\n",
                "maps_api.py": "# 🚦 Person A - Location services\n"
            },
            "db": {
                "__init__.py": "",
                "db.py": "# 🚦 Person A - Enhanced DB connections\n",
                "seed.py": "# 🚦 Person A / 📡 Person E - Enhanced seeding\n",
                "migrations": {
                    "__init__.py": "",
                    "001_initial_setup.py": "# 🚦 Person A - Initial database setup\n",
                    "002_add_appointments.py": "# 🚦 Person A - Appointment collections\n",
                    "003_add_communities.py": "# 📡 Person E - Community collections\n"
                }
            },
            "core": {
                "__init__.py": "",
                "config.py": "# 🚦 Person A - Enhanced configuration\n",
                "logger.py": "# 🔄 Person F - Logging setup\n",
                "security.py": "# 🔄 Person F - Authentication\n",
                "constants.py": "# 🚦 Person A - App constants\n"
            },
            "__init__.py": "",
            "main.py": "# 🚦 Backend & API orchestration – Person A\n",
            "dependencies.py": "# 🚦 Person A - Enhanced dependencies\n"
        },
        "tests": {
            "__init__.py": "",
            "test_main.py": "# 🔄 Person F - Main app tests\n",
            "test_health.py": "# 🔄 Person F - Health endpoint tests\n",
            "test_ask.py": "# 🔄 Person F / 🤖 Person B - AI query tests\n",
            "test_alerts.py": "# 🔄 Person F / 📡 Person E - Alert tests\n",
            "test_escalate.py": "# 🔄 Person F - Escalation tests\n",
            "test_whatsapp.py": "# 🔄 Person F - WhatsApp integration tests\n",
            "test_appointments.py": "# 🔄 Person F - Booking system tests\n",
            "test_emergency.py": "# 🔄 Person F - Emergency escalation tests\n",
            "test_voice.py": "# 🔄 Person F - Voice interface tests\n",
            "test_community.py": "# 🔄 Person F - Community feature tests\n"
        },
        "scripts": {
            "__init__.py": "",
            "setup_database.py": "# 🚦 Person A - Database initialization\n",
            "load_sample_data.py": "# 🚦 Person A - Load demo data\n",
            "backup_data.py": "# 🔄 Person F - Database backup\n",
            "deploy.py": "# 🔄 Person F - Deployment automation\n"
        },
        "docs": {
            "API.md": "# API Documentation\n\n## Health Chatbot API Endpoints\n\n### WhatsApp Integration\n- POST /whatsapp/webhook\n- GET /whatsapp/send-message\n\n### Appointments\n- POST /appointments/book\n- GET /appointments/available\n\n### Emergency\n- POST /emergency/escalate\n- GET /emergency/contacts\n",
            "DEPLOYMENT.md": "# Deployment Guide\n\n## Docker Deployment\n``````\n\n## Environment Setup\nCopy .env.example to .env and configure:\n- TWILIO credentials\n- MongoDB connection\n- API keys\n",
            "FEATURES.md": "# Feature Documentation\n\n## Competitive Advantages\n1. Local PHC/CHC booking\n2. ASHA worker escalation\n3. Voice interface for illiterate users\n4. Community health groups\n5. Offline SMS capability\n6. Multilingual support (Odia/Hindi/English)\n",
            "DEMO.md": "# Demo Script\n\n## WhatsApp Demo Flow\n1. Send 'I have fever' → Get health advice\n2. Send 'book appointment' → Get PHC booking\n3. Send 'emergency' → Trigger ASHA escalation\n4. Show community group joining\n5. Demonstrate voice interface\n"
        },
        ".env": "# 🚦 Person A - Environment variables\nMONGO_CONNECTION_STRING=mongodb://mongodb:27017\nTWILIO_ACCOUNT_SID=your_sid_here\nTWILIO_AUTH_TOKEN=your_token_here\nTWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886\nTWILIO_PHONE_NUMBER=+1234567890\nEMERGENCY_ESCALATION_TIMEOUT=300\nDEFAULT_LANGUAGE=odia\nAPPOINTMENT_BOOKING_ENABLED=true\nCOMMUNITY_FEATURES_ENABLED=true\nVOICE_INTERFACE_ENABLED=false\nDEBUG_MODE=true\n",
        ".env.example": "# Environment Template\n# Copy this to .env and fill in your values\nMONGO_CONNECTION_STRING=mongodb://mongodb:27017\nTWILIO_ACCOUNT_SID=your_twilio_sid\nTWILIO_AUTH_TOKEN=your_twilio_token\nTWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886\n",
        "requirements.txt": "# 🚦 Person A - Dependencies\nfastapi==0.104.1\nuvicorn[standard]==0.24.0\nmotor==3.3.2\npython-decouple==3.8\npydantic==2.5.0\ntwilio==8.10.0\nlangdetect==1.0.9\ngeopy==2.4.1\nschedule==1.2.0\npython-multipart==0.0.6\njinja2==3.1.2\naiofiles==23.2.1\nhttpx==0.25.2\n",
        "requirements-dev.txt": "# 🔄 Person F - Development dependencies\npytest==7.4.3\npytest-asyncio==0.21.1\nblack==23.11.0\nflake8==6.1.0\npre-commit==3.5.0\n",
        "Dockerfile": "# 🚦 Person A / 🔄 Person F - Enhanced Dockerfile\nFROM python:3.11-slim\n\nWORKDIR /app\n\n# Copy requirements first for better caching\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\n# Copy application code\nCOPY ./app ./app\n\n# Expose port\nEXPOSE 8000\n\n# Run the application\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\", \"--reload\"]\n",
        "docker-compose.yml": "# 🚦 Person A / 🔄 Person F - Enhanced Docker Compose\nversion: '3.8'\n\nservices:\n  backend:\n    build: .\n    ports:\n      - \"8000:8000\"\n    environment:\n      - MONGO_CONNECTION_STRING=mongodb://mongodb:27017\n    volumes:\n      - ./app:/app/app\n    depends_on:\n      - mongodb\n    restart: unless-stopped\n\n  mongodb:\n    image: mongo:6.0\n    ports:\n      - \"27017:27017\"\n    volumes:\n      - mongo-data:/data/db\n    restart: unless-stopped\n\nvolumes:\n  mongo-data:\n",
        "docker-compose.dev.yml": "# 🔄 Person F - Development environment\nversion: '3.8'\n\nservices:\n  backend:\n    build: .\n    ports:\n      - \"8000:8000\"\n    environment:\n      - DEBUG_MODE=true\n      - MONGO_CONNECTION_STRING=mongodb://mongodb:27017\n    volumes:\n      - ./:/app\n    depends_on:\n      - mongodb\n      - redis\n\n  mongodb:\n    image: mongo:6.0\n    ports:\n      - \"27017:27017\"\n    volumes:\n      - mongo-data:/data/db\n\n  redis:\n    image: redis:7-alpine\n    ports:\n      - \"6379:6379\"\n\nvolumes:\n  mongo-data:\n",
        "nginx.conf": "# 🔄 Person F - Production web server\nupstream backend {\n    server backend:8000;\n}\n\nserver {\n    listen 80;\n    server_name localhost;\n\n    location / {\n        proxy_pass http://backend;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n    }\n}\n",
        "README.md": "# 🏥 SWASTHYA SETU (ସ୍ୱାସ୍ଥ୍ଯ ସେତୁ)\n## Multilingual AI Health Chatbot for Rural Odisha\n\n### 🚀 Features\n- WhatsApp/SMS/Voice interfaces\n- Local PHC/CHC appointment booking\n- ASHA worker emergency escalation\n- Village health communities\n- Multilingual support (Odia/Hindi/English)\n- Offline SMS capability\n\n### 🛠️ Setup\n``````\n\n### 📱 Demo\n1. Join Twilio WhatsApp sandbox\n2. Send health queries in any language\n3. Book appointments at local clinics\n4. Test emergency escalation\n\n### 🏆 Competitive Advantages\n- First hyperlocal health assistant for Odisha\n- Direct PHC/CHC integration\n- Voice interface for illiterate users\n- Real ASHA worker escalation system\n",
        ".gitignore": "# 🔄 Person F - Git ignore patterns\n__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\n*.egg-info/\n.installed.cfg\n*.egg\nPYTHONPATH\n.env\n.venv\nenv/\nvenv/\nENV/\nenv.bak/\nvenv.bak/\n.pytest_cache/\n.coverage\nhtmlcov/\n.tox/\n.cache\nnosetests.xml\ncoverage.xml\n*.cover\n.hypothesis/\n.DS_Store\n.vscode/\n.idea/\n*.swp\n*.swo\n",
        ".dockerignore": "# 🔄 Person F - Docker ignore patterns\n.git\n.gitignore\nREADME.md\nDockerfile\n.dockerignore\nnode_modules\nnpm-debug.log\n.env\n.venv\nvenv/\n__pycache__\n*.pyc\n*.pyo\n*.pyd\n.Python\n.pytest_cache\n.coverage\n",
        "CHANGELOG.md": "# Changelog\n\n## [1.0.0] - 2025-09-19\n\n### Added\n- WhatsApp chatbot integration\n- Local PHC/CHC appointment booking\n- ASHA worker emergency escalation\n- Voice interface for illiterate users\n- Community health groups\n- Multilingual support (Odia/Hindi/English)\n- Offline SMS capability\n- Seasonal health alerts\n- Government health data integration\n\n### Features for Demo\n- Working WhatsApp bot with health FAQ\n- Mock appointment booking system\n- Emergency escalation simulation\n- Docker containerized deployment\n"
    }
}

def create_structure(base, struct):
    """Recursively create folders and files with content"""
    for name, content in struct.items():
        path = os.path.join(base, name)
        if isinstance(content, dict):  # directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:  # file
            # Ensure parent directory exists
            parent_dir = os.path.dirname(path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

# Run the script
create_structure(".", structure)
print("✅ Enhanced project structure with competitive features created!")
print("\n🎯 Priority files for Monday demo:")
print("   - app/routes/whatsapp.py")
print("   - app/routes/appointments.py") 
print("   - app/routes/emergency.py")
print("   - app/data/clinics/odisha_phcs.json")
print("   - app/data/health/symptoms_odia.json")
print("\n🚀 Next: Add code to these files and test with Docker!")
