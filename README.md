
## PROJECT REQUIREMENTS

Property Pulse UK aims to provide users with a powerful property price search tool and, eventually, predictive insights for future property values using machine learning.

The project requires a robust ETL pipeline to automatically download monthly UK property price data from the Land Registry’s public dataset, store it in a structured format, and prepare it for both analysis and application use. The pipeline must:
- Fetch new monthly data from a fixed URL.
- Store each month’s dataset in a versioned folder structure (data/raw/YYYY-MM).
- Clean and standardise the data, handling missing values and ensuring consistent formats (e.g., dates, currency, location fields).
- Integrate and combine monthly datasets into a unified historical dataset.
- Prepare the dataset for use in a Streamlit web application, enabling property searches by location, price range, and other filters.
- Maintain a history of all updates to support both current and retrospective property market analysis.

The final processed dataset will form the backbone of the Property Pulse UK app, supporting user-friendly search and future ML-driven property price predictions.

---

## Repository Structure

```bash
├── app
│   └── streamlit                  # Streamlit web application
│       ├── pages                  # Additional pages (Price Tracker, Map, Prediction, etc.)
│       ├── lib                    # Reusable functions/libraries specific to Streamlit
│       └── home.py                # Landing page
│
└── src
│   ├── etl                        # ETL pipeline scripts
│   │   ├── extract                # Extract data from source (HM Land Registry CSVs, APIs)
│   │   ├── load                   # Load cleaned/transformed data into PostgreSQL
│   │   └── transform              # Clean, enrich, and transform raw datasets
│   ├── model                      # Machine learning models (training, evaluation, prediction)
│   └── utils                      # General helper functions (logging, validation, file handling)
│
└── data
│   ├── mapping                    # Mapping tables (e.g., GeoJSON keys)
│   ├── marts                      # Analytical data marts
│   │   ├── fact_prices            # Fact table of property price transactions for analysis
│   │   └── fact_prediction        # Fact table of property price transactions for prediction
│   ├── raw                        # Raw downloaded datasets
│   └── transformed                # Cleaned & feature-engineered datasets ready for analysis
│
└── tests
│   └── unit_tests                 # Unit tests for ETL, models, and utilities
│
└── logs                           # Log files from ETL jobs and ML models
│
└── models                         # Saved ML models (Pickle file)
│
└── scripts                        # Automation script (run pipeline)
│
└── notebooks                      # Jupyter notebooks for EDA, prototyping, experimentation
│
└── config                         # Configuration files (DB connections, credentials, constants)
```    
---

## PROJECT REQUIREMENTS AS AN EPIC

```text
As a DA/DS and PROPERTY PULSE UK USER,
I want a robust ETL pipeline that automatically fetches, 
cleans, and standardises monthly UK property price data 
from public Land Registry CSV sources, storing each update 
in a versioned format and merging it with historical records,
So that I can search, analyse, and track property price trends 
over time in the Property Pulse UK app, and in the future, 
receive data-driven predictions on property values
powered by machine learning.
```

---

## EPIC 1

```text
As a Data Analyst/Scientist,
I want to have a robust extraction process that can download, 
track, and store UK property price data and supporting geospatial 
data, so that the ETL pipeline can reliably maintain both full 
historical records and monthly updates ready for transformation, 
analysis, and visualisation.
```

## EPIC 2

```text
As a Data Analyst/Scientist,
I want to transform and standardise the raw property 
price datasets so that they are clean, consistent, and 
geospatially compatible with the GeoJSON location data,
so that the data can be reliably joined, visualised, and
analysed within the Streamlit application and future 
machine learning models.
```

## EPIC 3

```text
As a Data Analyst/Scientist,
I want the extracted and transformed property price data 
to be loaded into a single, well-structured SQL table, 
so that I can efficiently query, analyse, and generate 
insights on UK property prices.
```

## EPIC 4

```text
As a Property Pulse UK user,
I want to access the extracted and transformed property 
price data through an intuitive, interactive interface, 
so that I can easily search, explore, and visualise 
property price trends across the UK.
```

---

## EPIC Breakdown

### EPIC 1

```text
As a Data Analyst/Scientist,
I want to have a robust extraction process that can download, 
track, and store UK property price data and supporting geospatial 
data, so that the ETL pipeline can reliably maintain both full 
historical records and monthly updates ready for transformation, 
analysis, and visualisation.
```

