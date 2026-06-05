# How to Train Your First ML Model (A Beginner's Walkthrough)

Okay, so you just installed MLToolkit and you're staring at your screen like "now what?" Don't worry — I was there too. This guide will walk you through training your very first model, step by step, with zero assumed knowledge.

## What You Need Before We Start

- MLToolkit installed (`pip install mltoolkit` — you did this already, right?)
- Python 3.8+
- A CSV file with some data (or just use the sample dataset I included)
- A willingness to mess up and try again

**This guide is for:** Complete beginners. I explain everything.

---

## Step 1: Make Sure It Actually Installed

1. Open your terminal or whatever IDE you're using
2. Make a new file called `first_model.py`
3. Run this to check:

```bash
python -c "import mltoolkit; print(mltoolkit.__version__)"
```

If you see a version number, you're golden. If you see red text, you probably need to reinstall:

```bash
pip install mltoolkit
```

---

## Step 2: Load Some Data

1. Import the thing that loads data:

```python
from mltoolkit import DataLoader
```

2. Actually load your data:

```python
# If you have your own CSV:
data = DataLoader.from_csv("your_data.csv")

# If you just want to practice with fake data:
data = DataLoader.load_sample("iris")
```

3. Peek at what you loaded:

```python
print(data.head())
print(data.info())
```

**[PLACEHOLDER FOR SCREENSHOT: Show the data table with columns and first few rows]**

**Tip:** If you're using the Iris dataset, the "target" column is called `species`. If you're using your own data, figure out which column is the thing you're trying to predict.

---

## Step 3: Clean and Prep the Data

Raw data is usually messy. Let's fix it.

1. Bring in the auto-cleaner:

```python
from mltoolkit.preprocessing import AutoPreprocessor

preprocessor = AutoPreprocessor(
    handle_missing=True,      # Fills empty cells automatically
    encode_categorical=True,  # Turns text into numbers
    scale_features=True       # Makes all numbers the same "size"
)
```

2. Separate your "inputs" from your "answer":

```python
X = data.drop("target_column")  # Everything except the answer
y = data["target_column"]      # The thing you're trying to predict
```

3. Split into training and testing sets:

```python
X_train, X_test, y_train, y_test = data.split(
    test_size=0.2,    # 80% for training, 20% for testing
    random_seed=42    # Makes it repeatable
)
```

4. Clean the training data, then clean the test data the same way:

```python
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)
```

**⚠️ SUPER IMPORTANT — Don't Skip This:**

Only run `fit_transform` on the **training** data. Then use `transform` (no "fit") on the test data. If you fit on everything, you're cheating — the model sees the test data too early. It's called "data leakage" and it'll make your accuracy look fake.

---

## Step 4: Pick a Model

1. Import the classifier:

```python
from mltoolkit.models import Classifier
```

2. Make a model:

```python
model = Classifier(
    algorithm="random_forest",
    n_estimators=100,
    max_depth=10
)
```

**Which algorithm should you pick?**

| Algorithm | When to Use It |
|-----------|---------------|
| `random_forest` | Default choice. Works on almost everything. |
| `logistic_regression` | Super fast, easy to understand. Good baseline. |
| `gradient_boosting` | Usually the most accurate, but slower. |

I always start with Random Forest. It's like the "safe choice" of ML.

---

## Step 5: Train It!

1. Set up the trainer:

```python
from mltoolkit.training import Trainer

trainer = Trainer(
    model=model,
    validation_split=0.2,  # Sets aside 20% of training data to check progress
    verbose=True           # Shows progress in the terminal
)
```

2. Actually train:

```python
history = trainer.fit(X_train_processed, y_train)
```

3. Watch the numbers:

```
Epoch 1/10 — loss: 0.4521 — val_accuracy: 0.8912
Epoch 2/10 — loss: 0.3124 — val_accuracy: 0.9234
...
```

The `val_accuracy` going up is good. If it goes down, something's wrong.

**[PLACEHOLDER FOR SCREENSHOT: Terminal showing training epochs]**

---

## Step 6: See How Good It Is

1. Run the evaluator:

```python
from mltoolkit.evaluation import Evaluator

evaluator = Evaluator(model)
results = evaluator.evaluate(X_test_processed, y_test)
```

2. Print the summary:

```python
print(results.summary())
```

3. Make a confusion matrix (fancy word for "where did it mess up?"):

```python
evaluator.plot_confusion_matrix(save_path="confusion_matrix.png")
```

**[PLACEHOLDER FOR SCREENSHOT: Confusion matrix heatmap]**

---

## Step 7: Save Your Model

You don't want to retrain every time. Save it!

```python
model.save("my_first_model.pkl")
```

Check that the file exists:

```bash
ls my_first_model.pkl    # Mac/Linux
dir my_first_model.pkl   # Windows
```

---

## Step 8: Use It on New Data (Optional But Cool)

1. Load your saved model back:

```python
loaded_model = Classifier.load("my_first_model.pkl")
```

2. Get new data and clean it the same way:

```python
new_data = DataLoader.from_csv("new_data.csv")
new_data_processed = preprocessor.transform(new_data)
predictions = loaded_model.predict(new_data_processed)

print(predictions)
```

Boom. You just predicted something.

---

## When Things Break (Because They Will)

### "FileNotFoundError: your_data.csv not found"

Your CSV isn't where Python is looking. Either:
- Move the CSV to the same folder as your Python script, OR
- Give the full path: `DataLoader.from_csv("C:/Users/You/Desktop/data.csv")`

### "ValueError: could not convert string to float"

You have text in a column that should be numbers. Make sure `encode_categorical=True` is set in your AutoPreprocessor. Or tell it which columns are text:

```python
preprocessor = AutoPreprocessor(categorical_columns=["color", "size"])
```

### "My accuracy is like 20% — terrible!"

A few things to check:
- Did you leak data? (See Step 3 warning)
- Is your target column imbalanced? (Like 95% "yes" and 5% "no")
- Try a different algorithm — `gradient_boosting` might work better

### "Training is taking FOREVER"

- Reduce `n_estimators` to 50 or 25 for testing
- Use a smaller chunk of your data just to see if it works
- If you have a GPU, enable it: `config.set("default_device", "gpu")`

---

## What's Next?

You trained a model! That's honestly the hardest part. Now try:

- **Compare models:** Train 3 different ones and see which wins
- **Tune it:** Use `HyperOptimizer` to find the best settings
- **Explain it:** Use the XAI tools to see which features matter most
- **Deploy it:** Export to ONNX and put it in a real app

You got this. 🚀
