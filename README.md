
PDF-COMMANDER
Complete Beginner's Guide
From Zero to Running — No Coding Knowledge Required

Written especially for engineers, doctors, lawyers,
and anyone who works with PDFs but does not write code.
Privacy First
Your files NEVER leave your computer.
100% Free
No subscriptions. No accounts. No cloud.
14 Operations
Merge, split, convert, secure & more.


SECTION 1 — What is PDF-Commander?

1.1  The Simple Explanation
PDF-Commander is a program you install on your own computer. Once installed, you open a black text window (called a Terminal or Command Prompt), type one command, and a menu appears. You then press a number to choose what you want to do with your PDF — merge, split, convert, lock with a password, and so on.
Think of it like a very powerful PDF tool that lives entirely on your machine, similar to how Microsoft Word or Excel lives on your computer rather than running on the internet.

KEY IDEA
Unlike SmallPDF, ILovePDF, or Adobe online tools, PDF-Commander is 100% offline. Your confidential engineering drawings, contracts, or medical records are NEVER uploaded anywhere. Everything happens inside your own computer.


1.2  What Can It Do?
Here is every operation available in the menu:

#
Feature
What it does for you
1
Merge PDFs
Combine several PDF files into one single document
2
Split by Page
Turn a 50-page PDF into 50 separate one-page files
3
Split by Range
Extract pages 3-7 from a PDF into its own file
4
PDF to Word
Convert a PDF into an editable Word (.docx) document
5
Word to PDF
Convert a Word document into a professional PDF
6
PDF to Text
Extract all text from a PDF into a plain .txt file
7
Rotate Pages
Fix upside-down or sideways pages (90, 180, 270 degrees)
8
Extract Specific Pages
Pull out pages 1, 5, and 10 into a new PDF
9
Add Watermark
Stamp CONFIDENTIAL or your logo onto every page
10
Encrypt PDF
Lock a PDF with a strong AES-256 password
11
Decrypt PDF
Remove password protection from a PDF you own
12
Redact Metadata
Strip hidden author info, creation dates, and tracking data
13
Inspect PDF
See full details: page count, size, author, encryption status
14
Extract Text and Tables
Export all text and tables from a PDF into a .txt file


1.3  Why Use This Instead of Online Tools?

Online PDF Tools (e.g. SmallPDF)
PDF-Commander (this tool)
Your file is UPLOADED to their servers
Your file NEVER leaves your computer
Requires internet connection
Works fully offline — no internet needed
Monthly subscription fees ($10-$30/month)
Completely free — always
File may be stored on their servers
Nothing is stored anywhere except your disk
No control over what happens to your data
You have 100% control
Limited to browser — can feel slow
Runs directly on your hardware — fast



SECTION 2 — What You Need Before Installing

2.1  Understanding the Pieces
Before we install PDF-Commander, you need two free programs. Think of it like needing both a car and a fuel station — PDF-Commander is the car, but it needs Python to run, just as a car needs petrol.

What
Real-World Analogy
Why You Need It
Python 3
The engine inside the car
PDF-Commander is written in Python. Python must be installed first.
pip
The fuel pump (comes with Python)
Downloads and installs all the PDF libraries automatically.
PDF-Commander
The car itself
The main tool you will use every day.


2.2  Check if Python is Already Installed
Before downloading anything, check if Python is already on your computer:

STEP 1  Open your Terminal (Mac/Linux) or Command Prompt (Windows)
On Windows: Press the Windows key, type cmd, and press Enter.
On Mac: Press Command + Space, type Terminal, and press Enter.
On Linux: Press Ctrl + Alt + T.


STEP 2  Type this command and press Enter



python --version

WHAT TO LOOK FOR
If you see something like 'Python 3.11.2' — you are ready! If you see an error or 'Python 2.x.x' — you need to install Python 3 (see Section 3).



SECTION 3 — Installation (Do This Once, Never Again)

3.1  Install Python 3

Windows
Open your web browser and go to:  python.org/downloads
Click the big yellow button that says 'Download Python 3.x.x'
Open the downloaded file to start the installer
CRITICAL — before clicking Install: tick the checkbox at the BOTTOM that says "Add Python to PATH". This is the most important step!
Click 'Install Now' and wait for it to finish
Close the installer

ADD TO PATH — WHY IT MATTERS
If you skip the 'Add Python to PATH' checkbox, the Terminal will not be able to find Python and every command you type later will show an error. It takes 2 seconds to tick this box — please do not skip it.


