
flowchart TD
    %% ========================================
    %% User Entry Point (Blue)
    %% ========================================
    subgraph USER_ENTRY[User Entry Point]:::user
        A1[Rural User with Health Query]
        A2[Language Options: Odia | Hindi | English]
        A3[Device Options: Basic Phone | Smartphone]
    end
    A1 --> A2 --> A3

    %% ========================================
    %% Multi-Channel Access (Blue)
    %% ========================================
    subgraph MULTI_CHANNEL[Multi-Channel Access]:::user
        B1[WhatsApp (Smartphone users)]
        B2[SMS (Basic phones)]
        B3[Voice/IVR (Illiterate users)]
    end
    A3 --> B1
    A3 --> B2
    A3 --> B3

    %% Twilio Gateway
    B1 --> C1[TWILIO GATEWAY]
    B2 --> C1
    B3 --> C1

    %% ========================================
    %% Backend Processing (Green)
    %% ========================================
    subgraph BACKEND[Backend Processing (Docker Container)]:::ai
        C2[FASTAPI Backend Container]
        C2 --> D1[Language Detection Module]
        C2 --> D2[Intent Classification Engine]
        D2 --> D2a[Medical Query (symptoms, prevention)]
        D2 --> D2b[Appointment Booking]
        D2 --> D2c[Vaccination Inquiry]
        D2 --> D2d[Emergency Alert]
        C2 --> D3[AI Query Processing (RAG Engine)]
        C2 --> D4[Government Health Data Integration]
    end
    C1 --> C2

    %% ========================================
    %% Service Routing (Decision Diamond - Orange)
    %% ========================================
    D2 --> E{Query Type Detection}:::decision
    E -->|🏥 MEDICAL QUERY| F1[Health FAQ + Symptom Checker]
    E -->|📅 APPOINTMENT| F2[PHC/CHC Booking System]
    E -->|💉 VACCINATION| F3[Schedule + Reminder System]
    E -->|🚨 EMERGENCY| F4[Escalation + Alert System]

    %% ========================================
    %% Government Data Integration (Purple)
    %% ========================================
    subgraph GOVERNMENT[Government Data Integration]:::government
        G1[National Health Portal]
        G2[CoWIN API]
        G3[District Health Database]
        G4[Outbreak Alert System]
    end
    D4 --> G1
    D4 --> G2
    D4 --> G3
    D4 --> G4

    %% ========================================
    %% Response Generation (Green)
    %% ========================================
    subgraph RESPONSE[Response Generation]:::ai
        H1[MongoDB Database - Store user data & chat history]
        H2[AI Response Generator]
        H2 --> H2a[80% accuracy health responses]
        H2 --> H2b[Multilingual output]
        H2 --> H2c[Escalation triggers]
        H2 --> H2d[Appointment confirmations]
    end
    F1 --> H1 --> H2
    F2 --> H1 --> H2
    F3 --> H1 --> H2
    F4 --> H1 --> H2

    %% ========================================
    %% Delivery Channels (Blue)
    %% ========================================
    subgraph DELIVERY[Delivery Channels]:::user
        I1[WhatsApp → Rich media]
        I2[SMS → Text-only]
        I3[Voice → Text-to-speech]
    end
    H2 --> I1
    H2 --> I2
    H2 --> I3

    %% ========================================
    %% Additional Features (Orange)
    %% ========================================
    subgraph INNOVATION[Additional Innovation Features]:::innovation
        J1[ASHA Worker Escalation System]
        J2[Community Health Campaign Broadcasts]
        J3[Vaccination Reminder Automation]
        J4[Government Scheme Notifications]
        J5[Offline SMS Capability]
    end
    I1 --> J1
    I2 --> J5
    I3 --> J1

    %% ========================================
    %% Impact Measurement (Blue)
    %% ========================================
    subgraph IMPACT[Impact Measurement]:::user
        K1[Query accuracy tracking (80% target)]
        K2[User engagement metrics]
        K3[Health awareness improvement (20% target)]
        K4[Geographic coverage analysis]
    end
    I1 --> K1
    I2 --> K2
    I3 --> K3

    %% ========================================
    %% Styling
    %% ========================================
    classDef user fill:#cce5ff,stroke:#007bff,stroke-width:2px,color:#000
    classDef ai fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#000
    classDef government fill:#e2d9f3,stroke:#6f42c1,stroke-width:2px,color:#000
    classDef decision fill:#ffe5b4,stroke:#ff9900,stroke-width:2px,color:#000
    classDef innovation fill:#fff3cd,stroke:#fd7e14,stroke-width:2px,color:#000