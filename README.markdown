# Digikala-Smart-Search

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

A powerful web-based application designed for Persian-speaking users to search for products on [Digikala](https://www.digikala.com), Iran’s leading e-commerce platform. By entering a product name in Persian, users can leverage AI-driven category classification and web automation to perform seamless searches, with results displayed directly in a browser.

## Features

- **Persian-Friendly Interface**: Built with Streamlit, featuring right-to-left (RTL) text support and Persian font styling for a native user experience.
- **AI-Powered Category Classification**: Uses LangChain with Ollama to intelligently determine the appropriate product category based on the user’s query.
- **Automated Web Search**: Employs Selenium to navigate Digikala’s website, simulating human interactions to perform searches efficiently.
- **Structured Workflow**: Managed by LangGraph, ensuring a smooth sequence of tasks from query input to search execution.
- **Real-Time Feedback**: Provides visual feedback and error handling within the Streamlit interface for a reliable user experience.

## Technologies Used

| Technology            | Description                                                  |
|-----------------------|--------------------------------------------------------------|
| **Python 3.8+**       | Core programming language for the application.                |
| **Streamlit**         | Creates the interactive web-based user interface with RTL support. |
| **LangChain**         | Framework for building applications with language models.     |
| **LangChain-Ollama**  | Integrates Ollama for natural language processing tasks.      |
| **LangGraph**         | Manages the workflow of query processing and search execution. |
| **Selenium**          | Automates web interactions with Digikala’s website.           |

## Prerequisites

- **Python 3.8 or later**: Download from [python.org](https://www.python.org/downloads/).
- **Ollama**: A local AI server for running the `qwen2.5:latest` model. Install from [ollama.com](https://ollama.com).
- **Google Chrome**: Required for Selenium WebDriver automation. Download from [google.com/chrome](https://www.google.com/chrome/).
- **ChromeDriver**: Must match your Chrome version, available at [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).
- **Internet Access**: Required for accessing [Digikala](https://www.digikala.com) and the font URL for styling ([Vazir font](https://cdn.rawgit.com/rastikerdar/vazir-font/v26.0.2/dist/Vazir.ttf)).

## Installation

1. **Install Python**:
   - Ensure Python 3.8 or later is installed. Verify with:
     ```bash
     python --version
     ```

2. **Install Ollama**:
   - Follow instructions at [ollama.com](https://ollama.com).
   - Pull the required model:
     ```bash
     ollama pull qwen2.5:latest
     ```
   - Start the Ollama server:
     ```bash
     ollama serve
     ```

3. **Install Google Chrome and ChromeDriver**:
   - Install Google Chrome from [google.com/chrome](https://www.google.com/chrome/).
   - Download ChromeDriver matching your Chrome version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).
   - Ensure ChromeDriver is in your system’s PATH or specify its path in the code if needed.

4. **Clone the Repository**:
   ```bash
   git clone https://github.com/armanjscript/Digikala-Smart-Search.git
   cd Digikala-Smart-Search
   ```

5. **Install Python Libraries**:
   ```bash
   pip install streamlit langchain-ollama langgraph selenium langchain
   ```

6. **Verify Network Access**:
   - Ensure access to [Digikala](https://www.digikala.com) and the font URL ([Vazir font](https://cdn.rawgit.com/rastikerdar/vazir-font/v26.0.2/dist/Vazir.ttf)) for proper styling.

## Usage

1. **Run the Application**:
   - Navigate to the project directory and start the Streamlit app:
     ```bash
     streamlit run main.py
     ```
   - Open your browser and go to `http://localhost:8501` to access the application.

2. **Using the Application**:
   - In the Streamlit interface, you’ll see a title in Persian (e.g., "جستجوی هوشمند دیجی‌کالا").
   - Enter a product name in Persian (e.g., "گوشی موبایل") in the text input field.
   - Click the "جستجو" (Search) button.
   - The system will:
     - Analyze the query to determine the product category using the `qwen2.5:latest` model.
     - Navigate to [Digikala](https://www.digikala.com) using Selenium, select the appropriate category, and perform the search.
     - Open a browser window displaying the search results.
   - A success or error message will appear in the Streamlit app.

## How It Works

The Digikala-Smart-Search integrates AI and web automation for a seamless experience:

1. **User Input**: Users enter a product name in Persian via the Streamlit interface.
2. **Category Classification**: The `qwen2.5:latest` model analyzes the query to determine the appropriate product category (e.g., "موبایل" for mobile phones).
3. **Web Automation**: Selenium WebDriver navigates to [Digikala](https://www.digikala.com), selects the category, enters the search term, and submits the search, simulating human interactions.
4. **Feedback**: Streamlit displays a success message if the search completes or an error message if issues arise (e.g., network errors or unavailable categories).

The workflow is orchestrated by LangGraph, ensuring efficient task sequencing.

## Limitations

- **External Dependencies**: Relies on [Digikala](https://www.digikala.com) and Ollama models, which may change or become unavailable.
- **Web Automation Stability**: Dynamic elements on Digikala may cause occasional failures (e.g., `StaleElementReferenceException`).
- **Network Dependency**: Requires a stable internet connection for web access and font loading.
- **Category Accuracy**: The AI model’s category classification depends on the quality of the input query and model performance.
- **Browser Dependency**: Limited to Google Chrome and ChromeDriver; other browsers are not supported.

## Known Issues

- **Selenium Errors**: Dynamic web elements may cause automation failures.
- **Timeouts**: Fixed timeouts (e.g., 10 seconds) may fail on slow networks.
- **Font Loading**: The external font URL may be inaccessible, affecting styling.
- **Error Handling**: Limited handling for edge cases like network interruptions or LLM failures.

## Future Improvements

- Enhance error handling and logging for better debugging.
- Support additional e-commerce platforms to reduce dependency on Digikala.
- Optimize Selenium for faster performance, possibly using headless mode.
- Improve UI/UX with progress indicators and input validation.
- Add unit tests for reliability.
- Expand language support and accessibility features.

## Contributing

Contributions are welcome! Fork the repository, make changes, and submit a pull request. Ensure your code follows the project’s style and includes tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please contact [Arman Daneshdoost] at [armannew73@gmail.com].