Mac
Open your web browser and go to:  python.org/downloads
Click the download button for the latest Python 3 version
Open the downloaded .pkg file and follow the installer steps
Click Continue, Accept, and Install when prompted
Python is now installed — no extra PATH step needed on Mac

Linux (Ubuntu / Debian)
Open Terminal and type these two commands one at a time:
sudo apt update
sudo apt install python3 python3-pip -y

3.2  Download PDF-Commander
PDF-Commander is a folder of files. You need to get that folder onto your computer.

Option A — If You Were Given a ZIP File (Easiest)
Locate the PDF-Commander.zip file (e.g. on your Desktop or in Downloads)
Right-click the ZIP file and select 'Extract All' (Windows) or double-click (Mac)
Choose a location — for example: C:\PDF-Commander on Windows, or /Users/YourName/PDF-Commander on Mac
You now have a folder called PDF-Commander

Option B — Download from GitHub (If You Have the Link)
If someone gave you a GitHub link:
Go to the GitHub page in your browser
Click the green 'Code' button
Click 'Download ZIP'
Extract the ZIP as described in Option A above

3.3  Install All PDF Libraries (One Command)
PDF-Commander needs several PDF tools installed. One command installs them all automatically:

STEP 1  Open Terminal / Command Prompt




STEP 2  Navigate to the PDF-Commander folder



cd C:\PDF-Commander
On Mac/Linux it would look like:
cd /Users/YourName/PDF-Commander

WHAT IS 'cd'?
'cd' means 'Change Directory'. It tells the Terminal: go inside this folder. Think of it like double-clicking a folder in File Explorer, but in text form.


STEP 3  Install all libraries with one command



pip install -r requirements.txt

You will see a lot of text scrolling past — that is normal. It is downloading the PDF tools. When it stops and shows no error, you are done.

TROUBLESHOOTING
If you see 'pip is not recognized' — try typing 'pip3' instead of 'pip'. If that also fails, Python was not added to PATH. Re-install Python and tick the PATH checkbox (see Step 3.1).


3.4  (Optional) Install LibreOffice for Word-to-PDF Conversion
Only needed if you want to convert Word documents to PDF on Mac or Linux. Windows users can skip this — it uses Microsoft Word automatically.

Mac: Go to libreoffice.org, click Download, and install it like any Mac app
Ubuntu/Linux: Open Terminal and type:
sudo apt install libreoffice -y
Windows: Skip this step — not required


SECTION 4 — Running PDF-Commander

4.1  How to Start the Program
Every time you want to use PDF-Commander, follow these two steps:

STEP 1  Open Terminal / Command Prompt






STEP 2  Go to the PDF-Commander folder



cd C:\PDF-Commander

STEP 3  Start the program



python main.py

The screen will clear and you will see the PDF-Commander menu, which looks like this:

  PDF-COMMANDER  |  Privacy-First  Local-Only  No Cloud
  
  #    Operation
   1   Merge PDFs
   2   Split PDF (by page)
   ...and so on...

4.2  Using the Menu
The menu is simple to use:

Type the number next to the operation you want (e.g. type 1 for Merge PDFs)
Press Enter
The program will ask you questions — like which file to use and where to save the result
Type your answers and press Enter after each one
When finished, it shows a success message and returns to the main menu
Type 0 and press Enter to exit the program

IMPORTANT — FILE PATHS
When the program asks 'Input PDF path', you need to type the FULL location of your file. Example on Windows:  C:\Users\Ahmed\Documents\report.pdf  Example on Mac:  /Users/Ahmed/Documents/report.pdf  Tip: You can drag-and-drop the file into the Terminal window and it will type the path for you!


4.3  Keyboard Shortcuts

Key
What it does
Ctrl + C  (during an operation)
Cancel the current task and go back to the menu — nothing is saved
Ctrl + C  (at the main menu)
Exit and close the program
Enter (blank line)
In some prompts, accept the default suggestion shown in brackets
Arrow keys
Move through previous commands you typed (useful for fixing typos)



SECTION 5 — Step-by-Step Examples (Real Walkthroughs)

5.1  Example: Merge Three PDF Reports into One
Scenario: You have three separate PDF files and need to combine them into one document.

