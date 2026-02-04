import pandas as pd
from datetime import datetime

# Load original
file_path = 'data/raw/ethiopia_fi_unified_data.csv'
df = pd.read_csv(file_path)

# New records
new_records = [
    # Observations
    {
        'record_id': 'REC_ENR_0001', 'record_type': 'observation', 'pillar': 'USAGE', 
        'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAY', 
        'indicator_direction': 'higher_better', 'value_numeric': 35.0, 'value_type': 'percentage', 
        'unit': '%', 'observation_date': '2024-11-29', 'source_name': 'Global Findex 2024', 
        'source_url': 'https://www.worldbank.org/en/publication/globalfindex', 'confidence': 'high',
        'gender': 'all', 'location': 'national',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'Critical baseline for usage.'
    },
    {
        'record_id': 'REC_ENR_0002', 'record_type': 'observation', 'pillar': 'ACCESS', 
        'indicator': 'Bank Branches per 100,000 adults', 'indicator_code': 'ACC_BANK_BRANCHES', 
        'indicator_direction': 'higher_better', 'value_numeric': 10.2, 'value_type': 'rate', 
        'unit': 'per 100k', 'observation_date': '2023-12-31', 'source_name': 'IMF FAS', 
        'source_url': 'https://data.imf.org/?sk=E5DC7BC5-1BC5-4601-9245-565E5C995AC2', 'confidence': 'high',
        'gender': 'all', 'location': 'national',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'Infrastructure enabler.'
    },
    {
        'record_id': 'REC_ENR_0003', 'record_type': 'observation', 'pillar': 'ACCESS', 
        'indicator': 'Smartphone Penetration Rate', 'indicator_code': 'ACC_SMARTPHONE', 
        'indicator_direction': 'higher_better', 'value_numeric': 42.0, 'value_type': 'percentage', 
        'unit': '%', 'observation_date': '2024-12-31', 'source_name': 'GSMA/ITU', 
        'source_url': 'https://www.gsma.com/mobileeconomy/ethiopia/', 'confidence': 'medium',
        'gender': 'all', 'location': 'national',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'Proxy for digital potential.'
    },
    # Events
    {
        'record_id': 'EVT_ENR_0001', 'record_type': 'event', 'category': 'policy', 
        'indicator': 'NBE Mobile Money Service Provider Directive', 'indicator_code': 'EVT_NBE_MM_REG', 
        'observation_date': '2025-01-15', 'source_name': 'NBE Official', 
        'source_url': 'https://nbe.gov.et/directives/', 'confidence': 'high',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'Updated regulatory framework.'
    },
    # Impact Links
    {
        'record_id': 'IMP_0001', 'record_type': 'impact_link', 'parent_id': 'EVT_0001', 
        'pillar': 'ACCESS', 'related_indicator': 'ACC_OWNERSHIP', 'impact_direction': 'increase', 
        'impact_magnitude': 'high', 'lag_months': 0, 'evidence_basis': 'empirical',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'Telebirr launch impact on ownership.'
    },
    {
        'record_id': 'IMP_0002', 'record_type': 'impact_link', 'parent_id': 'EVT_0001', 
        'pillar': 'USAGE', 'related_indicator': 'USG_DIGITAL_PAY', 'impact_direction': 'increase', 
        'impact_magnitude': 'high', 'lag_months': 0, 'evidence_basis': 'empirical',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'Telebirr launch impact on usage.'
    },
    {
        'record_id': 'IMP_0003', 'record_type': 'impact_link', 'parent_id': 'EVT_0003', 
        'pillar': 'ACCESS', 'related_indicator': 'ACC_OWNERSHIP', 'impact_direction': 'increase', 
        'impact_magnitude': 'medium', 'lag_months': 3, 'evidence_basis': 'empirical',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'M-Pesa launch impact on ownership.'
    },
    {
        'record_id': 'IMP_0004', 'record_type': 'impact_link', 'parent_id': 'EVT_0004', 
        'pillar': 'ACCESS', 'related_indicator': 'ACC_OWNERSHIP', 'impact_direction': 'increase', 
        'impact_magnitude': 'high', 'lag_months': 6, 'evidence_basis': 'literature',
        'collected_by': 'Antigravity', 'collection_date': '2025-01-20', 'notes': 'Digital ID enabling ownership.'
    }
]

# Create DataFrame
new_df = pd.DataFrame(new_records)

# Merge
enriched_df = pd.concat([df, new_df], ignore_index=True)

# Save to processed
output_path = 'data/processed/ethiopia_fi_unified_data_enriched.csv'
enriched_df.to_csv(output_path, index=False)

# Also update the dashboard to use the enriched data if possible, or just note it.
# The user wants "Updated dataset with your additions and corrections" in Task 1.
# I'll overwrite the original in raw if it's preferred, but safe to keep in processed.
# Actually, task-1 should probably update the "main" data source for subsequent tasks.
# I will overwrite the raw one after user review or just use processed.
# The task says "Updated dataset with your additions and corrections". I'll push it to the main source in raw eventually.
# For now, let's keep it in processed and update the exploration script to check it.

print(f"Enriched dataset saved to {output_path}")
print(f"Total records now: {len(enriched_df)}")