#### USER STORY 1

```text
As a Data Analyst/Scientist,
I want to access the UK property price dataset, both 
full history and monthly updates, from the Land Registry, 
so that I can maintain an up-to-date raw dataset for 
downstream processing.
```

#### USER STORY 2

```text
As a Data Analyst/Scientist,
I want to have access to stored extracted property data 
in an efficient, organised format, so that the data can be 
read quickly and easily by downstream processes.
```

#### USER STORY 3

```text
As a Data Analyst/Scientist,
I want to have access to Local Authority GeoJSON boundaries,
so that the property price data can be accurately mapped for 
visualisation in the Streamlit app.
```

---

### EPIC 2

```text
As a Data Analyst/Scientist,
I want to transform and standardise the raw property 
price datasets so that they are clean, consistent, and 
geospatially compatible with the GeoJSON location data,
so that the data can be reliably joined, visualised, and
analysed within the Streamlit application and future 
machine learning models.
```

#### USER STORY 1

```text
As a Data Analyst/Scientist,
I want to have clean, validated, and standardised property 
price dataset — including dates, currency, categories, and 
location identifiers, so that the data is accurate, consistent, 
and ready for reliable analysis and visualisation.
```

#### USER STORY 2

```text
As a Data Analyst/Scientist,
I want to have access to a single dataset with monthly updates merged into the historical 
dataset and enrich each record with spatial identifiers, 
so that the dataset remains complete, up-to-date, and 
ready for geospatial analysis.
```

### EPIC 3

```text
As a Data Analyst/Scientist,
I want the extracted and transformed property price data 
to be loaded into a single, well-structured SQL table, 
so that I can efficiently query, analyse, and generate 
insights on UK property prices.
```

### EPIC 4

```text
As a Property Pulse UK user,
I want to access the extracted and transformed property 
price data through an intuitive, interactive interface, 
so that I can easily search, explore, and visualise 
property price trends across the UK.
```

---

## KANBAN BOARD
### EPIC 1 User stories and tasks

```mermaid
kanban
    Epics
        (Epic 1: As a Data Analyst/Scientist, I want to have a robust extraction process that can download, track, and store UK property price data and supporting geospatial data, so that the ETL pipeline can reliably maintain both full historical records and monthly updates ready for transformation, analysis, and visualisation.)

        (Epic 2: As a Data Analyst/Scientist, I want to have raw property price datasets transformed and standardised the so that they are clean, consistent, and geospatially compatible with the GeoJSON location data, so that the data can be reliably joined, visualised, and analysed within the Streamlit application and future machine learning models.)

        (Epic 3: As a Data Analyst/Scientist, I want the extracted and transformed property price data to be loaded into a single, well-structured SQL table, so that I can efficiently query, analyse, and generate insights on UK property prices.)

        (Epic 4: As a Property Pulse UK user, I want to access the extracted and transformed property price data through an intuitive, interactive interface, so that I can easily search, explore, and visualise property price trends across the UK.)

    (E1 Story 1: As a Data Analyst/Scientist, I want to access the UK property price dataset, both full history and monthly updates, from the Land Registry, so that I can maintain an up-to-date raw dataset for downstream processing.)
        No tasks left.

    (E1 Story 2: As a Data Analyst/Scientist, I want to have access to Local Authority GeoJSON boundaries, so that the property price data can be accurately mapped for visualisation in the Streamlit app.)
        No tasks left.

    (E1 Story 3: As a Data Analyst/Scientist, I want to have access to stored extracted property data in an efficient, organised format, so that the data can be read quickly and easily by downstream processes.)
        Task 3.5: Unit test: extract.py
        Task 3.12: Unit test: logging_utils.py
        
        
    Done
        Task 1.1: Create Python script to ingest CSV from data source using stream=True
        Task 1.2: Implement logic that will store the downloaded file as a temp file and replace if process successful
        Task 1.3: Create extract "master" script to orchestrate all functions
        Task 1.4: Implement logic so that full and monthly fetches are possible
        Task 1.5: Add function to determine if full or monthly download is required
        Task 1.6: Add JSON state file to track last fetch date
        Task 1.7: Task 7: Add helper script to return -resolve- output path and url based on full_done
        Task 2.1: Fetch GeoJSON from source
        Task 2.2: Store in "data/mapping/" folder
        Task 3.1: Organise pp data into folder structure in "data/raw/YYYY-MM" format
        Task 3.2: Add inline comments as best practice
        Task 3.3: Add logging for extract step as best practice
        Task 3.4: Add docstrings for each function as best practice
        Task 3.6: Unit test: fetch_data.py
        Task 3.7: Unit test: fetch_geojson.py
        Task 3.8: Unit test: date_utils.py
        Task 3.9: Unit test: state_utils.py
        Task 3.10: Unit test: geojson_utils.py
        Task 3.11: Unit test: path_resolve_utils.py
     
```

