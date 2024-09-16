# Smart Security Guard

This project consists of a Smart Security Guard system implemented in Python. It includes two main components:
- `main.py`: The core functionality of the security guard.
- `app.py`: A Flask application to access and manage stored people information.

## Components

### main.py
This script handles the main functionality of the Smart Security Guard, including:
- Monitoring and detecting intrusions.
- Storing information about detected individuals.

### app.py
This Flask application provides a web interface to:
- Access stored information about people.
- Manage and update the stored data.

## Setup

### Prerequisites
- Python 3.x
- Flask

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Hansraja/guard.git
    cd guard
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Project

### Running main.py
To start the Smart Security Guard system:
```sh
python main.py
```
To start web interface:
```sh
python app.py
```