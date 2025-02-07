# 📄 Project: Bidding Document Extraction and Analysis with BERT

## 📌 Description
This project leverages **Natural Language Processing (NLP) with BERT** to extract, segment, and analyze bidding documents in Spanish. The workflow includes:

- **Text extraction from PDF**.
- **Segmentation and structuring of content**.
- **Using BERT to answer key questions** about the document.
- **Training a BERT model specialized in bidding documents**.

---

## 🚀 Installation
### **1️⃣ Clone the repository**
```bash
$ git clone https://github.com/user/bidding-bert-project.git
$ cd bidding-bert-project
```

### **2️⃣ Create a virtual environment** (optional but recommended)
```bash
$ python3 -m venv env
$ source env/bin/activate  # On Windows: env\Scripts\activate
```

### **3️⃣ Install dependencies**
```bash
$ pip install -r requirements.txt
```

---

## 📂 Project Structure
```plaintext
├── data/
│   ├── ExampleBidding.pdf          # Sample document
│   ├── training_dataset.json       # Training dataset
├── output/
│   ├── raw_text.txt                # Extracted text
│   ├── bidding_data.csv            # Structured data
├── src/
│   ├── bert_qa.py                  # BERT model for question answering
│   ├── extract.py                   # Text extraction and segmentation
│   ├── train_bert.py                # BERT training script
│   ├── validation.py                # Model validation
│   ├── config.py                    # Configuration
├── main.py                          # Main script
├── requirements.txt                  # Project dependencies
└── README.md                         # Documentation
```

---

## 🔧 How to Use
### **1️⃣ Process a PDF Document**
```bash
$ python main.py
```
This will execute the full pipeline:
- Extract text from `data/ExampleBidding.pdf`.
- Segment the content.
- Apply regex to extract structured data.
- Use BERT to answer key questions about the document.
- Save results in `output/bidding_data.csv`.

### **2️⃣ Train a Custom BERT Model**
```bash
$ python src/train_bert.py
```
This will train a **Spanish BERT model** using the dataset from `data/training_dataset.json`.

### **3️⃣ Evaluate the Model**
```bash
$ python src/validation.py
```
This script evaluates the performance of the fine-tuned model.

---

## 🧠 Technologies Used
- **Python 3.8+**
- **Hugging Face Transformers** (`BERT` for Question Answering)
- **Pandas** (handling extracted data)
- **PyPDF2** (extracting text from PDF)

---

## 📌 Future Improvements
- Enhance text segmentation using **transformers** instead of regex.
- Optimize answer alignment in `train_bert.py`.
- Expand the dataset with more bidding documents.

---

## 📩 Contact
If you have any questions or suggestions, feel free to open an issue or submit a pull request! 🚀

