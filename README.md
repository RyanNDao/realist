# Realist

## Overview
Realist is a tool designed to assist real estate buyers by analyzing property listings. It scrapes real estate listing websites for home data and sends the data into a database to be stored. In the future, the tool will provide insights that help users make informed purchasing decisions.

## Installation

To set up the project environment, follow these steps:

### Prerequisites
- Ensure Python 3.11 and Poetry are installed on your machine.

### Setup
1. Clone the repository:
    ```bash
    git clone git@github.com:RyanNDao/realist.git
    cd realist
    ```
2. Install dependencies
    ```bash
    poetry install
    ```

## Testing
To run tests and ensure the functionality of the application, use the following command:
``` bash
poetry run pytest .
```
This command executes all tests written for the Realist application, ensuring that all components function correctly as expected.

## Future Features

### Data Analysis Enhancements: 
Implementation of advanced analytics to assess market trends and predict future property values.

### Recommendation Engine: 
Development of a recommendation system using large language models (LLMs) to provide personalized buying suggestions based on user preferences and historical data.
