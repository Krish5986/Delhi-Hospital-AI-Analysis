# 🏥 AI-Powered Hospital Experience Analysis (Delhi)
An end-to-end data engineering and AI pipeline comparing **Government vs. Private** healthcare sectors in Delhi.

## 📊 Executive Summary
This project analyzes 300+ patient reviews to identify systemic "Pain Points" in healthcare logistics and service quality. 

### Key Findings:
* **The Wait-Time Gap:** Government hospitals face **7x more** complaints regarding "Long Wait Times" (9.2%) compared to the private sector (1.4%).
* **The Trust Anchor:** Despite administrative delays, **44.9%** of public hospital reviews specifically praise **Medical Expertise**, showing high clinical trust.
* **Staff Behavior:** Identified as a major pain point in public facilities (**28.6%**), signaling high workload stress.

---

## 🏗️ Technical Architecture

### Phase 1: Data Collection (VS Code)
- **Tooling:** Selenium WebDriver.
- **Action:** Custom scraper built to handle dynamic loading on Google Maps.
- **Output:** `delhi_hospital_reviews.csv`

### Phase 2: AI Processing (Google Colab)
- **Model:** `facebook/bart-large-mnli` (Zero-Shot Classification).
- **Process:** Automated categorization of raw text into 6 strategic buckets (Wait Times, Staff Behavior, Cleanliness, etc.).
- **Hardware:** Utilized T4 GPU for high-speed inference.
---
## 📈 Visual Insights

### 1. Current Pain Points & Praise (Last 12 Months)
![<img width="858" height="470" alt="image" src="https://github.com/user-attachments/assets/6fa79439-5133-4103-bb2c-cc55b1321fd8" />
)
*This AI-generated chart shows the distribution of feedback categories across both hospital types.*

### 2. Data Recency Analysis
![<img width="1175" height="547" alt="image" src="https://github.com/user-attachments/assets/fb8ed5a3-2b42-4c44-8c08-d4b4378c905e" />
)
*To ensure 2026 relevance, we filtered for reviews from the last 12 months, removing "solved" historical problems.*

---
## 🔍 Key Strategic Findings

The analysis reveals a significant divergence in patient experience between the public and private sectors.

### 1. The Logistics Bottleneck (Wait Times) ⏳
* **Government Hospitals (9.2%)** face nearly **7x more** complaints regarding "Long Wait Times" compared to **Private hospitals (1.4%)**.
* **Impact:** This highlights a critical need for digital queue management systems in the public sector to manage high patient volumes efficiently.

### 2. Staff Interaction Gap 🤝
* **28.6%** of Government hospital feedback identified **Staff Behavior** as a primary pain point.
* **Context:** This is likely driven by high patient-to-staff ratios and worker burnout. In contrast, Private hospitals saw this at only **16.4%**.

### 3. Core Strength: Medical Trust 🩺
* Despite the delays, **44.9%** of Government reviews focus on praising **Medical Expertise**.
* **Competitive Advantage:** This proves that public trust in the clinical skills of doctors at institutions like Safdarjung and AIIMS remains remarkably high.

### 4. Market Segmentation (The Value Proposition) 💰
* **Government hospitals** dominate in **Affordability (8.2%)**.
* **Private hospitals** lead in **Cleanliness** and **Infrastructure**.
* **Conclusion:** Patient choice is clearly segmented based on whether they prioritize cost or environmental logistics.

---

## 🚀 Future Recommendations

Based on the AI-driven insights, the following interventions are suggested:

1.  **Digital Transformation:** Implementing real-time appointment tracking and digital tokens could directly mitigate the primary pain point of wait times.
2.  **Soft Skills Training:** Targeted behavioral intervention for frontline staff in public hospitals could bridge the satisfaction gap identified by the sentiment analysis.

## 🛠️ Installation & Usage
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/REPO_NAME.git`
2. Install requirements: `pip install -r requirements.txt`
3. View the full analysis in `notebooks/Bulid_Reviews.ipynb`
