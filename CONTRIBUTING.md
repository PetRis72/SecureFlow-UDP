# Contributing to SecureFlow-UDP

First off, thank you for considering contributing to **SecureFlow-UDP**! It is contributors like you that make this project a robust and secure tool for everyone.

By contributing to this project, you agree to abide by its terms and ensure that your contributions are made in good faith.

---

## 📜 Table of Contents
1. [Code of Conduct](#-code-of-conduct)
2. [Our Process](#-our-process)
3. [How to Contribute](#-how-to-contribute)
4. [Coding Standards](#-coding-standards)
5. [Attribution & Ownership](#-attribution--ownership)

---

## 🤝 Code of Conduct
This project and everyone participating in it is governed by a standard of respect and professionalism. Please be kind, constructive, and helpful in your communication with the maintainer and other contributors.

---

## 🛠 Our Process
To maintain a clean and professional codebase, we use **Squash Merging**. 



This means all your commits for a specific feature will be combined into one single, high-quality commit in the `main` branch. This keeps our project history readable and professional.

---

## 🚀 How to Contribute

### 1. Reporting Bugs
* Check the **Issues** tab to see if the bug has already been reported.
* If not, open a new issue. Include steps to reproduce the bug and details about your environment (OS, Python version).

### 2. Suggesting Enhancements
* Open an issue to discuss the enhancement before starting the work. This ensures your idea aligns with the project's **Future Roadmap**.

### 3. Pull Requests
1. **Fork** the repository to your own account.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. **Test your code!** Ensure it works in both **Normal Mode** and **Demo Mode** (using the MITM sniffer).
4. Commit your changes with a descriptive message.
5. Push to your fork and open a **Pull Request** to the `main` branch of the original repository.

---

## 📏 Coding Standards
* **Python Style:** Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
* **Security First:** Never downgrade encryption settings. AES-256-GCM is our non-negotiable standard.
* **Documentation:** If you add a new feature, update the `README.md` and add inline comments to the code in `engine.py`.

---

## ⚖ Attribution & Ownership
As specified in the project license:
* This is an open-source project, but **[Your Name]** remains the lead author and owner.
* All contributors will be credited in the git history.
* If you use this base code for your own project, you **must** link back to this original repository.

---
*Thank you for helping make SecureFlow-UDP faster and more secure!*