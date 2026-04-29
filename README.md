# bigdata-task2-krul

CLI utility that produces descriptive statistics for any CSV. Packaged as a Docker image.

## What it does

Given any CSV file, the tool outputs the following files to the `output/` directory:

- `summary.csv` – descriptive statistics for all columns (`describe()`)
- `summary.parquet` – same as above in Parquet format
- `missing.csv` – missing value count and percentage per column
- `correlations.csv` – Pearson correlation matrix (numeric columns only)
- `dtypes.csv` – column names, data types, null flags, and unique value counts

## Prerequisites

- Docker 24+ installed and running.
- A CSV file to test with (e.g. `sample.csv`).

## Docker Hub image

```
kruel1/bigdata-task2:2.0
```

## Dockerfile

```dockerfile
FROM python:3.13-slim

LABEL maintainer="kruel1" \
      version="2.0" \
      description="CSV statistics CLI – summary, missing values, correlations, dtypes"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "/app/main.py"]
```

## Build the image

```bash
docker build -t kruel1/bigdata-task2:2.0 .
```

## Run the container

```bash
docker run --rm -v ${PWD}/sample.csv:/data/sample.csv -v ${PWD}/output:/app/output kruel1/bigdata-task2:2.0 /data/sample.csv
```

This mounts your local CSV into the container and writes the output files back to a local `output/` folder.

## Utility test

A `sample.csv` was created with two columns (`col1`, `col2`) and two rows of data. Running the container against it produces all output files listed above. The `correlations.csv` is skipped when fewer than 2 numeric columns are present.

## Issues encountered

During the build, `pandas==2.2.4` was initially specified in `requirements.txt` but this version does not exist on PyPI — the 2.x line ends at `2.2.3`. The requirements file was corrected to `pandas==2.2.3` and the build completed successfully.
