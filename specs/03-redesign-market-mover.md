# Specification: Consolidated DSE & CSE Market Performance Table

## 1. Overview

Replace the four separate market performance tables with a single, tab-based market data table.

The consolidated table will display four categories:

1. Gainers
2. Losers
3. Highest Value
4. Highest Volume

Users can switch between DSE and CSE using an exchange selector.

Only one category table should be displayed at a time.

## 2. User Interface Requirements

### 2.1 Exchange Selector

Provide two exchange options:

- DSE – Dhaka Stock Exchange
- CSE – Chittagong Stock Exchange

When the user selects an exchange, display only the corresponding exchange's market data.

### 2.2 Category Tabs

Provide four tabs:

| Tab | Sorting Logic | Records |
|---|---|---|
| Gainers | Change (%) descending | Top 10 |
| Losers | Change (%) ascending | Top 10 |
| Highest Value | Value descending | Top 10 |
| Highest Volume | Volume descending | Top 10 |

Only one category should be active at a time.

### 2.3 Table Columns

Display columns according to the selected category.

| Tab | Columns |
|---|---|
| Gainers | Instrument, LTP, YCP, Change, Change (%) |
| Losers | Instrument, LTP, YCP, Change, Change (%) |
| Highest Value | Instrument, LTP, YCP, Change, Change (%), Value |
| Highest Volume | Instrument, LTP, YCP, Change, Change (%), Volume |

Keep the table header consistent with the selected category.

## 3. Business Logic and Sorting Rules

### 3.1 Gainers

- Sort by Change (%) in descending order.
- Display the highest positive percentage change first.
- Display the top 10 instruments.

### 3.2 Losers

- Sort by Change (%) in ascending order.
- Display the most negative percentage change first.
- Display the top 10 instruments.

### 3.3 Highest Value

- Sort by traded value in descending order.
- Display the highest traded value first.
- Display the top 10 instruments.

### 3.4 Highest Volume

- Sort by traded volume in descending order.
- Display the highest traded volume first.
- Display the top 10 instruments.

### 3.5 Additional Sorting Rules

- Apply sorting independently for DSE and CSE.
- Use numeric values for sorting, not formatted strings.
- Exclude records with missing or invalid sorting values.
- Use instrument symbol in ascending order as a secondary sorting criterion when values are equal.
- Do not modify the original API data.

## 4. Data and API Integration

Before implementation, inspect the existing API endpoints and data structures.

Reuse the existing market data sources that currently populate the four separate tables.

Requirements:

1. Maintain existing DSE and CSE API integrations.
2. Do not introduce hardcoded stock data.
3. Do not change backend APIs or database schemas.
4. Reuse existing API responses wherever possible.
5. Avoid unnecessary duplicate API requests when switching tabs.
6. Recalculate sorting and top 10 records from the available market data.

If the existing API already returns sorted and limited records, verify whether its sorting matches the required business rules before reusing that result.

## 5. Visual Design

Maintain the existing premium dark theme.

| Element | Color |
|---|---|
| Background | `#0B1120` |
| Table Background | `#111B2D` |
| Table Header | `#1C2940` |
| Primary Text | `#F1F5F9` |
| Secondary Text | `#CBD5E1` |
| Borders | `#2A3850` |
| Positive Change | `#34D399` |
| Negative Change | `#FB7185` |
| Active Tab Accent | `#2DD4BF` |

Additional requirements:

- Highlight the active tab clearly.
- Use green for positive changes and red/pink for negative changes.
- Maintain compact and readable table rows.
- Add subtle row hover highlighting.
- Keep numeric columns right-aligned.
- Avoid unnecessary animations and decorative elements.

## 6. Responsive Design

### Desktop
- Full-width market table.
- Exchange selector and four horizontal tabs.
- Display all relevant columns without clipping.

### Tablet
- Maintain horizontal tabs where possible.
- Ensure table columns remain readable.

### Mobile
- Allow horizontal scrolling for the table if necessary.
- Prevent text clipping and column overlap.
- Maintain accessible exchange and tab controls.

## 7. Loading and Error Handling

Implement appropriate states:

- **Loading:** Display an indicator while fetching data.
- **Empty:** Display an appropriate message when no instruments match the selected category.
- **Error:** Display an error message if the API request fails.
- **State preservation:** Preserve the selected exchange and tab when refreshing data, where appropriate.

## 8. Acceptance Criteria

1. Four separate tables are replaced by one tab-based table.
2. DSE and CSE data can be selected independently.
3. All four tabs display the correct category.
4. Sorting follows the specified business rules.
5. Each category displays a maximum of 10 records.
6. Switching tabs does not unnecessarily reload the entire dashboard.
7. Existing API integrations and business logic remain unchanged.
8. The design matches the website's existing dark theme.
9. All data remains readable on desktop, tablet, and mobile.

## 9. Technical Constraints

- Frontend-only implementation.
- Do not modify backend code or database structures.
- Do not change existing market data calculations.
- Reuse existing components and API services.
- Avoid unnecessary dependencies.
- Inspect the current implementation before modifying files.
- Maintain existing functionality and integrations.

## 10. Implementation Approach

1. Inspect the four existing DSE/CSE market performance tables.
2. Identify their API endpoints, data structures, and current sorting behavior.
3. Identify reusable components and existing styling conventions.
4. Implement a reusable market performance table component.
5. Implement the DSE/CSE exchange selector.
6. Implement the four category tabs.
7. Implement the required sorting and top 10 filtering logic.
8. Integrate existing API responses.
9. Apply the existing dark-theme design.
10. Verify responsiveness and all sorting scenarios.

## Final Instruction

First inspect the existing implementation and identify the data sources and sorting behavior of the four market performance tables.

Then consolidate them into a reusable tab-based component with an exchange selector.

Verify all four sorting scenarios independently for both DSE and CSE.

Do not modify backend functionality, API contracts, database structures, or existing market data calculations.