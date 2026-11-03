# Learning Log

What I learned in each sprint, in my own words.

## Sprint 0: Setup and SAP landscape

- **SAP HANA Cloud** is the database layer: in-memory and columnar, so aggregations over large volumes are very fast. In my BusinessObjects projects, this role was played by Oracle.
- **SAP Datasphere** is the data and semantic layer, similar to a BO universe. Unlike a universe, it can integrate SAP and non-SAP sources and either query data at the source (federation) or replicate it.
- **SAP Analytics Cloud** is the analytics layer, similar to Web Intelligence, with planning and predictive features on top.
- **SAP Business Data Cloud** brings these together, adding ready-made data products managed by SAP.
- **Why Datasphere *and* SAC?** You model the data and business rules once in Datasphere, and every report uses the same version of the truth. It's the same idea as a universe, but at company scale.
