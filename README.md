# Brewery Scraper

Scrapes the Brewer's Association directory for addresses of member breweries.

### Installation 

Use poetry to install dependencies in a venv

`poetry install`

Get driver google chrome web drive (Ubuntu instructions)

```Shell
wget -N http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo chmod +x chromedriver
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```

Download chrome

```Shell
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update 
sudo apt-get install google-chrome-stable
```

### Usage

`poetry run brewery_scraper.py`

Results will be saved in `brewers_association_addresses.csv`.
