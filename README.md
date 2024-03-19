# divvy-analysis


### Data
- You can find an overview of the data Divvy currently makes available [here](https://divvybikes.com/system-data).
- Trip history data, in particular, is found [here](https://divvy-tripdata.s3.amazonaws.com/index.html).


### Local Database
1. Install postgres, if you don't have it, with:
    ```bash
    brew install postgresql@16
    ```

1. Then, start postgres with:
    ```bash
    brew services start postgresql@16
    ```

1. Manually create a database named `divvy`, before connecting to postgres, with:
    ```bash
    createdb divvy
    ```

1. You can then connect to it with:
    ```bash
    psql divvy
    ```