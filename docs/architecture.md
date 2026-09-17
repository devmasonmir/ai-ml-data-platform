# AI & ML Data Platform Architecture

## Design
1. **Feature Ingestion**: Ingests cleansed Delta Lake entities into standardized Feature Views.
2. **Point-in-Time Correctness**: As-of joins prevent data leakage during offline training set creation.
3. **Drift Monitoring**: Calculates Population Stability Index (PSI) with alert triggers at PSI > 0.2.
