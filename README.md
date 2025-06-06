# Python Backend API

A scalable Python backend API project with a clean architecture.

## Project Structure

```
python_backend_api/
├── src/               # Main application code
│   ├── api/           # API routes and handlers
│   ├── models/        # Database models
│   ├── services/      # Business logic
│   └── utils/         # Utility functions
├── tests/             # Test files
├── config/            # Configuration files
├── docs/              # Documentation
├── venv/              # Virtual environment
├── .env               # Environment variables
├── .gitignore         # Git ignore file
├── main.py            # Application entry point
└── requirements.txt   # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository
2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the values
5. Run the application:
   ```
   python main.py
   ```

## API Documentation

API documentation can be accessed at `/docs` when the application is running.

## Testing

Run tests with:
```
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

