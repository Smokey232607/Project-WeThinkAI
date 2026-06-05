# MLToolkit

Hey! This is MLToolkit — a Python toolkit I built to make machine learning way less scary. I got tired of writing the same boilerplate code over and over for every project, so I wrapped up Scikit-learn and TensorFlow into something that's actually easy to use.

## What This Thing Does

- **Simplified ML Interfaces** — No more digging through docs for hours. Just call `Classifier()` and go.
- **Auto Data Preprocessing** — It cleans your data for you. Missing values? Categorical columns? Handled.
- **Hyperparameter Tuning** — Built-in grid search and Bayesian optimization so you don't have to guess.
- **Model Comparison** — Train 3 models at once and see which one wins side-by-side.
- **Export & Deploy** — Save to Pickle, ONNX, or TensorFlow Serving. Whatever you need.
- **Pretty Charts** — Learning curves, confusion matrices, feature importance. Looks good in presentations.
- **Explainable AI** — SHAP and LIME built-in so you can actually explain why your model predicted something.

## What You Need Before Starting

- Python 3.8 or newer
- pip (should come with Python)

## How to Install It

### The Easy Way

```bash
pip install mltoolkit
```

### If You Want Everything (Recommended)

```bash
pip install mltoolkit[full]
```

This gets you TensorFlow, all the viz tools, everything.

### If You Want to Hack On It

```bash
git clone https://github.com/Smokey232607/mltoolkit.git
cd mltoolkit
pip install -e .
```

## Quick Start — Copy This and Run It

```python
from mltoolkit import AutoModel, DataLoader

# Load your data
data = DataLoader.from_csv("data.csv")
X_train, X_test, y_train, y_test = data.split(target="target")

# Train a model (AutoModel picks the best algorithm for you!)
model = AutoModel(task="classification")
model.fit(X_train, y_train)
results = model.evaluate(X_test, y_test)

# Save it
model.save("model.pkl")
```

That's literally it. Five lines and you have a trained model.

## How to Actually Use It

### Cleaning Your Data

```python
from mltoolkit.preprocessing import AutoPreprocessor

preprocessor = AutoPreprocessor()
X_clean = preprocessor.fit_transform(X_raw)
```

### Training a Specific Model

```python
from mltoolkit.models import Classifier
from mltoolkit.training import Trainer

model = Classifier(algorithm="random_forest")
trainer = Trainer(model)
trainer.fit(X_train, y_train)
```

### Tuning Hyperparameters (The Smart Way)

```python
from mltoolkit.training import HyperOptimizer

optimizer = HyperOptimizer(model, search_space={
    "n_estimators": [100, 200, 500],
    "max_depth": [5, 10, None]
})
best_model = optimizer.search(X_train, y_train, method="bayesian")
```

### Comparing Models

```python
from mltoolkit.evaluation import ModelComparator

comparator = ModelComparator([model1, model2, model3])
comparator.compare(X_test, y_test)
comparator.plot_results()  # Spits out a nice chart
```

### Making Pretty Charts

```python
from mltoolkit.visualization import LearningCurvePlotter

plotter = LearningCurvePlotter(trainer.history)
plotter.plot(save_path="learning_curve.png")
```

### Exporting for Production

```python
from mltoolkit.deployment import ModelExporter

exporter = ModelExporter(format="onnx")
exporter.export(model, "model.onnx")
```

## Configuration

MLToolkit looks for a `config.yaml` in your project root. Here's what mine looks like:

```yaml
mltoolkit:
  random_seed: 42
  default_device: "cpu"  # change to "gpu" if you have one
  logging_level: "INFO"
  cache_dir: "./cache"
```

Or just set stuff in code:

```python
from mltoolkit import config
config.set("random_seed", 123)
```

## How the Code Is Organized

```
mltoolkit/
├── mltoolkit/
│   ├── preprocessing/      # Cleans and fixes your data
│   ├── models/            # The actual ML algorithms
│   ├── training/          # Training loops and hyperparameter search
│   ├── evaluation/        # Metrics and comparing models
│   ├── visualization/     # Charts and graphs
│   └── deployment/        # Getting your model out into the world
├── examples/              # Working code examples you can copy
├── notebooks/             # Jupyter notebooks with tutorials
└── tests/                 # Unit tests so stuff doesn't break
```

## When Stuff Goes Wrong

### "ModuleNotFoundError" or Import Errors

You probably didn't install the full package. Try:

```bash
pip install mltoolkit[full]
```

### GPU Not Showing Up

If you're using TensorFlow and it can't see your GPU, check that CUDA and cuDNN are installed. Or just use CPU — it's fine for small stuff.

```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Running Out of Memory

Your dataset might be too big. Turn on chunked processing:

```python
from mltoolkit import config
config.set("chunk_size", 10000)
```

### ONNX Export Fails

You need the ONNX libraries:

```bash
pip install onnx onnxruntime
```

## Want to Contribute?

I'd love help! Here's how:

1. Fork the repo
2. Make a branch: `git checkout -b feature/cool-new-thing`
3. Commit your stuff: `git commit -m 'Added cool new thing'`
4. Push it: `git push origin feature/cool-new-thing`
5. Open a Pull Request

Please run the tests first so nothing breaks:

```bash
pytest tests/
```

## License

MIT License — do whatever you want with it. See [LICENSE](LICENSE) for the legal text.

## Shoutouts

- [Scikit-learn](https://scikit-learn.org/) for doing the heavy lifting on classical ML
- [TensorFlow](https://tensorflow.org/) for the deep learning stuff
- [SHAP](https://shap.readthedocs.io/) for making models explainable
- [Matplotlib](https://matplotlib.org/) and [Plotly](https://plotly.com/) for the charts
