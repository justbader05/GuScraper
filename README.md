# GuScraper

A web scraper that allows you to automatically download and organize your course contents!

(Intended for use by Gulf University for Science and Technology students. However, with some tweaking, it could work on any student portal that utilizes Moodle.)

## Features

* Terminal interface
* Add courses you're currently taking from the GUST portal
* Organize said courses by semester
* Download courses automatically from each page
* Automatically sort all the downloaded files into folders
* Remembers what materials have already been downloaded to avoid repeats

## Installation

Clone the repository:

```bash
git clone https://github.com/justbader05/GuScraper
```

Enter the project directory:

```bash
cd GuScraper
```

You can either install the packages globally:

```bash
pip install -r requirements.txt
```

This is unrecommended. Alternatively, create a virtual environment using the steps below.

Create the virtual environment:

```bash
python -m venv .venv
```

Enter the virtual environment.

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Enter the virtual environment.

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Run GuScraper:
### Windows PowerShell
```powershell
python main.py
```

### Linux/macos
```bash
python3 main.py
```

## Requirements

* Python 3
* Firefox
* Required packages from `requirements.txt`

## Context

I made this project because every semester I have the same problem. Professors have different material uploading styles. Some dump the whole course on you from the beginning and others do it piece meal throughout the semester.

However, I don't want to have to keep updating my folders manually every time they decide to upload something, so this project will do it for me automatically.

Now I must confess, all of the terminal in/out is vibe coded, but right now I don't have the time to be doing stuff I already know how to do and (frankly) don't want to do. However, most of the scripting itself is me for the stuff that matters.

## Contributing

Contributions are welcome. Some areas that could use improvement:

- Add support for browsers other than Firefox
- Improve download performance, possibly through concurrent downloads
- Add packaged executables for Linux, Windows, and macOS

## Disclaimer

This project is not affiliated with Gulf University for Science and Technology. Use it responsibly and in accordance with your institution's policies.