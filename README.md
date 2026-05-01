# local-img-gen-service
Python based command line app that uses OpenRouter image models via api requests to generate images

Automatically generates Instagram carousel slide images using AI. You provide a JSON file describing each slide's content and an example image for style reference — the app calls Google Gemini via OpenRouter and saves optimized JPEG images to your downloads folder.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Windows Setup](#windows-setup-recommended-for-most-users)
- [Mac / Linux Setup](#mac--linux-setup)
- [Configure Environment Variables](#configure-environment-variables)
- [Running the App](#running-the-app)
- [Preparing Your Input Files](#preparing-your-input-files)

---

## Prerequisites

Before you start, you will need:

- An **OpenRouter account** with API key and purchased credits — sign up at [openrouter.ai](https://openrouter.ai), then add credits at [openrouter.ai/credits](https://openrouter.ai/credits)
- **Python 3.10 or later** — download from [python.org/downloads](https://www.python.org/downloads/)

---

## Windows Setup (Recommended for most users)

### Step 1 — Check if Python is Already Installed

Before downloading anything, check whether Python is already on your machine. Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter) and run:

```
python --version
```

- If you see something like `Python 3.12.3` and the version is **3.10 or later**, Python is already installed — skip to [Step 2](#step-2--download-the-project).
- If you see an older version (e.g. `Python 3.8.x`), you will need to install a newer version below.
- If you see an error or `python` is not recognised, Python is not installed — follow the instructions below.

#### Installing Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and click **Download Python 3.x.x**
2. Run the installer
3. **Important:** On the very first screen of the installer, tick the checkbox labelled **"Add python.exe to PATH"** before clicking Install Now — do not skip this step

To confirm Python installed correctly, close and reopen Command Prompt, then run:

```
python --version
```

You should see something like `Python 3.12.3`. If you see an error, restart your computer and try again.

---

### Step 2 — Download the Project

**Option A — Download as a ZIP (easiest, no technical knowledge required):**

1. Go to the project page on GitHub: **https://github.com/dbrown725/local-img-gen-service**
2. Click the green **"< > Code"** button near the top right
3. Click **"Download ZIP"**
4. Once downloaded, right-click the ZIP file and choose **"Extract All..."**
5. Choose a location you can easily find, such as your **Desktop** or **Documents** folder
6. Open the extracted folder — it will be named something like `local-img-gen-service`

**Option B — Clone with Git (only if you already have Git installed):**

```
git clone https://github.com/dbrown725/local-img-gen-service.git
cd local-img-gen-service
```

---

### Step 3 — Open a Command Prompt Inside the Project Folder

1. Open the extracted project folder in File Explorer
2. Click the **address bar** at the top of the File Explorer window (the bar showing the folder path)
3. Type `cmd` and press **Enter**

A black Command Prompt window will open, already pointed at the project folder. Keep this window open for the next steps.

---

### Step 4 — Create a Virtual Environment

In the Command Prompt window, type the following and press Enter:

```
python -m venv .venv
```

Then activate it by typing this and pressing Enter:

```
.venv\Scripts\activate
```

You should see `(.venv)` appear at the start of the line. This means it worked.

> **Important:** Every time you open a new Command Prompt window to run the app, you need to activate the virtual environment again. Navigate to the project folder and run `.venv\Scripts\activate`.

---

### Step 5 — Install Dependencies

With `(.venv)` showing at the start of the line, type the following and press Enter:

```
pip install -r requirements.txt
```

This may take a minute or two. Wait until it finishes and the prompt returns.

---

### Step 6 — Create the .env File

The `.env` file stores your personal settings. It is not included in the download (it is intentionally excluded from the repository for security reasons), so you need to create it yourself.

1. Open **Notepad**
2. Click **File** → **Save As**
3. Navigate to the project folder
4. In the **"File name"** field, type `.env` (including the dot)
5. In the **"Save as type"** dropdown, choose **All Files** — this is important, otherwise Notepad will save it as `.env.txt`
6. Click **Save**

Now right-click the `.env` file and choose **Open with** → **Notepad** to edit it. Add the following three lines and fill in your own values:

```
OPENROUTER_API_KEY=your_api_key_here
UPLOADS_DIRECTORY=C:\Users\YourName\Documents\LocalImageGenService\Uploads
DOWNLOADS_DIRECTORY=C:\Users\YourName\Documents\LocalImageGenService\Downloads
```

- **OPENROUTER_API_KEY** — paste your OpenRouter API key here (find it at openrouter.ai/keys after signing in)
- **UPLOADS_DIRECTORY** — the full path to a folder where you will place your input files
- **DOWNLOADS_DIRECTORY** — the full path to a folder where finished images will be saved

**Create both folders now** in File Explorer if they do not already exist.

**Path example for a user named Sarah:**
```
UPLOADS_DIRECTORY=C:\Users\Sarah\Documents\LocalImageGenService\Uploads
DOWNLOADS_DIRECTORY=C:\Users\Sarah\Documents\LocalImageGenService\Downloads
```

Save the file and close Notepad.

---

### Step 7 — Copy the Example Files

Before running the app for the first time, copy the two files from the `examples` folder inside the project to your `UPLOADS_DIRECTORY`:

1. Open the project folder in File Explorer
2. Open the `examples` subfolder
3. Copy both files inside it
4. Paste them into the folder you set as `UPLOADS_DIRECTORY`

---

### Step 8 — Run the App

In the Command Prompt window (with `(.venv)` showing), type:

```
python main.py
```

The app will ask you two questions — type the filename and press Enter for each. Enter the names of the example files you just copied to get started quickly.

---

## Mac / Linux Setup

### Step 1 — Install Python

**Mac:** Open Terminal and run `python3 --version`. If Python is not installed, download it from [python.org/downloads](https://www.python.org/downloads/) or run `brew install python` if you have Homebrew.

**Linux:** Run `sudo apt install python3 python3-venv` (Ubuntu/Debian) or use your distribution's package manager.

---

### Step 2 — Download the Project

**Option A — Download as a ZIP:**

1. Go to **https://github.com/dbrown725/local-img-gen-service.git**
2. Click **"< > Code"** → **"Download ZIP"**
3. Unzip the file, then open a Terminal window inside the extracted folder

**Option B — Clone with Git:**

```bash
git clone https://github.com/dbrown725/local-img-gen-service.git
cd local-img-gen-service
```

---

### Step 3 — Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

To deactivate later: `deactivate`

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Create the .env File

The `.env` file is not included in the download (it is intentionally excluded from the repository for security reasons), so you need to create it yourself. In your Terminal, make sure you are inside the project folder, then run:

```bash
touch .env
```

Open the file in any text editor and add the following lines, filling in your own values:

```
OPENROUTER_API_KEY=your_api_key_here
UPLOADS_DIRECTORY=/path/to/your/uploads
DOWNLOADS_DIRECTORY=/path/to/your/downloads
```

---

### Step 6 — Copy the Example Files

Before running the app for the first time, copy the two files from the `examples` folder inside the project to your `UPLOADS_DIRECTORY`:

```bash
cp examples/* /path/to/your/uploads
```

Replace `/path/to/your/uploads` with the actual path you set for `UPLOADS_DIRECTORY`.

---

### Step 7 — Run the App

```bash
python main.py
```

---

## Configure Environment Variables

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | Your API key from [openrouter.ai/keys](https://openrouter.ai/keys) |
| `UPLOADS_DIRECTORY` | Full path to the folder containing your JSON and reference image files |
| `DOWNLOADS_DIRECTORY` | Full path to the folder where generated slide images will be saved |

---

## Running the App

When you run `python main.py`, you will be asked two questions:

1. **The carousel content JSON filename** — e.g. `carousel_content.json` (must be placed in your `UPLOADS_DIRECTORY` first)
2. **The example image filename** — e.g. `instaCarouselExample.jpg` (must be placed in your `UPLOADS_DIRECTORY` first)

Generated images are saved to your `DOWNLOADS_DIRECTORY` as `Slide_A.jpg`, `Slide_B.jpg`, `Slide_C.jpg`, and so on.

---

## Preparing Your Input Files

### The JSON File

Create a plain text file ending in `.json` with the following structure. Each item in the `presentation` list is one carousel slide:

```json
{
  "presentation": [
    {
      "image_number": 1,
      "title": "Your Slide Title",
      "visual": "Description of what should appear visually on the slide",
      "text": "Body text or caption that should appear on the slide"
    },
    {
      "image_number": 2,
      "title": "Second Slide",
      "visual": "A bright, airy kitchen scene",
      "text": "Supporting detail for this slide"
    }
  ]
}
```

### The Reference Image

This is an existing carousel image that shows the visual style you want — layout, colours, fonts, and general look. The AI will use it as a style guide when generating your new slides. Any `.jpg` or `.png` file works.

Place both files in your `UPLOADS_DIRECTORY` before running the app.

---

## Generating Your JSON Content with an LLM

Rather than writing the JSON file by hand, you can use a large language model to generate it for you. We recommend using **Google Gemini** via the OpenRouter playground:

**[openrouter.ai/google/gemini-2.5-pro-preview/playground](https://openrouter.ai/google/gemini-2.5-pro-preview/playground)**

### How to do it

1. Open `carousel_preprompt.txt` from the project folder — this is a ready-made prompt template that instructs the LLM how to structure the JSON output
2. Copy the contents of `carousel_preprompt.txt` and paste it into the playground's prompt field, filling in the topic and slide details you want
3. Run the prompt — the LLM will return a JSON block formatted correctly for this app
4. Copy the JSON output, paste it into a new file ending in `.json`, and save it to your `UPLOADS_DIRECTORY`

`carousel_preprompt_response.json` in the project folder shows a typical response to that prompt, so you can see what to expect before trying it yourself.

### Validating your JSON

Before using the generated JSON with the app, it is worth checking that it is valid. Paste the contents into **[jsonformatter.curiousconcept.com](https://jsonformatter.curiousconcept.com/)** — it will flag any formatting errors and show you exactly where the problem is.

