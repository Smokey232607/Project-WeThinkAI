# MLToolkit FAQ — Stuff I Get Asked All the Time

## Getting Started

### What even is MLToolkit?

It's a Python library I built to make machine learning less painful. Instead of writing 50 lines of setup code every time, you can train a model in like 5 lines. It wraps Scikit-learn and TensorFlow into something that doesn't make you want to cry.

### What Python do I need?

Python 3.8 or newer. I personally use 3.10 and it works great. Don't use anything older than 3.8 or some stuff will break.

### How do I install it?

```bash
pip install mltoolkit
```

If you want everything (TensorFlow, viz tools, all the good stuff):

```bash
pip install mltoolkit[full]
```

### Is this free?

Yeah, completely. MIT License. Use it for your homework, your startup, whatever. Just maybe give me a shoutout if it saves your life.

### Do I need to be a machine learning expert?

Nope. I literally made this for people who aren't. The `AutoModel` class is basically "I don't know what I'm doing, just make it work" mode. It tries a bunch of algorithms and picks the best one for you.

---

## Data Stuff

### What kind of data can I load?

Pretty much everything:
- CSV files: `DataLoader.from_csv("file.csv")`
- Excel: `DataLoader.from_excel("file.xlsx")`
- Pandas DataFrames: `DataLoader.from_dataframe(df)`
- SQL databases: `DataLoader.from_sql(connection, "SELECT * FROM table")`
- NumPy arrays if you're into that

### How does the auto-cleaner work?

`AutoPreprocessor` looks at your data and figures out what's wrong:
- Missing numbers? Fills them with the average (or median, depending)
- Missing text? Fills with the most common answer
- Text categories? Turns them into numbers automatically
- Numbers on different scales? Normalizes them

You can also customize it if the defaults aren't cutting it.

### Can I do my own preprocessing instead?

Totally. Build a pipeline:

```python
from mltoolkit.preprocessing import Pipeline, Scaler, Encoder

pipeline = Pipeline([
    ("imputer", Imputer(strategy="median")),
    ("scaler", Scaler(method="standard")),
    ("encoder", Encoder(type="one_hot"))
])
```

### I have a million rows. Will it crash?

Probably not if you turn on chunked mode:

```python
from mltoolkit import config
config.set("chunk_size", 50000)
config.set("n_jobs", -1)  # Uses all your CPU cores
```

It processes the data in pieces instead of trying to swallow it whole.

---

## Training Models

### What algorithms can I use?

**Classical ML:** Random Forest, Logistic Regression, SVM, Gradient Boosting, KNN, Naive Bayes
**Deep Learning:** Neural networks through TensorFlow
**Ensemble stuff:** Stacking, blending, voting classifiers

### What's the difference between Classifier and AutoModel?

- **Classifier/Regressor:** YOU pick the algorithm and set the knobs. More control.
- **AutoModel:** IT picks everything. You just say "classification" or "regression" and hand it data. Great when you're lazy or learning.

### Can I use my GPU?

For TensorFlow models, it usually auto-detects. To force it:

```python
from mltoolkit import config
config.set("default_device", "gpu")
```

Scikit-learn models are CPU-only, but honestly they're fast enough for most stuff.

### Can I pause training and come back later?

Yes! Checkpoints are a lifesaver:

```python
trainer = Trainer(model, checkpoint_dir="./checkpoints", checkpoint_every=5)
trainer.fit(X_train, y_train)
```

If your computer dies or you close the laptop, it picks up where it left off.

---

## Hyperparameter Tuning (The Fancy Stuff)

### What methods are there?

- **Grid Search:** Tries every combo. Slow but thorough. Good for small searches.
- **Random Search:** Tries random combos. Faster. Good enough most of the time.
- **Bayesian Optimization:** The smart one. Learns from each try and gets better. This is my go-to.

### How long does it take?

Depends on your data size, how many parameters you're testing, and how complex the model is. For a quick run, set `n_iterations=20` with Bayesian — you'll get solid results in minutes.

### Can I tune multiple models at once?

Yep:

```python
from mltoolkit.training import MultiModelOptimizer

optimizer = MultiModelOptimizer({
    "random_forest": {"n_estimators": [100, 200]},
    "svm": {"C": [0.1, 1, 10]}
})
best_model = optimizer.search(X_train, y_train)
```

It'll train both and tell you which won.

---

## Evaluation & Charts

### What metrics do I get?

**Classification:** Accuracy, Precision, Recall, F1-Score, ROC-AUC, Log Loss
**Regression:** MAE, RMSE, R², MAPE