### EPIC 2 User stories and tasks

```mermaid
kanban
    Epics
        (Epic 1: As a Data Analyst/Scientist, I want to have a robust extraction process that can download, track, and store UK property price data and supporting geospatial data, so that the ETL pipeline can reliably maintain both full historical records and monthly updates ready for transformation, analysis, and visualisation.)

        (Epic 2: As a Data Analyst/Scientist, I want to have raw property price datasets transformed and standardised the so that they are clean, consistent, and geospatially compatible with the GeoJSON location data, so that the data can be reliably joined, visualised, and analysed within the Streamlit application and future machine learning models.)

        (Epic 3: As a Data Analyst/Scientist, I want the extracted and transformed property price data to be loaded into a single, well-structured SQL table, so that I can efficiently query, analyse, and generate insights on UK property prices.)

        (Epic 4: As a Property Pulse UK user, I want to access the extracted and transformed property price data through an intuitive, interactive interface, so that I can easily search, explore, and visualise property price trends across the UK.)

    (E2 Story 1: As a Data Analyst/Scientist, I want to have clean, validated, and standardised property price dataset — including dates, currency, categories, and location identifiers, so that the data is accurate, consistent, and ready for reliable analysis and visualisation.)
        No tasks left.

    (E2 Story 2: As a Data Analyst/Scientist, I want to have clean, validated, and standardised property price data marts, so that the data is accurate, consistent, and optimized for reliable analysis and visualisation in Streamlit.)
        No tasks left.

    Done
        Task 1.1: Convert CSV to Parquet for performance
        Task 1.2: Implement full vs. monthly logic for CSV transform
        Task 1.3: Add logging in transform.py
        Task 1.4: Check for null values
        Task 1.5: Check for duplicate rows
        Task 1.6: Create schema for parquet file
        Task 1.7: Standardize datetime column
        Task 1.8: Standardize postcode column
        Task 2.1: Data mart: Monthly average price and transaction count by, district, property_type, year, month for price tracker
        Task 2.2: Data mart: Monthly average price by, district, year, month for price tracker
        Task 2.3: Min/Max price in the last 5 years by district for ML model
        Task 2.4: Write a partitioned parquet - data mart - by year and month, using dynamic overwrite if incremental
        Task 2.5: Incorporate marts.py with master transform script
        
```

### EPIC 3 User stories and tasks

```mermaid
kanban
    Epics
        (Epic 1: As a Data Analyst/Scientist, I want to have a robust extraction process that can download, track, and store UK property price data and supporting geospatial data, so that the ETL pipeline can reliably maintain both full historical records and monthly updates ready for transformation, analysis, and visualisation.)

        (Epic 2: As a Data Analyst/Scientist, I want to have raw property price datasets transformed and standardised the so that they are clean, consistent, and geospatially compatible with the GeoJSON location data, so that the data can be reliably joined, visualised, and analysed within the Streamlit application and future machine learning models.)

        (Epic 3: As a Data Analyst/Scientist, I want the extracted and transformed property price data to be loaded into a single, well-structured SQL table, so that I can efficiently query, analyse, and generate insights on UK property prices.)

        (Epic 4: As a Property Pulse UK user, I want to access the extracted and transformed property price data through an intuitive, interactive interface, so that I can easily search, explore, and visualise property price trends across the UK.)

    (E3 Story 1: As a Data Analyst/Scientist, I want to have clean, validated, and standardised property price dataset — including dates, currency, categories, and location identifiers, so that the data is accurate, consistent, and ready for reliable analysis and visualisation.)
        No tasks left.

    (E3 Story 2: As a Data Engineer, I want DB credentials and target names sourced from .env file, so that they can be easily changed if switching between environments.)
        No tasks left.

    Done
        Task 1.1: Read parquet file with a configurable row limit - 10k
        Task 1.2: Build DB URL from .env, or use TARGET_DB_URL if present, and create a SQLAlchemy engine
        Task 1.3: Write data to Postgres
        Task 1.4: Implement logging in load.py
        Task 2.1: Read TARGET_DB_* pieces from .env and compose URL with util function
        Task 2.2: Provide get_target to read TARGET_DB_SCHEMA and TARGET_DB_TABLE
        Task 2.3: Ensure .env is git-ignored
        
```

