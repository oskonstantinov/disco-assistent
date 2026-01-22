Installation

To set up and run the project, follow these steps:

Clone the Repository

```bash
git clone https://github.com/coignard/disco-cli
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

Running the Application

```bash
python3 .
```

Contributing

Feel free to submit issues and pull requests to improve the project.

License

This project is licensed under the MIT License.