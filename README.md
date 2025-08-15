
## PROJECT REQUIREMENTS

A customer has approached us with a requirement to create a data set that their Data Analysts and Data Scientists can work with.

The customer requires a robust ETL pipeline to integrate transaction data from a SQL database and demographic data from a CSV file. The pipeline must clean and standardise the data, remove invalid or incomplete records, and retain only active customers who have spent over $500. Additionally, it should enrich the dataset by calculating total customer spending and average transaction value per customer. This is so the company can target high-value customers with relevant marketing and rewards.  The final dataset must be stored in SQL and updated regularly for accurate analysis.

---


## PROJECT REQUIREMENTS AS AN EPIC

```text
As a THE CUSTOMER,
I want a robust ETL pipeline that integrates, cleans, standardises, and enriches transaction and demographic data from SQL and CSV sources, retaining only active customers who have spent over $500 and calculating total and average spend per customer,
So that high-value customers can be identified and targeted with marketing and rewards, using an up-to-date dataset stored in SQL for accurate analysis.
```

---


## EPIC 1

```text
As a Data Analyst/Scientist,
I want to be able to access the property prices data,
So that it can be transformed ready for analysis.
```

---


## EPIC 2

```text
As a Data Analyst/Scientist,
I want to be able to access clean, standardised, enriched and aggregated property prices data,
So that it can be analysed easier.
```

---


## EPIC 3

```text
As a Data Analyst/Scientist,
I want to be able to access the extracted, transformed data in a single SQL table,
So that analysis can be done on property prices in the UK.
```

---

## EPIC 4

```text
As the product user,
I want to be able to access the extracted, transformed data in through a user-friendly interface,
So that insights on property prices in the UK can be easily visualised.
```

---

## EPIC 1 Breakdown

```text
As a Data Analyst/Scientist,
I want to be able to access the property prices data,
So that it can be transformed ready for analysis.
```

---

### USER STORY 1

```text
As a Data Analyst/Scientist,
I want to be able to access the property prices data from the CSV file,
So that it can be transformed ready for analysis.
```

### USER STORY 2

```text
As a Data Analyst/Scientist,
I want to be able to access the customer data from the parquet file,
So that it can be transformed, ready for analysis
```

### USER STORY 3

```text
As a Data Analyst/Scientist,
I want to be able to perform monthly updates,
So new data can be added to the dataset.
```


---
---

## EPIC 2 Breakdown

```text
As a Data Analyst/Scientist,
I want to be able to access clean, standardised, enriched and aggregated data,
So that it can be analysed easier
```

### USER STORY 3

```text
As a Data Analyst/Scientist,
I want to be able to access cleaned, standardised transaction data,
So that it can be combined with the customer data and made available as a single table
```

### USER STORY 4

```text
As a Data Analyst/Scientist,
I want to be able to access cleaned, standardised customer data,
So that it can be combined with the transaction data and made available as a single table
```

###  USER STORY 5

```text
As a Data Analyst/Scientist,
I want to be able to access the combined, enriched and aggregated transaction and customer data,
So that it can be analysed easier
```

---
---

## EPIC 3 Breakdown

```text
As a Data Analyst/Scientist,
I want to be able to access the extracted, transformed data in a single SQL table,
So that analysis can be done on high value customers
```

### USER STORY 6

```text
As a Data Analyst/Scientist,
I want the cleaned, standardised, enriched and aggregated data to be available in a single SQL table,
So that it can be analysed easier
```

---

```mermaid
kanban
    Epics
        (Epic 1: As a Data Analyst/Scientist, I want to be able to access the property prices data, so that it can be transformed ready for analysis.)
        (Epic 2: As a Data Analyst/Scientist, I want to be able to access clean, standardised, enriched and aggregated property prices data, so that it can be analysed easier.)
        (Epic 3: As a Data Analyst/Scientist, I want to be able to access the extracted, transformed data in a single SQL table, so that analysis can be done on property prices in the UK.)
        (Epic 4: As the product user, I want to be able to access the extracted, transformed data in through a user-friendly interface, so that insights on property prices in the UK can be easily visualised.)
    (Epic 1 Story 1: As a Data Analyst/Scientist, I want to be able to access the property prices data from the CSV/parquet file, so that it can be transformed ready for analysis.)
        Task 1: Create a python script to ingest data in the CSV format from the data source
        Task 2: Create a python script that will be able to ingest both full historic data and monthly updates
        Task 3: Create a python script that will check if full or monthly download is needed
        Task 4: Create a JSON file that will store records for helper function
        Task 5: Create a python script that will check date and return last month
        Task 6: Create a "master" extract python script that will call all other functions
        Task 7: Add comments throughout
        Task 8: Add logging
        Task 9: Add folder structure and keep functions in separate files
        Task 10: Make CSV into parquet file for better performance
    (Epic 1 Story 2: As a Data Analyst/Scientist, I want to be able to access the property prices data from the CSV/parquet file that is mapped onto a UK, so that it can be visually inspected for average prices etc.)
        Task 1: Implement fetching GEOJSON file, local authority level, needed to generate Streamlit map functionality
        Task 2: Fix any inconsistencies between GEOJSON and property prices data, e.g. Bristol, City of -> Bristol
    Done
```

```mermaid
kanban
    Epics
        (Epic 1: As a Data Analyst/Scientist, I want to be able to access the property prices data, so that it can be transformed ready for analysis.)
        (Epic 2: As a Data Analyst/Scientist, I want to be able to access clean, standardised, enriched and aggregated property prices data, so that it can be analysed easier.)
        (Epic 3: As a Data Analyst/Scientist, I want to be able to access the extracted, transformed data in a single SQL table, so that analysis can be done on property prices in the UK.)
        (Epic 4: As the product user, I want to be able to access the extracted, transformed data in through a user-friendly interface, so that insights on property prices in the UK can be easily visualised.)
    (Epic 2 Story 1: As a Data Analyst/Scientist, I want to be able to access the property prices data, so that it can be transformed ready for analysis.)
        Task 1: Portion off a section of data, e.g. 15k rows
        Task 2: Mess data up for cleaning and transform as original data is cleaned already - Courtesy of HM Land Registry -
        Task 3: Check for null values
        Task 4: Check for duplicates
        Task 5: Check the timestamp variable and extract a column "month" and "year"
    Done
        
```