### EPIC 4 User stories and tasks

```mermaid
kanban
    Epics
        (Epic 1: As a Data Analyst/Scientist, I want to have a robust extraction process that can download, track, and store UK property price data and supporting geospatial data, so that the ETL pipeline can reliably maintain both full historical records and monthly updates ready for transformation, analysis, and visualisation.)

        (Epic 2: As a Data Analyst/Scientist, I want to have raw property price datasets transformed and standardised the so that they are clean, consistent, and geospatially compatible with the GeoJSON location data, so that the data can be reliably joined, visualised, and analysed within the Streamlit application and future machine learning models.)

        (Epic 3: As a Data Analyst/Scientist, I want the extracted and transformed property price data to be loaded into a single, well-structured SQL table, so that I can efficiently query, analyse, and generate insights on UK property prices.)

        (Epic 4: As a Property Pulse UK user, I want to access the extracted and transformed property price data through an intuitive, interactive interface, so that I can easily search, explore, and visualise property price trends across the UK.)

    (E4 Story 1: As a Property Pulse UK user, I want to view average property prices by local authority on a map and filter those prices by year and property type so I can quickly compare areas.)
		Task 1.7: Test: Unit test join logic - names vs codes; visual smoke test.
		Task 1.8: Test: Filter combos; empty state.

    (E4 Story 2: As a Property Pulse UK user, I want to select multiple districts and see price trends over time as well as % change between the first and last year in range for each district, so I can compare areas.)
        Task 2.5: Compute start/end per district - no extra aggregation if mart is yearly.
		Task 2.6: Display as compact cards or table; sort by % change.
        Task 2.7: Test: Edge cases - empty selection, single district.
		Task 2.8: Test: Correctness when years are missing for some districts.
    
    (E4 Story 3: As a Property Pulse UK user, I want a 5-year price forecast, with uncertainty, for a specific district, property type, new build, and tenure, anchored to my asking price.)
        Task 3.5: Test: Segment with data; segment without data; extreme asking prices.

    (E4 Story 4: As a Property Pulse UK user,  I want to simulate a one-off downturn in the future  to see impact on the 5-year path.)
        Task 4.1: Implement shock by selecting in which of the next 5 years it happens and update chart/table.
        Task 4.2: Implement shock by selecting a downturn in percentages on a slider and multiply subsequent ratios; update chart/table.
        Task 4.3: Test: Shock off vs on; different years and different percentages.
    
    Done
        Task 1.1: Ensure fact_by_district mart includes district, year, property_type, avg_price.
        Task 1.2: Build Streamlit page with PyDeck GeoJsonLayer; tooltips; initial view state.
		Task 1.3: Implement detect_name_field and normalize_name; join mart → GeoJSON.
		Task 1.4: Cache mart and GeoJSON - @st.cache_data/@st.cache_resource.
        Task 1.5: Year selectbox, custom property type control, icons → values D/S/T/F/All.
		Task 1.6: Verify mart has rows for all combinations; handle empty results.
        Task 2.1: Ensure mart has district, year, avg_price; drop property_type='O' rows.
		Task 2.2: Altair line chart; nearest point interaction; tooltip.
		Task 2.3: Year range slider; district multiselect - no default.
		Task 2.4: Cache the dataframe; pre-coerce numeric dtypes.
        Task 3.1: Read parquet once; fit log-linear trend per segment; store params {a,b,rmse,last_year,mu_last} in models/lintrend_params.pkl.
        Task 3.2: Save category vocab to drive UI dropdowns.
        Task 3.3: Load pickle; compute absolute forecast; anchor to asking price using ratios vs mu_last.
        Task 3.4: Chart with band; details table; comparison vs current average via load_fact_by_district.
        
```