# sfdc-profile-merge
A python script that takes two salesforce profile metadata files and merges them (prioritizing one).

## Requirements
You must have the following installed on your machine and available in your PATH:
- python 3 
- python package "lxml", install with ```pip3 install lxml```

## Usage
Clone this repo and open a terminal in the folder.

Run the following
```
python3 main.py -in <path to input profile> -to <path to profile being overwritten> -o <path to output file>
```

## Known Issues
1. This package will not work if the profiles contain ```profileActionOverrides```.
