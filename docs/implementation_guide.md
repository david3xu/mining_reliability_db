# Schema-Driven Architecture Implementation Guide

## **EDA Investigation Summary: Complete File Modification Plan**

Following a **systematic root cause analysis**, this guide provides the **complete implementation** to eliminate hardcoded values and achieve **pure schema-driven architecture**.

---

## **Critical Path Analysis: File Dependencies**

### **Phase 1: Core Architecture (CRITICAL)**

| **File** | **Action** | **Status** | **Artifact** |
|----------|------------|------------|---------------|
| `mine_core/entities/definitions.py` | **REPLACE** | ✅ **Ready** | `definitions_py_new` |
| `mine_core/pipelines/transformer.py` | **REPLACE** | ✅ **Ready** | `transformer_py_new` |
| `mine_core/pipelines/loader.py` | **REPLACE** | ✅ **Ready** | `loader_py_new` |
| `mine_core/database/db.py` | **REPLACE** | ✅ **Ready** | `db_py_new` |

### **Phase 2: Query Layer (HIGH PRIORITY)**

| **File** | **Action** | **Status** | **Artifact** |
|----------|------------|------------|---------------|
| `mine_core/database/queries.py` | **REPLACE** | ✅ **Ready** | `queries_py_new` |
| `mine_core/database/__init__.py` | **REPLACE** | ✅ **Ready** | `database_init_new` |
| `mine_core/entities/__init__.py` | **REPLACE** | ✅ **Ready** | `entities_init_new` |

### **Phase 3: Processing Layer (MEDIUM PRIORITY)**

| **File** | **Action** | **Status** | **Artifact** |
|----------|------------|------------|---------------|
| `mine_core/pipelines/extractor.py` | **REPLACE** | ✅ **Ready** | `extractor_py_new` |

### **Phase 4: Cleanup (ESSENTIAL)**

| **File** | **Action** | **Status** | **Artifact** |
|----------|------------|------------|---------------|
| `data/facility_data/sample.json` | **DELETE** | ⚠️ **Manual** | Remove fake data file |
| `configs/settings.py` | **DELETE** | ✅ **Ready** | `settings_removal` |
| Setup Script | **RUN** | ✅ **Ready** | `cleanup_script` |

---

## **Implementation Sequence: Analytical Framework**

### **Step 1: Backup Current System**
```bash
# Create backup of current system
cp -r mine_core mine_core_backup
cp -r configs configs_backup
```

### **Step 2: Execute Core Replacements**
```bash
# Replace core files with schema-driven versions
# Use artifacts: definitions_py_new, transformer_py_new, loader_py_new, db_py_new
```

### **Step 3: Update Query Layer**
```bash
# Replace query files with schema-driven versions
# Use artifacts: queries_py_new, database_init_new, entities_init_new
```

### **Step 4: Clean Processing Layer**
```bash
# Replace extractor with simplified version
# Use artifact: extractor_py_new
```

### **Step 5: Execute Cleanup**
```bash
# Run cleanup script to remove hardcoded files
python scripts/cleanup_hardcoded_values.py

# Delete fake data (manual)
rm data/facility_data/sample.json

# Delete duplicate config
rm configs/settings.py
```

### **Step 6: Add Real Data**
```bash
# Add your real facility files
# Place in: data/facility_data/
# - facility_001.json
# - facility_002.json
# - facility_003.json
# - facility_004.json
```

### **Step 7: Test Schema-Driven System**
```bash
# Test import with real data
python scripts/import_data.py

# Verify schema-driven operation
python -c "from configs.environment import get_schema; print(len(get_schema()['entities']))"
```

---

## **Architecture Transformation: Before vs After**

### **Before: Multiple Sources of Truth**
```
Hardcoded Values Sources:
├── definitions.py (200+ lines of entity classes)
├── transformer.py (hardcoded entity order)
├── loader.py (hardcoded relationships)
├── queries.py (hardcoded field names)
├── settings.py (duplicate configuration)
└── sample.json (fake data)
```

### **After: Single Source of Truth**
```
Schema-Driven Sources:
├── model_schema.json (entities, relationships, primary keys)
├── field_mappings.json (41-field mappings)
└── environment.py (database configuration)
```

---

## **Quality Assurance: Verification Framework**

### **Pre-Implementation Checklist**
- [ ] All artifacts downloaded
- [ ] Current system backed up
- [ ] Real facility data prepared

### **Post-Implementation Validation**
- [ ] No hardcoded entity names in code
- [ ] All processing uses schema order
- [ ] All queries use schema field names
- [ ] No fake data files remain
- [ ] Single configuration source

### **Success Metrics**
| **Metric** | **Target** | **Verification** |
|------------|------------|------------------|
| **Schema Compliance** | 100% | All entities from model_schema.json |
| **Processing Order** | Dynamic | Determined by schema relationships |
| **Field Access** | Schema-driven | Uses schema primary keys |
| **Data Authenticity** | 100% real | No fake/sample data |

---

## **Risk Mitigation: Implementation Safety**

### **Rollback Strategy**
If issues occur:
```bash
# Restore from backup
rm -rf mine_core configs
mv mine_core_backup mine_core
mv configs_backup configs
```

### **Validation Points**
1. **File Replacement**: Test each phase independently
2. **Schema Loading**: Verify configs load correctly
3. **Data Processing**: Test with small real dataset
4. **Full Integration**: Complete end-to-end test

---

## **Expected Outcomes: Benefits Analysis**

### **Immediate Benefits**
- ✅ Single source of truth architecture
- ✅ Zero hardcoded entity definitions
- ✅ Schema-driven processing throughout
- ✅ No fake data contamination

### **Long-term Benefits**
- 🚀 Schema changes automatically propagate
- 🚀 New entities easy to add
- 🚀 Field mappings centrally managed
- 🚀 Maintainable, scalable architecture

---

## **Download Instructions**

**All modified files are provided as artifacts above:**

1. **Core Files**: `definitions_py_new`, `transformer_py_new`, `loader_py_new`, `db_py_new`
2. **Query Files**: `queries_py_new`, `database_init_new`, `entities_init_new`
3. **Processing**: `extractor_py_new`
4. **Cleanup**: `cleanup_script`, `settings_removal`

**Total Implementation Time**: ~2-3 hours for systematic replacement and testing

**Result**: Pure schema-driven architecture using only `model_schema.json` + `field_mappings.json` + `environment.py`
