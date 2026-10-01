# PDFsFromWeb

Two small desktop tools for quickly collecting PDFs on a list of topics. The list in there right now is mostly U.S. economics: GDP, inflation, the Fed, monetary and fiscal policy.

**`getPDFsFromWeb.py`** runs a Google search for `<topic> filetype:pdf` on every topic in the list at the top of the file, takes the top 5 results for each, and saves the links to `pdf_links.txt`.

**`downloadPDFs.py`** reads `pdf_links.txt`, downloads every link that actually comes back as a PDF into `pdf_downloads/`, and skips the rest (dead links, HTML pages pretending to be PDFs).

Both have a simple PyQt window with a progress bar, and the work runs on a background thread so the window stays responsive.

## Running it

```bash
pip install PyQt5 requests google beautifulsoup4 ollama PyPDF2
python getPDFsFromWeb.py
python downloadPDFs.py
```

Edit the `topics` list in `getPDFsFromWeb.py` to search for whatever you want. It waits 2 seconds between searches so Google doesn't block it.
