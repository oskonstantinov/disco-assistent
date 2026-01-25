# 🎭 Disco Assistant

*A terminal-based AI assistant inspired by Disco Elysium, featuring skill checks, dynamic dialogue, and intelligent context learning.*

**This is a fork of [disco-cli](https://github.com/coignard/disco-cli) with bug fixes and the new user context feedback loop feature.**

## 🚀 Installation

To set up and run the project, follow these steps:

### 📥 Clone the Repository

```bash
git clone https://github.com/oskonstantinov/disco-assistent.git
cd disco-assistent
```

### 🐍 Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 🔑 API Key Setup

Before running the application, you need to add your Anthropic API key:

**Option 1: Create a `.api_key` file**
```bash
echo "your-api-key-here" > .api_key
```

**Option 2: Environment Variable**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

> **Security Note:** The `.api_key` file is automatically ignored by git for your privacy.

## 🧠 User Context Learning

The application features an **intelligent context learning system** that automatically builds and maintains user context from chat history.

### 🔄 How It Works

- **🤖 AI Recognition**: During conversations, the AI identifies valuable personal information
- **💾 Auto-Save**: New information is automatically added to `config/user_context.txt`
- **📚 Skill Notifications**: The system provides in-character notifications using the **Encyclopedia** skill
- **🔄 Personalized Responses**: Future conversations include accumulated context for more relevant interactions

### 📁 Context File Details

- **📍 Location**: `config/user_context.txt`
- **📝 Format**: Plain text with one piece of information per line
- **🌍 Language**: Automatically maintained in the user's dialogue language
- **🔒 Privacy**: Added to `.gitignore` (contains personal information)

### 🌐 Multilingual Support

- **💬 Language Matching**: Context updates stored in dialogue language
- **🔔 Localized Notifications**: Appear in configured language (Russian/English)
- **🔄 Language Switching**: All context preserved across language changes

## ▶️ Running the Application

```bash
python3 .
```

## 🤝 Contributing

Feel free to submit **issues** and **pull requests** to improve the project!

## 📄 License

This project is licensed under the **MIT License**.