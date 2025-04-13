# Electricity Price Forecasting in Germany (Showcase only)

## Overview
This project implements machine learning models to forecast day-ahead electricity prices in Germany as part of my university course Case Studies. It builds on my previous work that used classical linear models for electricity load forecasting. The project explores decision trees and random forests for more accurate price predictions and is shown for showcase purposes only.

## Data Sources
- Day-ahead electricity prices (provided via Moodle + supplemented from ENTSO-E)
- Actual electricity generation output by type (provided via Moodle)
- Historical weather data (from Open-Meteo API)
- German holidays and time features (engineered)

## Methods
- Data preprocessing: growth rate transformations, NA imputation using Kalman filters with ARIMA
- Decision tree regression models
- Random forest ensemble models
- Feature importance analysis

## Key Results
- Random forest models outperformed decision trees
- Best model: Random forest with all predictors

## Tools Used
- R 4.4.0 with RStudio
- Python (Google Colab)
- FileZilla (FTP)
- LaTeX (Overleaf)

## Time Frame
Data from January 1, 2015 to April 1, 2024

## Project Structure
- Data preprocessing and transformation
- Model implementation with lagged values only
- Model implementation with all predictors
- Feature importance analysis
- One-step-ahead forecasting evaluation
