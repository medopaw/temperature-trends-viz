# Setup Guide for Temperature Trends Viz

This guide will help you set up the Temperature Trends Viz project using uv package manager.

## Prerequisites

### Install uv

First, you need to install uv. Choose one of the following methods:

#### Method 1: Using the official installer (Recommended)

**On macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Method 2: Using pip
```bash
pip install uv
```

#### Method 3: Using Homebrew (macOS)
```bash
brew install uv
```

#### Method 4: Using Cargo (if you have Rust installed)
```bash
cargo install uv
```

### Verify Installation

After installation, verify that uv is working:
```bash
uv --version
```

You should see output like: `uv 0.x.x`

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd temperature-trends-viz
```

### 2. Install Dependencies

```bash
# Install all dependencies
uv sync

# Or install with development dependencies
uv sync --extra dev
```

This will:
- Create a virtual environment in `.venv/`
- Install all required dependencies
- Set up the project for development

### 3. Run the Application

Choose one of these methods:

#### Method A: Direct run with uv (Recommended)
```bash
uv run streamlit run weather_gui.py
```

#### Method B: Using the convenience script
```bash
# On Linux/macOS
./run.sh

# On Windows
run.bat
```

#### Method C: Using Makefile (Linux/macOS)
```bash
make run
```

#### Method D: Activate virtual environment manually
```bash
# On Linux/macOS
source .venv/bin/activate

# On Windows
.venv\Scripts\activate

# Then run
streamlit run weather_gui.py
```

## Development Workflow

### Code Quality Tools

The project includes several development tools configured in `pyproject.toml`:

```bash
# Format code
uv run black weather_gui.py
uv run isort weather_gui.py

# Type checking
uv run mypy weather_gui.py

# Linting
uv run flake8 weather_gui.py

# Run all checks
make all-checks  # (Linux/macOS only)
```

### Adding Dependencies

```bash
# Add a runtime dependency
uv add package-name

# Add a development dependency
uv add --group dev package-name

# Remove a dependency
uv remove package-name
```

### VS Code Setup

If you're using VS Code, the project includes configuration in `.vscode/settings.json` that will:
- Use the correct Python interpreter from `.venv/`
- Enable automatic code formatting on save
- Configure linting and type checking
- Set up testing with pytest

## Troubleshooting

### Common Issues

1. **uv command not found**
   - Make sure uv is installed and in your PATH
   - Restart your terminal after installation
   - Try `which uv` (Linux/macOS) or `where uv` (Windows) to verify

2. **Permission denied on run.sh**
   ```bash
   chmod +x run.sh
   ```

3. **Dependencies not installing**
   - Check your internet connection
   - Try `uv sync --refresh` to force refresh
   - Check if you're behind a corporate firewall

4. **Streamlit not starting**
   - Make sure all dependencies are installed: `uv sync`
   - Check if port 8501 is available
   - Try running with a different port: `uv run streamlit run weather_gui.py --server.port 8502`

### Getting Help

If you encounter issues:
1. Check the error message carefully
2. Ensure all prerequisites are installed
3. Try the troubleshooting steps above
4. Check the project's issue tracker
5. Create a new issue with detailed error information

## Project Structure

```
temperature-trends-viz/
├── .vscode/                 # VS Code configuration
├── cities.json             # City coordinates database
├── weather_gui.py          # Main application
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # Main documentation
├── SETUP.md                # This setup guide
├── Makefile                # Development commands (Linux/macOS)
├── run.sh                  # Startup script (Linux/macOS)
├── run.bat                 # Startup script (Windows)
├── .gitignore              # Git ignore rules
└── .venv/                  # Virtual environment (created by uv)
```

## Next Steps

Once you have the application running:
1. Open your browser to the displayed URL (usually http://localhost:8501)
2. Explore the temperature visualization features
3. Try adding new cities by editing `cities.json`
4. Consider contributing improvements to the project

Happy coding! 🌡️
