# Facility Data Splitter

This script splits facility data JSON files into individual JSON files for each record.

## Usage

### Basic Usage

```bash
# Run from the project root directory
python scripts/split_facility_records.py
```

This will:

- Read all JSON files from `data/facility_data/`
- Create subfolders in `data/facility_data/split_records/`
- Generate individual JSON files for each record

### Advanced Usage

```bash
# Custom input and output directories
python scripts/split_facility_records.py \
    --input-dir data/facility_data \
    --output-dir data/output/individual_records

# Process only specific files
python scripts/split_facility_records.py \
    --file-pattern "*sample*.json"
```

### Command Line Options

- `--input-dir`: Directory containing input JSON files (default: `data/facility_data`)
- `--output-dir`: Directory for output files (default: `data/facility_data/split_records`)
- `--file-pattern`: File pattern to match (default: `*.json`)

## Output Structure

For each input file, the script creates:

1. A subfolder named after the input file (without extension)
2. Individual JSON files for each record in that subfolder

### Example

Input file: `sample_5_fab16f86-faa9-44d9-b9d7-cfbbb47061da.json`

Output structure:

```
data/facility_data/split_records/
└── sample_5_fab16f86-faa9-44d9-b9d7-cfbbb47061da/
    ├── 0000_2023-04657.json
    ├── 0001_2021-08906.json
    ├── 0002_2023-07250.json
    └── ...
```

## File Naming Convention

Individual JSON files are named using:

- 4-digit sequence number (0000, 0001, etc.)
- Meaningful identifier from the record (e.g., Action Request Number, Title)
- `.json` extension

Examples:

- `0000_2023-04657.json` (using Action Request Number)
- `0001_Unplanned_maintenance_on_generator.json` (using Title if no Action Request Number)

## Supported Input Formats

The script handles different JSON structures:

1. **Direct array**: `[{record1}, {record2}, ...]`
2. **Nested under 'records'**: `{"records": [{record1}, {record2}, ...]}`
3. **Single record**: `{record}`

## Metadata

Each individual JSON file includes additional metadata:

```json
{
  "Action Request Number:": "2023-04657",
  "Title": "...",
  // ... original record data ...
  "_split_metadata": {
    "source_file": "original_file.json",
    "record_index": 0,
    "split_timestamp": null
  }
}
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
