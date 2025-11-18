# Foreign Education Support Agent

A multi-agent AI system built with **Crew AI** to assist prospective international students in planning their studies abroad.
This agent provides comprehensive information on universities, living expenses, airlines, lifestyle, and currency exchange rates for any country.

---

## Features

- **University Finder:** Retrieves top private universities in the mentioned country and program details for foreign students.
- **Financial Planner:** Estimates monthly living expenses (rent, food, transport) for students.
- **Airlines Finder:** Lists major airlines operating flights to the target country.
- **Lifestyle Advisor:** Provides cultural insights, local lifestyle, student community, and special occasions.
- **Currency & Exchange Rate Checker:** Fetches current exchange rates against USD, GBP, EURO, and INR.

---

## Technologies & Libraries Used

- **Crew AI:** For creating agents, tasks, and multi-agent coordination.
- **Tavily:** For real-time travel and airline information.
- **Python Libraries:** `datetime`, `os`, `requests`, `dotenv`
- **LLMs from Groq:**
  - `groq/llama-3.1-8b-instant` (temperature=0.5)
  - `groq/llama-3.3-70b-versatile` (temperature=0.6)

---

## Agents & Tasks

### 1. University Finder
- **Goal:** Return a list of top 10 private universities with program details for foreign students for the interested country and stream.
- **Output:** Markdown list including specializations, program duration, and rankings.

### 2. Financial Planner
- **Goal:** Provide rough monthly living expenses for students (rent, food, transport) in local currency.
- **Output:** Structured Markdown format with estimated costs and notes.

### 3. Airlines Finder
- **Goal:** Return a list of frequently traveling airlines operating to the target country.
- **Output:** Markdown list of airlines.

### 4. Lifestyle Advisor
- **Goal:** Describe cultural fit, lifestyle, student community, and special occasions.
- **Output:** Structured Markdown detailing language, lifestyle, and major events.

### 5. Currency & Exchange Rate Checker
- **Goal:** Provide current exchange rates against USD, GBP, EURO, and INR.
- **Output:** Structured Markdown format with approximate rates.

---

## Flask Web Interface

A **Flask-based web application** was created to interact with the Foreign Education Support Agent, allowing users to input their preferences and view results in a user-friendly format.

### Features

- Accepts user input for:
  - **Country**
  - **Education Level**
  - **Stream / Field of Study**
- Displays structured reports from the agents directly in the browser.
- Converts the Markdown outputs from the agents into HTML for easy viewing.


Following are some ss for the developed application.

<img width="1182" height="480" alt="image" src="https://github.com/user-attachments/assets/1025892e-3e07-4224-9fad-4f95e9502a34" />

<img width="1037" height="685" alt="image" src="https://github.com/user-attachments/assets/c042f12c-7883-423a-a377-f3a0d398d971" />

<img width="1138" height="726" alt="image" src="https://github.com/user-attachments/assets/bb0f8095-afaf-482b-9882-5ba920805803" />

<img width="1058" height="613" alt="image" src="https://github.com/user-attachments/assets/cf658dae-145e-4d0d-96b7-015e8e795a5b" />

<img width="1063" height="550" alt="image" src="https://github.com/user-attachments/assets/cf10f452-23b0-4cff-86c2-15c84a9e4dfb" />

<img width="1132" height="767" alt="image" src="https://github.com/user-attachments/assets/314f45f1-3811-4e2e-86fc-7d74650745fd" />






