# discord-cloud

Simple web application to use discord channels as free cloud storage.

<img alt="Screenshot1" width=425 height=365 src="static/Screenshot1.png" />

## Built With

* ![](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
* ![](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)
* ![](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)

## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/lilmirac/discord-cloud.git
   ```
2. Navigate to the project directory
   ```sh
   cd discord-cloud
   ```
3. Enter variables in `.env` file

`BOT_TOKEN="Discord Bot Token"`

`SERVER_ID="ID of server"`

`CHANNEL_ID="ID of channel"`

4. Set up project manually or using docker

    ```sh
   pip install -r requirements.txt
   python main.py
   ```
    ```sh
   docker build -t discord-cloud .
   docker run discord-cloud
   ```

## Usage
* After installation steps you can navigate to `localhost:8000` in your web browser
* You can manage, download, delete existing files, upload new (Up to 25MB / file for now) files
* You can use VPN services for using this service on your other devices

## Contact
Miraç - [contact@mirac.dev](mailto:contact@mirac.dev?subject=[GitHub])

[![Website](https://img.shields.io/badge/website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://mirac.dev)
## License
Distributed under the MIT License. See [License](https://github.com/lilmirac/discord-cloud/blob/main/LICENSE) for more information.

