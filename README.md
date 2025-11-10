# Six Degrees of Kevin Bacon

This project is a Python implementation of the "Six Degrees of Kevin Bacon" game. It uses publicly available data from IMDb to build a graph of actors and their connections. Given an actor's name, it calculates their "Bacon Number" by finding the shortest path to Kevin Bacon in this vast network of co-stars.

## Features

-   Processes large-scale IMDb datasets efficiently using the `pandas` library.
-   Builds a comprehensive graph of actor co-starring relationships using the `networkx` library.
-   Calculates the shortest path between any two actors using the highly efficient Breadth-First Search (BFS) algorithm.
-   Provides a simple command-line interface to easily query for any actor.

## Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
First, clone this repository to your computer:
```bash
git clone https://github.com/kaganmumcu/six-degrees-of-bacon.git
cd SENIN-REPO-ADIN```

### 2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to keep dependencies isolated.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the Dependencies
Install all the necessary Python libraries from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Download the IMDb Data
This project requires three large dataset files from IMDb. **These files are not included in the repository due to their size.**

You must download them manually from [IMDb Datasets](https://datasets.imdbws.com/) and place the `.tsv.gz` files in the root directory of this project.

-   `name.basics.tsv.gz` (Contains actor names and IDs)
-   `title.basics.tsv.gz` (Contains movie titles and IDs)
-   `title.principals.tsv.gz` (Connects actors to movies)

After this step, your project folder should contain these three `.gz` files alongside the Python script.

## Usage

You can run the script from your terminal. Make sure your virtual environment is active.

**To find an actor's path to Kevin Bacon:**
Provide the actor's name in quotes as an argument.
```bash
python3 bacon_game.py "Meryl Streep"
```
```
--- Output ---
Success! The 'Kevin Bacon' number for 'Meryl Streep' is: 1
----------------------------------------------------
1. Meryl Streep was in 'The River Wild' with Kevin Bacon
----------------------------------------------------
```

**To find the path between any two actors:**
Use the `--target` flag to specify a different target actor.
```bash
python3 bacon_game.py "Al Pacino" --target "Robert De Niro"
```
```
--- Output ---
Success! The 'Robert De Niro' number for 'Al Pacino' is: 1
----------------------------------------------------
1. Al Pacino was in 'The Irishman' with Robert De Niro
----------------------------------------------------
```