Basically all the stuff your professor asks for.

### How do I compare two models?

```python
from mltoolkit.evaluation import ModelComparator

comparator = ModelComparator([model_a, model_b])
comparator.compare(X_test, y_test)
comparator.plot_comparison(save_path="comparison.png")
```

You get a nice chart showing which model is better at what.

### Can I save the charts for my report?

Yeah, every plot function takes a `save_path`:

```python
plotter.plot(save_path="report_chart.png", dpi=300)
```

300 DPI is good for printing or putting in a presentation.

---

## Deployment (Getting It Out There)

### What formats can I export to?

- **Pickle (.pkl):** Python-only. Fastest to load. Use this if you're staying in Python.
- **ONNX (.onnx):** Works in other languages too. Good for cross-platform stuff.
- **TensorFlow SavedModel:** If you're using TensorFlow Serving.
- **JSON:** Just the config/settings. Lightweight.

### How do I put it on TensorFlow Serving?

```python
from mltoolkit.deployment import TFServingExporter

exporter = TFServingExporter(model_name="my_model", version=1)
exporter.export(model, "/path/to/serving/models")
```

### Can I make a REST API?

Yup, built-in Flask wrapper:

```python
from mltoolkit.deployment import ModelAPI

api = ModelAPI(model)
api.run(host="0.0.0.0", port=5000)
```

Then hit `http://localhost:5000/predict` with a POST request and JSON data.

---

## Explainable AI (XAI) — Making It Not a Black Box

### Why do I need XAI?

Because saying "the model said no" isn't enough. You need to explain WHY. XAI shows you which features influenced the prediction. Super useful for:
- Debugging weird predictions
- Meeting compliance requirements
- Not failing your class when the professor asks "but why?"

### How do I use SHAP?

```python
from mltoolkit.xai import SHAPExplainer

explainer = SHAPExplainer(model)
explanations = explainer.explain(X_test[:5])
explanations.plot()
```

### Can I explain just one prediction?

Yes:

```python
explanation = explainer.explain_instance(X_test[0])
print(explanation.summary())
```

Great for when someone asks "why did it predict THIS specific thing?"

---

## Troubleshooting (The Stuff I Personally Messed Up)

### "ImportError: No module named 'tensorflow'"

Install it:
```bash
pip install tensorflow
```
Or just reinstall MLToolkit with the TensorFlow extra:
```bash
pip install mltoolkit[tensorflow]
```

### "MemoryError" — my computer is dying

Your data is too big for RAM. Try:
1. Chunked processing (see the big dataset question above)
2. Smaller batch sizes for neural nets
3. Dimensionality reduction (PCA, etc.) before training
4. Train on a sample first to make sure it works

### My predictions are garbage

Check these in order:
1. **Data leakage?** Did you `fit_transform` on the WHOLE dataset before splitting? (Don't do that.)
2. **Overfitting?** Is training accuracy 99% but test accuracy 60%? Your model memorized the training data.
3. **Wrong target?** Did you accidentally predict the ID column or something?
4. **Imbalanced classes?** If 95% of your data is "yes," the model will just say "yes" every time.

### How do I reset everything to default?

Delete the config file:
- **Mac/Linux:** `~/.mltoolkit/config.yaml`
- **Windows:** `%USERPROFILE%\.mltoolkit\config.yaml`

Or in code:
```python
from mltoolkit import config
config.reset_to_defaults()
```

### Where do I get help if I'm stuck?

- **Docs:** [https://mltoolkit.readthedocs.io](https://mltoolkit.readthedocs.io)
- **Bugs:** Open an issue on GitHub
- **Questions:** GitHub Discussions or just DM me if you know me

---

## Advanced / Random Questions

### Can I build my own custom model?

Yeah, inherit from `BaseModel`:

```python
from mltoolkit.models import BaseModel

class MyCustomModel(BaseModel):
    def fit(self, X, y):
        # Your training code here
        pass

    def predict(self, X):
        # Your prediction code here
        pass
```

### Does it do distributed training?

For TensorFlow stuff, yes — multi-GPU and distributed via TensorFlow's tools. For Scikit-learn, just use `n_jobs=-1` to use all CPU cores.

### Can I hook it up to MLflow or Weights & Biases?

Yep. Enable MLflow like this:

```python
from mltoolkit import config
config.set("mlflow_tracking_uri", "http://localhost:5000")
```

Then all your experiments get logged automatically. Super handy for keeping track of what you tried.

---

Hope this helps! If you're reading this, you're probably stuck on something. Don't give up — ML is hard but it's worth it. 🔥
