# Detecting Malicious Android Apps Using App Permissions
The goal of this project is to predict whether an Android application is malicious, given
the app’s required permissions.

## Authors
* **Matthew Cairns** - [MattCairns](https://github.com/MattCairns)
* **Tim Salomonssons**  - [tsalomon](https://github.com/tsalomon)


### Project Structure

    .
    ├── data                   # Built datasets for training model
    ├── report                 # Our project report files
    ├── src                    # Source files
    │   ├── algorithms         # Algorithms used for training dataset
    │   ├── process            # Scripts for building dataset and downloading apks
    │   └── utils              # Basic utilities for extracting apks, connecting to sftp etc.
    └── README.md

### Acknowledgments
* Malicious app dataset provided by [Kooduous](https://koodous.com/)
