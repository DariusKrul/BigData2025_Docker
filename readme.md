# bigdata-task2-krul

CLI utility that produces descriptive statistics for any CSV. Packaged as a Docker image.

## Prerequisites
* Docker 24+ installed and running.
* A CSV file to test with (e.g. `iris.csv`).

## Utility test
For test a sample.csv was created that consisted of two columns and two rows.
Output creates two summary files: one csv and one parquet.

## Build the image
```bash
docker build -t kruel1/bigdata-task2-krul:1.0 .

