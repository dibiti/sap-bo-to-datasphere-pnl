# From BusinessObjects to SAP Datasphere: a P&L analytics migration

> 🚧 Work in progress, built sprint by sprint. See [LEARNING_LOG.md](LEARNING_LOG.md).

## Why this project

I'm a curious person by nature, and I spent over four years as a BI consultant working with SAP BusinessObjects, maintaining universes and Web Intelligence reports over complex ERP data, including P&L reporting. Today, many SAP customers are moving their reporting to the cloud, to SAP Datasphere and SAP Analytics Cloud. Migration tools can convert objects, but not knowledge: someone still has to understand legacy universes (often poorly documented), decide what should be redesigned rather than copied, and prove that the numbers still match after the move. This project is my way of bridging both worlds: I take a classic P&L reporting scenario, the kind I used to build in BusinessObjects, and rebuild it on SAP HANA Cloud, SAP Datasphere and SAP Analytics Cloud, with data quality checks to make sure the numbers can be trusted. I'm building it sprint by sprint while learning the new stack, and documenting what I learn along the way.

## Roadmap

- [x] Sprint 0: Setup and SAP landscape
- [ ] Sprint 1: S/4HANA-style finance data
- [ ] Sprint 2: Data quality checks
- [ ] Sprint 3: SAP HANA Cloud
- [ ] Sprint 4: BusinessObjects → Datasphere mapping
- [ ] Sprint 5: SAP Datasphere model
- [ ] Sprint 6: SAP Analytics Cloud story
- [ ] Sprint 7: Wrap-up
