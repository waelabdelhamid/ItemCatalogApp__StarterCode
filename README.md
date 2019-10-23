# Item Catalog App
Source code for `Item Catalog Web Application` Project.

The Catalog App provides a `list of items within a variety of categories` as well as provide a `user registration`, and `authentication system`. Registered users will have the `ability to post, edit and delete` for their own items. And `make APIs requests`.

## Prerequisites

Made in Python 2.7 using Flask web development framework, SQLite database, and Html & CSS utilizes the off-canvas layout with styles making use of the flexbox.

*How To install:*
  * Install Python 2.7 from the python web site https://www.python.org/downloads/release/python-2712/
  * The required database file `catalogitems db` will automatically created in the runtime using `models.py` file which is already imported to the main application file `application.py`. So after the first-run, the database file will created empty in the downloaded project folder, but for a testing purpose I already include the populated database file in the repo.
  * Install Flask& its dependencies using Python's package manager pip from the shell like (`terminal` on Mac or Linux), or from `git bash` on Windows by running:
      ```
      pip install -r /path/to/requirements.txt
      ```
      *Where the `path to` is the downloaded project folder path.*

## Features

* Implements login using Google Sign in.
* Implements Basic Authentication for APIs using Token generation for registered users.
* All content is responsive and displays on all display sizes.

## Examples

| [Nexus Show Catalog Item](https://1.bp.blogspot.com/-DnwkCmvYsUU/Xauz5krq_0I/AAAAAAAAAWE/CsGblMUevXEp53THGj1ZA_eE7jlnXNluwCLcBGAsYHQ/s1600/2019-10-19%2B%25283%2529NexasShowCatalogItem.png)
| [Nexus Catalogs Main Panel](https://1.bp.blogspot.com/-MMD0n0FmZcc/Xauz0iUrwiI/AAAAAAAAAV8/zgAPqVeJX2McYEAey7Y0dyGUzxC-xLU0gCLcBGAsYHQ/s1600/2019-10-19%2B%25284%2529NexasCatalogsRight.png)
| [Nexus Catalogs Menu](https://1.bp.blogspot.com/-R3NT58Rr5xw/Xauz0x6aylI/AAAAAAAAAWA/px5tVCiU-KcKsuPu4xePVZSVFd9pXcY3QCLcBGAsYHQ/s1600/2019-10-19%2B%25285%2529NexasCatalogsMenu.png)
| [Nexus Catalog Items](https://1.bp.blogspot.com/-ulAOxQ6MLUg/Xauz6sndPQI/AAAAAAAAAWI/A40QXValeWY8HZ-1693n2rnZnnZs-d7rACLcBGAsYHQ/s1600/2019-10-19%2B%25286%2529NexasCatalogItems.png)
| [Catalog Items](https://1.bp.blogspot.com/-nGpZ3iIxQPM/Xauz6-ai5tI/AAAAAAAAAWM/qd8BRRDxTckET60atrzJ1eRoq0yuyToIwCLcBGAsYHQ/s1600/2019-10-19%2B%25287%2529CatalogItems.png)
| [Catalogs](https://1.bp.blogspot.com/-rskUyaBmRYA/Xauz7b_PvxI/AAAAAAAAAWQ/aGOAxqUtGqYdB00y4pu2uTXKAmLimTy6ACLcBGAsYHQ/s1600/2019-10-19%2B%25288%2529Catalogs.png)
| [Flash Login](https://1.bp.blogspot.com/-oQ5MEHT-sPg/Xauz7gmbVAI/AAAAAAAAAWU/N_5Or9qffRQf70gU3WVJzfzr2Om7WB4GACLcBGAsYHQ/s1600/2019-10-19%2B%25289%2529Flash.png)
| [Add Item](https://1.bp.blogspot.com/-fqBXLT7wt_o/XauzwlBO6KI/AAAAAAAAAVk/PLPJHa4KVT4LBPTDqiaICwlOYS15nSFowCLcBGAsYHQ/s1600/2019-10-19%2B%252810%2529Add.png)
| [Show Catalog Item with Edit& Delete links](https://1.bp.blogspot.com/-Kbiigp__8Zw/Xauzwhca6mI/AAAAAAAAAVs/GsE4b0Aa06syQNcsnQaJFvwyAvjsiI66gCLcBGAsYHQ/s1600/2019-10-19%2B%252811%2529ShowCatalogItem.png)
| [Edit Item](https://1.bp.blogspot.com/-tKEgR4UIklg/XauzwoS5fwI/AAAAAAAAAVo/P8Jf8_n7t9kma6_vaJnqaOw1oUe1ey1sgCLcBGAsYHQ/s1600/2019-10-19%2B%252812%2529Edit.png)
| [Delete Item](https://1.bp.blogspot.com/-pRd7YATQmUQ/Xauzxl-KKmI/AAAAAAAAAVw/pbIRkWyyjuAudEVrc3KOwzanU9WiuPERACLcBGAsYHQ/s1600/2019-10-19%2B%252813%2529Delete.png)
| [Show Category JSON](https://1.bp.blogspot.com/-2xTVfM8py7Y/XauzyH3iuMI/AAAAAAAAAV0/fEH1CPq6Rg41WTMlgOtNd8GwXfoSvc20ACLcBGAsYHQ/s1600/2019-10-19%2B%252814%2529JSON.png)
| [Login](https://1.bp.blogspot.com/-eBFI33Otl14/XbBO-YyhrZI/AAAAAAAAAXI/-o40tYoOiAMoipprheExyNw3pF-4qDSPQCLcBGAsYHQ/s1600/2019-10-23-Login.png)

## Usage

1. Download the files from GitHub.
2. To start the Catalog App web server Using the terminal, CD to the project folder, then type `python application.py`.
3. Visit this URL http://localhost:8000/ to see the Catalog App web page.
4. To stop the Catalog App web server, press [ctrl+c] from the terminal.

## API Docs

1. The Catalog App API is a RESTful API depends on the HTTP-level request & response for all functionality.
2. The API request must use the GET method to a specific resource EndPoint.
3. The API response will return a JSON object for the available data sets.
4. The Available data sets are the Category, Category Items, and Category Item
5. The Example EndPoints as the following:
  ```
  Data Set: Category
  EndPoint: /catalog/JSON
  Example:  http://localhost:8000/catalog/JSON
  description: find in our category and on all of our items

  Data Set: Category Items
  EndPoint: /catalog/<int:catalog_id>/items/JSON
  Example:  http://localhost:8000/catalog/1/items/JSON
  description: find in a specific category and on all of category items

  Data Set: Category Item
  EndPoint: /catalog/<int:catalog_id>/items/<int:item_id>/JSON
  Example:  http://localhost:8000/catalog/1/items/6/JSON
  description: find in a specific category item
  ```
  ### API Security

  * `make APIs requests` needs a basic Http Authentication, so after login, the `Your APIs Token` link will appear in the page header, click on the link copy the token and use it as a username with blank password when the API Authentication required.
  * `make APIs requests from curl` use the same steps as above but the word `blank` as a password when you fill the `-u` Authentication parameter.

## Troubleshooting

**I'm getting an error about port 8000 is already in use.**
* You can use a few different commands to get list of all port used and process using the port and type of network protocol. It basically depends on the Operating System.
* There are some articles that explain How to find what's running on a given port. I'd suggest searching for these articles and then trying to stop the process to resolve this issue.
* In the case for the Mac OS, this is an article I've found useful: https://www.mkyong.com/mac/mac-osx-what-program-is-using-port-80/
* Also this in case for Windows & Linux: https://www.quora.com/How-do-I-check-which-application-using-port-80
