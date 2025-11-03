# Bobo Reporter

**Bobo Reporter** is a tool designed to help you generate reports of your eBooks highlights quickly and efficiently. Connect your Kobo or Kindle eReader to your PC and automatically create a PDF or HTML report of your highlights and annotations.

## Features

- **Compatibility**: Kobo (GNU/Linux systems) and Kindle (Windows).
- **Output formats**: Generate reports in PDF or HTML.
- **Web App**: Modern web interface for easy access (NEW!)
- **Terminal App**: Original command-line interface still available

## Usage

### Web App (Recommended)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the web server:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

4. Select your device type (Kobo or Kindle), scan for devices, or upload a file manually.

### Terminal App

Run the original terminal application:
```bash
python main.py
```

## TODO
[] A lot of refactor
[] More compatibility
[] Kobo unofficial annotations support
[] Seduce Willy to remove Pandas
[] Little external dependencies 
[] Write license

## Requirements

- **Operating System**: Linux.
- **Device**: Kobo.
- **USB Connection**: To connect your device to the PC.

## License

This project is licensed under the Beerware License.

---

Bobo Reporter, making your readings more organized.
