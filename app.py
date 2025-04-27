"""
Sprint 1:
1. ocr_engine.py -> converts image to text (DONE; OCR cant read bill pictures)
2. parser.py ->  detects date and amount from ocr output (DONE)
3. automator.py -> logins to expense page, fills in date, casecode, amount etc
4. app.py -> landing page for uploading pdf and doing 1,2,3
5. deploy via render
"""

import ocr_engine
import parser

def file_expense(image_path):
    ocr_text = ocr_engine.extract_text(image_path)
    response = parser.parse_text(ocr_text)
    print(response)
