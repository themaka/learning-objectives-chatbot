# Learning Objectives Chatbot

A Streamlit-based chatbot application that helps educators and instructional designers create effective learning objectives through guided conversation.

## Features

- Interactive chatbot that guides users through creating learning objectives
- Analysis of learning objectives based on Bloom's Taxonomy
- Suggestions for improving learning objectives
- Sample objectives for reference
- History tracking of created objectives

## Getting Started

### Prerequisites

- Python 3.12 or higher
- uv package manager (`pip install uv`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/learning-objectives-chatbot.git
cd learning-objectives-chatbot
```

2. Set up the Python environment:
```bash
uv venv
```

3. Activate the virtual environment:
```bash
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

4. Install dependencies:
```bash
uv sync
```

### Running the Application

Run the Streamlit app:
```bash
streamlit run src/learning_objectives_chatbot/app.py
```

The app will be accessible at http://localhost:8501 by default.

## Project Structure

```
.
├── README.md                          # Project overview
├── pyproject.toml                     # Python project metadata and dependencies
└── src/
    └── learning_objectives_chatbot/   # Main package
        ├── __init__.py                # Package initialization
        ├── app.py                     # Main Streamlit application
        └── utils.py                   # Utility functions for chatbot
```

## How It Works

1. The chatbot guides users through a series of questions about their teaching subject, desired learning level, and assessment methods.
2. Based on user responses, the chatbot generates learning objectives following best practices.
3. The system analyzes objectives using Bloom's Taxonomy and provides suggestions for improvement.
4. Users can refine objectives or create new ones for different aspects of their subject.

## Bloom's Taxonomy Levels

The chatbot uses Bloom's Taxonomy to structure learning objectives at appropriate cognitive levels:

1. **Remember**: Recall facts and basic concepts
2. **Understand**: Explain ideas or concepts
3. **Apply**: Use information in new situations
4. **Analyze**: Draw connections among ideas
5. **Evaluate**: Justify a stand or decision
6. **Create**: Produce new or original work

## Development

### Adding Dependencies

```bash
# Add a package
uv add package-name
```

### Testing

```bash
pytest
```

## License

[MIT](LICENSE)