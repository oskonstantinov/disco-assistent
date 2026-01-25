Installation

To set up and run the project, follow these steps:

Clone the Repository

```bash
git clone https://github.com/oskonstantinov/disco-assistent.git
cd disco-cli
```
Set Up a Virtual Environment

```bash
python3 -m pip install venv
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

Configuration

Before running the application, you need to add your API key. Create a `.api_key` file in the project root with your API key as its only content (no quotes, just the key). This file is automatically ignored by git for security.

The application will also check for the `ANTHROPIC_API_KEY` environment variable as a fallback.

User Context Learning

The application features an intelligent context learning system that automatically builds and maintains user context from chat history:

**How It Works:**
- During conversations, the AI identifies valuable personal information (preferences, experiences, goals, relationships, etc.)
- New information is automatically added to `config/user_context.txt`
- The system provides in-character notifications when context is updated using the **Encyclopedia** skill
- Future conversations include this accumulated context for more personalized interactions

**Context File:**
- Location: `config/user_context.txt`
- Format: Plain text with one piece of information per line
- Language: Automatically maintained in the user's dialogue language
- Git: Added to `.gitignore` for privacy (contains personal information)

**Multilingual Support:**
- Context updates are automatically stored in the same language as your dialogue
- Notifications appear in your configured language (Russian/English)
- All context is preserved across language switches

Running the Application

```bash
python3 .
```

Contributing

Feel free to submit issues and pull requests to improve the project.

License

This project is licensed under the MIT License.