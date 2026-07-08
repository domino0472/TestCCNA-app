<div align="center">

# CCNA Interactive Quiz

A responsive, interactive CCNA practice application featuring 158 extracted questions, visual exhibits, and local progress tracking.

[![Questions](https://img.shields.io/badge/Questions-158-1e90b8?style=for-the-badge)](#)
[![Exhibits](https://img.shields.io/badge/Exhibits-19-1e90b8?style=for-the-badge)](#)
[![HTML/CSS/JS](https://img.shields.io/badge/Frontend-HTML/CSS/JS-1e90b8?style=for-the-badge)](#)
[![Python](https://img.shields.io/badge/Backend-Python-1e90b8?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-1e90b8?style=for-the-badge)](LICENSE)

<br/>

<a href="https://domino0472.github.io/TestCCNA-app/">
  <img src="https://img.shields.io/badge/▶_Live_Demo-Click_Here-181717?style=for-the-badge&logo=github" alt="Live Demo" />
</a>

</div>

## 📌 Why This Project?

Preparing for the CCNA exam requires consistent practice and repetition. This project takes a raw PDF of practice questions and transforms it into an interactive web application. With features like local progress saving, exhibit filtering, and an intuitive UI, it allows you to test your knowledge seamlessly across both desktop and mobile devices.

## ✨ Features

- 🧠 **158 Practice Questions** — Automatically extracted from a PDF source using Python (`PyMuPDF`).
- 🖼️ **Exhibit Integration** — Includes 19 visual exhibits mapped accurately to their respective questions.
- 💾 **Progress that Sticks** — Your answers and progress are saved between sessions.
- 🎯 **Smart Filtering** — Instantly filter to show only questions with visual exhibits.
- 📱 **Fully Responsive** — Sleek sidebar navigation and mobile-friendly layouts for studying anywhere.
- 🛠️ **Local API Server** — Comes with a Python server for local testing and managing/removing exhibits.

## 🚀 Getting Started

### 1. Use the Live App (Recommended)
The easiest way to practice is through the live deployment on GitHub Pages:
**[▶ Open Live Demo](https://domino0472.github.io/TestCCNA-app/)**

### 2. Run Locally (Frontend Only)
You can run the web interface directly on your machine without a server:
1. Clone this repository:
   ```bash
   git clone https://github.com/domino0472/TestCCNA-app.git
   cd TestCCNA-app
   ```
2. Open `index.html` in your favorite web browser.

### 3. Run the Backend Tools (Optional)
If you want to re-extract questions from the PDF or run the local management API:
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install pymupdf
   ```
3. Extract questions (requires `CCNA.pdf` in the root):
   ```bash
   python extract_quiz.py
   ```
4. Start the local server API:
   ```bash
   python server.py
   ```
   *The app will be available at `http://localhost:8000`.*

## 📂 Project Structure

```text
.
├── extract_quiz.py       # PDF parsing logic using PyMuPDF (fitz)
├── server.py             # Local HTTP + API Server for exhibit management
├── baza_pytan.json       # The extracted database of 158 questions
├── index.html            # Main application entry point
├── app.js                # Frontend logic, rendering, and state management
├── style.css             # Responsive styling and typography
└── assets/               # Folder containing 19 mapped exhibits (q13.png, etc.)
```

## ⚖️ Disclaimer

This project is an unofficial study tool. "CCNA" is a registered trademark of Cisco Systems, Inc. This application is not affiliated with, endorsed by, or sponsored by Cisco. The practice questions used in this repository are intended for educational and preparation purposes only.

## 👤 Author

**Damian Dominiak** — Technical Computer Science student @ Wrocław University of Science and Technology.
Linux · Infrastructure · Embedded · Networking.

[![GitHub](https://img.shields.io/badge/GitHub-domino0472-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/domino0472)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Damian_Dominiak-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/damian-dominiak/)
[![Email](https://img.shields.io/badge/Email-damian.dominiak.2006@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:damian.dominiak.2006@gmail.com)

<sub>Built with Linux, C and coffee ☕</sub>
