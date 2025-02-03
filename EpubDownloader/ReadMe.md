# Novel Downloader

Novel Downloader is a Python tool designed to automatically download chapters from online novels and save them locally for offline reading. This tool uses Selenium to navigate websites and extract the content dynamically, handling sites with JavaScript-generated content.

## Features

- Downloads multiple chapters concurrently using multithreading.
- Saves chapters in both plain text and JSON format for easy consumption.
- Handles network errors and retries failed downloads.
- Runs in headless mode to optimize performance.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8+
- Selenium
- ChromeDriver compatible with your Chrome browser version https://getwebdriver.com/chromedriver
- (Optional) Virtual environment

## Installation

Follow these steps to get your development environment set up:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/novel-downloader.git
   ```
2. Change directory to the novel-downloader:
    ```bash
    cd novel-downloader
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. To run the script from command line:
    ```bash
    python src/main.py
    ```

    Configuration

You can configure the novel downloader by modifying the config.py file in the src directory. Available configurations include:

Number of retry attempts
Delay between retries
Output file format and location
Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
License

Distributed under the MIT License. See LICENSE for more information.

Contact

Your Name - @lizhicq - lizhicq@hotmail.com

Project Link: https://github.com/lizhicq/novel-downloader

Acknowledgements

Selenium
Python
ChromeDriver