Start PDF-Commander: type python main.py and press Enter
Type 1 (for Merge PDFs) and press Enter
The program asks for PDF files one at a time. Type the first file path:
C:\Documents\report_part1.pdf
Press Enter. Type the second file path:
C:\Documents\report_part2.pdf
Press Enter. Type the third file path:
C:\Documents\report_part3.pdf
Press Enter on a BLANK line to tell the program you are done adding files
It asks for the output file name. Type where you want to save it:
C:\Documents\full_report.pdf
Press Enter — the merge happens in seconds
You will see:  'Merged 47 pages → C:\Documents\full_report.pdf'

5.2  Example: Lock a PDF with a Password
Scenario: You have a confidential engineering report and need to protect it before emailing it.

Start PDF-Commander and type 10 (Encrypt PDF), press Enter
Type the path to your PDF file when asked:
C:\Documents\confidential_design.pdf
Type a strong password when asked (the text you type is hidden — that is normal)
Retype the password to confirm
Press Enter when asked for Owner Password (same password will be used)
Type the output file path:
C:\Documents\confidential_design_LOCKED.pdf
Press Enter — the encrypted file is created

STRONG PASSWORDS
Use a password that is at least 12 characters long and includes numbers and symbols. Example: Engineering#2024! is much stronger than 'password123'. Write it down somewhere safe — there is no 'forgot password' option for encrypted PDFs.


5.3  Example: Convert PDF to Word for Editing
Scenario: You received a PDF specification sheet and need to edit some text in it.

Start PDF-Commander and type 4 (PDF to Word), press Enter
Type the full path to your PDF:
C:\Documents\spec_sheet.pdf
Press Enter — the tool suggests a default output name. Press Enter to accept it, or type a new path
Wait 10-30 seconds depending on file size
Open the resulting .docx file in Microsoft Word and edit as needed

NOTE ON CONVERSION QUALITY
PDF to Word conversion works best on text-based PDFs. Scanned documents (photos of paper) will not convert as cleanly. For scanned documents, try Option 14 (Extract Text) instead.


5.4  Example: Remove Hidden Metadata Before Sharing
Scenario: You are about to email a PDF report externally and want to make sure no hidden author or company information is embedded in it.

Start PDF-Commander and type 13 (Inspect PDF) first — to see what metadata exists
Type your file path to see the metadata (Author, Creator, dates, etc.)
Press Enter to return to the menu, then type 12 (Redact Metadata)
Type the path to the PDF and a new output path for the clean version
The program confirms exactly what it removed
Share the clean version — it contains no hidden personal or company data


SECTION 6 — Understanding File Paths (The Most Common Confusion)

6.1  What is a File Path?
A file path is the full address of a file on your computer — like a street address, but for files. When PDF-Commander asks 'Input PDF path', it is asking: where exactly on your computer is this file?

Operating System
Example File Path
Windows
C:\Users\Ahmed\Documents\my_report.pdf
Mac
/Users/Ahmed/Documents/my_report.pdf
Linux
/home/ahmed/Documents/my_report.pdf


6.2  The Easiest Way — Drag and Drop!
You do not need to type file paths manually. Use drag-and-drop:

When PDF-Commander is waiting for a file path, switch to File Explorer (Windows) or Finder (Mac)
Locate your PDF file
Click and drag the file into the Terminal/Command Prompt window
The full file path appears automatically — press Enter

WORKS ON ALL SYSTEMS
Drag-and-drop into Terminal works on Windows, Mac, and Linux. It is the fastest way to enter file paths and eliminates typos entirely.


6.3  Common File Path Mistakes

Mistake
Fix
Forgetting the file extension (.pdf)
Always include .pdf at the end: report.pdf not just report
Using wrong slash direction on Windows
Windows uses backslash \  not forward slash /
Spaces in folder names
Put quotes around the path:  "C:\My Files\report.pdf"
Wrong drive letter on Windows
Check if your file is on C:, D:, or another drive
Typing the path instead of dragging
Use drag-and-drop — it is faster and 100% accurate



SECTION 7 — Troubleshooting Common Problems

7.1  Error Messages and Solutions

Error Message
What to Do
'python' is not recognized
Python is not installed or not added to PATH. Re-install Python and tick the 'Add to PATH' checkbox.
'pip' is not recognized
Try using 'pip3' instead. If that fails, Python needs to be re-installed with PATH enabled.
ModuleNotFoundError
A library is missing. Run:  pip install -r requirements.txt  again from the PDF-Commander folder.
File not found: your_file.pdf
The file path is wrong. Double-check spelling, or use drag-and-drop to insert the path automatically.
Permission denied
You are trying to save to a read-only location. Save to your Desktop or Documents folder instead.
Incorrect password / PasswordError
The PDF password you entered does not match the file's password. Check for typos (password input is case-sensitive).
Conversion failed (Word to PDF)
LibreOffice is not installed. Install it from libreoffice.org (Mac/Linux only — Windows uses Microsoft Word).


