# Jupyter notebooks for TourPerret2G4

## Prepare CSV files

```bash
nvm use stable
npm i @json2csv/cli
```

```bash
json2csv -i dataset-perret-multichan_gateway_1.log > dataset-perret-multichan_gateway_1.csv
json2csv -i dataset-perret-multichan_gateway_2.log > dataset-perret-multichan_gateway_2.csv
json2csv -i dataset-perret-multisf_gateway_2.log > dataset-perret-multisf_gateway_2.csv
```

## Launch Jupyter Notebook

```bash
jupyter notebook
```

Coming soon

