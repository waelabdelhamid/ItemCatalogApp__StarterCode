# ItemCatalogApp__StarterCode
Source code for `Item Catalog Web Application` Project.

The Catalog App provides a `list of items within a variety of categories` as well as provide a `user registration`, and `authentication system`. Registered users will have the `ability to post, edit and delete` for their own items. And `make APIs requests`.

Made in Python 2.7 using Flask web development framework, and Html & CSS utilizes the off-canvas layout with styles making use of the flexbox.

## Features

* Implements login using Google Sign in & Facebook.
* Implements Basic Authentication for APIs using Token generation for registered users.
* All content is responsive and displays on all display sizes.

## Examples

[Image 1](https://1.bp.blogspot.com/-DnwkCmvYsUU/Xauz5krq_0I/AAAAAAAAAWE/CsGblMUevXEp53THGj1ZA_eE7jlnXNluwCLcBGAsYHQ/s1600/2019-10-19%2B%25283%2529NexasShowCatalogItem.png)
[Image 2](https://1.bp.blogspot.com/-MMD0n0FmZcc/Xauz0iUrwiI/AAAAAAAAAV8/zgAPqVeJX2McYEAey7Y0dyGUzxC-xLU0gCLcBGAsYHQ/s1600/2019-10-19%2B%25284%2529NexasCatalogsRight.png)
[Image 3](https://1.bp.blogspot.com/-R3NT58Rr5xw/Xauz0x6aylI/AAAAAAAAAWA/px5tVCiU-KcKsuPu4xePVZSVFd9pXcY3QCLcBGAsYHQ/s1600/2019-10-19%2B%25285%2529NexasCatalogsMenu.png)
[Image 4](https://1.bp.blogspot.com/-ulAOxQ6MLUg/Xauz6sndPQI/AAAAAAAAAWI/A40QXValeWY8HZ-1693n2rnZnnZs-d7rACLcBGAsYHQ/s1600/2019-10-19%2B%25286%2529NexasCatalogItems.png)
[Image 5](https://1.bp.blogspot.com/-nGpZ3iIxQPM/Xauz6-ai5tI/AAAAAAAAAWM/qd8BRRDxTckET60atrzJ1eRoq0yuyToIwCLcBGAsYHQ/s1600/2019-10-19%2B%25287%2529CatalogItems.png)
[Image 6](https://1.bp.blogspot.com/-rskUyaBmRYA/Xauz7b_PvxI/AAAAAAAAAWQ/aGOAxqUtGqYdB00y4pu2uTXKAmLimTy6ACLcBGAsYHQ/s1600/2019-10-19%2B%25288%2529Catalogs.png)
[Image 7](https://1.bp.blogspot.com/-oQ5MEHT-sPg/Xauz7gmbVAI/AAAAAAAAAWU/N_5Or9qffRQf70gU3WVJzfzr2Om7WB4GACLcBGAsYHQ/s1600/2019-10-19%2B%25289%2529Flash.png)
[Image 8](https://1.bp.blogspot.com/-fqBXLT7wt_o/XauzwlBO6KI/AAAAAAAAAVk/PLPJHa4KVT4LBPTDqiaICwlOYS15nSFowCLcBGAsYHQ/s1600/2019-10-19%2B%252810%2529Add.png)
[Image 9](https://1.bp.blogspot.com/-Kbiigp__8Zw/Xauzwhca6mI/AAAAAAAAAVs/GsE4b0Aa06syQNcsnQaJFvwyAvjsiI66gCLcBGAsYHQ/s1600/2019-10-19%2B%252811%2529ShowCatalogItem.png)
[Image 10](https://1.bp.blogspot.com/-tKEgR4UIklg/XauzwoS5fwI/AAAAAAAAAVo/P8Jf8_n7t9kma6_vaJnqaOw1oUe1ey1sgCLcBGAsYHQ/s1600/2019-10-19%2B%252812%2529Edit.png)
[Image 11](https://1.bp.blogspot.com/-pRd7YATQmUQ/Xauzxl-KKmI/AAAAAAAAAVw/pbIRkWyyjuAudEVrc3KOwzanU9WiuPERACLcBGAsYHQ/s1600/2019-10-19%2B%252813%2529Delete.png)
[Image 12](https://1.bp.blogspot.com/-2xTVfM8py7Y/XauzyH3iuMI/AAAAAAAAAV0/fEH1CPq6Rg41WTMlgOtNd8GwXfoSvc20ACLcBGAsYHQ/s1600/2019-10-19%2B%252814%2529JSON.png)
[Image 13](https://1.bp.blogspot.com/-_Xk29otGkgQ/XauzyAkDBaI/AAAAAAAAAV4/sI5EnVov814Lhcf_Cpyk5MJJSp7uHxtegCLcBGAsYHQ/s1600/2019-10-19%2B%252815%2529Login.png)

## Installation

* Install Python from the python web site https://www.python.org
* The database connection to the  `catalogitems db` is required, its a sqlite database, will created automatically in the run time.
* Install Flask& its dependencies using Python's package manager pip from the shell like (`terminal` on Mac or Linux), or from `git bash` on Windows
  * If you are on Mac or Linux, then:
    ```
    sudo python3 -m pip install werkzeug==0.8.3
    sudo python3 -m pip install flask==0.9
    sudo python3 -m pip install Flask-login==0.1.3
    sudo python3 -m pip install requests==2.22.0
    sudo python3 -m pip install SQLAlchemy==1.3.6
    sudo python3 -m pip install oauth2client==4.1.3
    sudo python3 -m pip install itsdangerous==1.1.0
    sudo python3 -m pip install passlib==1.7.1
    sudo python3 -m pip install Flask-HTTPAuth==3.3.0
    ```
  * On Windows, as an administrator:
    ```
    python -m pip install werkzeug==0.8.3
    python -m pip install flask==0.9
    python -m pip install Flask-login==0.1.3
    python -m pip install requests==2.22.0
    python -m pip install SQLAlchemy==1.3.6
    python -m pip install oauth2client==4.1.3
    python -m pip install itsdangerous==1.1.0
    python -m pip install passlib==1.7.1
    python -m pip install Flask-HTTPAuth==3.3.0
    ```

## Usage

1. Download the files from GitHub.
2. To start the Catalog App web server Using the terminal, CD to the project folder, then type `python3 application.py`, or on Windows by typing `python application.py`
3. Visit this URL http://localhost:8000/ to see the Catalog App web page.
4. Please notes: `make APIs requests` needs a basic Http Authentication, so after login, the `Your APIs Token` link will appear in the page header, click on the link copy the token and use it as a username without password when the API Authentication required.
5. To stop the Catalog App web server, press [ctrl+c] from the terminal.

## Troubleshooting

**I'm getting an error about port 8000 is already in use.**
* Please run the server on another port: 5000 or 8080, for ex. from the terminal, type `export PORT=5000` and try again.