7.2  The Program Seems Stuck
If PDF-Commander appears frozen or is taking very long:

For large files (100+ MB PDFs), conversion and extraction can take several minutes — this is normal
If it has been more than 10 minutes with no progress, press Ctrl + C to cancel safely
The program will return to the main menu without corrupting any files

7.3  I Made a Mistake — Will My Original File Be Damaged?
No. PDF-Commander NEVER modifies your original files. Every operation reads your original and saves the result to a NEW file. Your original PDF is always left untouched.

ORIGINAL FILES ARE ALWAYS SAFE
You can run any operation with confidence. The original file is never overwritten. If you do not like the result, simply delete the output file and try again.



SECTION 8 — Quick Reference Card (Print This Page)

Starting PDF-Commander (do this every time)

Step 1  Open Terminal
Windows: Press Win key, type 'cmd', press Enter. Mac: Cmd+Space, type 'Terminal', press Enter.
Step 2  Go to Folder
Type: cd C:\PDF-Commander   (Windows)
Type: cd /Users/YourName/PDF-Commander   (Mac)
Step 3  Run
python main.py


Menu Number Reference

1
Merge PDFs
2
Split by Page
3
Split by Range
4
PDF to Word
5
Word to PDF
6
PDF to Text
7
Rotate Pages
8
Extract Pages
9
Watermark
10
Encrypt
11
Decrypt
12
Clear Metadata
13
Inspect PDF
14
Extract Text
0
EXIT


Emergency Commands

Situation
What to Type
Cancel current task
Ctrl + C   (hold Ctrl and press C)
Exit the program
Type 0 and press Enter at main menu  —  or  Ctrl + C
Restart after a crash
Type python main.py again
Re-install libraries
Type pip install -r requirements.txt



SECTION 9 — Frequently Asked Questions

Does PDF-Commander need internet to work?
No. After the one-time installation, PDF-Commander is 100% offline. It does not make any network connections. You can use it on an air-gapped computer with no internet at all.

Will my original PDF files be changed or deleted?
Never. PDF-Commander only reads your original files. It always creates a new output file. If you do not like the result, simply delete the output file — your original is perfectly safe.

How do I update PDF-Commander if a new version is released?
Download the new version (ZIP file or from GitHub), extract it to the same folder, and run pip install -r requirements.txt again. Your settings are not stored in the program so nothing is lost.

I am on a company computer and do not have admin rights. Can I still install it?
Possibly. Python can sometimes be installed without admin rights. If pip install fails due to permissions, try adding '--user' to the command: pip install --user -r requirements.txt. Contact your IT department if this does not work.

Can PDF-Commander handle very large PDF files (500MB, 1GB)?
Yes, but large files take longer. A 500MB merge may take several minutes. A 1GB file extraction may take 10-20 minutes depending on your computer's speed. This is normal — the program has not crashed, it is working.

Is this safe to use for confidential engineering drawings or legal documents?
Yes — that is exactly what it was designed for. Because nothing is uploaded to the internet, your confidential files stay entirely on your machine. This makes PDF-Commander significantly safer than any online PDF tool for sensitive documents.

The program showed an error. How do I report it?
Take a screenshot of the error message and note which operation you were running. Share this with the person who set up PDF-Commander for you (or file a bug report on GitHub if you have access). The error text is very helpful for diagnosing issues.


SECTION 10 — Installation Checklist

Use this checklist to confirm everything is set up correctly. Tick each item as you complete it.



One-Time Setup
☐
Python 3 is installed (version 3.10 or higher)
☐
During Python install, 'Add Python to PATH' was ticked (Windows)
☐
The PDF-Commander folder is on your computer (e.g. C:\PDF-Commander)
☐
Terminal is open and you navigated to the folder using the cd command
☐
pip install -r requirements.txt completed without errors
☐
LibreOffice installed (Mac/Linux only, for Word-to-PDF)


First Run Test
☐
Typed python main.py and saw the PDF-Commander menu
☐
Ran Option 13 (Inspect PDF) on any PDF file successfully
☐
Tried at least one merge or split operation
☐
Know how to cancel with Ctrl+C and exit with 0


You are ready. Your PDFs. Your machine. Your privacy.
PDF-Commander — built for professionals who work with sensitive documents.
