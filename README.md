# YouTube Data Analysis in AWS

This is an end-to-end data engineering project that uses AWS cloud services to analyze YouTube trending video data across multiple regions.

## 📌 Overview

This project simulates a real-world advertising use case where a client wants to understand video trends before investing in YouTube campaigns. The goal is to extract, clean, catalog, and analyze YouTube data from <a href="https://www.kaggle.com/datasets/datasnaek/youtube-new/data" target="_blank">Kaggle</a> to uncover factors that influence video popularity.

## 🧰 Tech Stack

- **AWS S3** - raw and clean data storage  
- **AWS Lambda and AWS Glue** - ETL for JSON to Parquet conversion, Data Catalog and schema crawling
- **AWS Athena** - SQL-based querying of data
- **AWS QuickSight** - Visualize the trends analysis
- **Python, Pandas, AWS Wrangler** - data transformation
   
*Extras* - *IAM Roles, AWS Wrangler, AWS CLI*

## AWS Data Flow Pipeline Digram

<img src="images/Data%20Flow%20Diagram.png" alt="AWS Data Flow Diagram" width="500"/>


## 📊 Sample Insights (from QuickSight)

-  Top trending and frequency by categories and country

![YouTube Dashboard](images/quicksight-viz-1.png)

-  Average video duration vs. view count
-  Weekly trends of video publishing


<sub>*Note: AWS QuickSight dashboards are not public, but visuals and screenshots are available upon request or in this repo.*</sub>

## 📁 Project Structure

- data/              # Sample data or S3 reference
- scripts/           # Lambda, Glue ETL, CLI commands
- images/            # Illustrations

## 📊 Business Objective

Analyze trends across YouTube video categories to:
- Understand what makes videos "trending"
- Guide ad spend targeting by region/category
- Generate real-time dashboards for decision makers
